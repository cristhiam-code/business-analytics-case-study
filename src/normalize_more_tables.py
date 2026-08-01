import sqlite3
import pandas as pd
from utilidades import ARCHIVO_DB, asegurar_directorios

DB_PATH = ARCHIVO_DB


def to_float_safe(x):
    try:
        if pd.isna(x):
            return 0.0
        # Si YA es un número (int o float), lo devolvemos directo,
        # sin tratarlo como texto con separadores.
        if isinstance(x, (int, float)):
            return float(x)
        # Si es texto, aplicamos limpieza de formato colombiano
        s = str(x).strip()
        if s == "":
            return 0.0
        s = s.replace('.', '').replace(',', '.')
        try:
            return float(s)
        except ValueError:
            s_digits = ''.join(ch for ch in s if ch.isdigit())
            return float(s_digits) if s_digits else 0.0
    except Exception:
        return 0.0


def to_int_safe(x):
    try:
        if pd.isna(x):
            return 0
        return int(float(str(x).strip()))
    except Exception:
        return 0


def table_exists(cursor, table_name):
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,)
    )
    return cursor.fetchone() is not None


def normalize_matriz_bcg(conn):
    print('Normalizando matriz_bcg...')
    df = pd.read_sql_query('SELECT * FROM matriz_bcg', conn)
    if df.empty:
        print('matriz_bcg está vacía o no existe.')
        return
    # Normalizar columnas a lower
    df.columns = [c.strip() for c in df.columns]

    # Asegurar columnas canónicas
    col_map = {}
    for c in df.columns:
        lc = c.lower()
        if lc in ['codigo_barras', 'cod_barras', 'cod_barra']:
            col_map[c] = 'codigo_barras'
        elif lc in ['producto']:
            col_map[c] = 'producto'
        elif lc in ['laboratorio']:
            col_map[c] = 'laboratorio'
        elif lc in ['existencia', 'existencias', 'exist_caja']:
            col_map[c] = 'existencia'
        elif lc in ['precio_venta', 'precio']:
            col_map[c] = 'precio_venta'
        elif lc in ['costo_promedio', 'costo']:
            col_map[c] = 'costo_promedio'
        elif lc in ['unid_vendidas', 'unid_vend', 'unidades_vendidas']:
            col_map[c] = 'unid_vendidas'
        elif lc in ['val_vendido', 'valor_vendido', 'valor']:
            col_map[c] = 'val_vendido'
        elif lc in ['rentabilidad']:
            col_map[c] = 'rentabilidad'
        else:
            # keep others
            pass

    df = df.rename(columns=col_map)

    # Ensure canonical cols exist
    canonical = ['codigo_barras','producto','laboratorio','existencia','precio_venta','costo_promedio','unid_vendidas','val_vendido','rentabilidad','ranking_1','ranking_2','ranking_3','suma_ranking','ranking_final','grupo']
    for c in canonical:
        if c not in df.columns:
            df[c] = None

    # Convertir tipos
    df['existencia'] = df['existencia'].apply(to_int_safe)
    df['precio_venta'] = df['precio_venta'].apply(to_float_safe)
    df['costo_promedio'] = df['costo_promedio'].apply(to_float_safe)
    df['unid_vendidas'] = df['unid_vendidas'].apply(to_int_safe)
    df['val_vendido'] = df['val_vendido'].apply(to_float_safe)
    df['rentabilidad'] = df['rentabilidad'].apply(to_float_safe)

    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS matriz_bcg_new')
    cur.execute('''
        CREATE TABLE matriz_bcg_new (
            codigo_barras TEXT PRIMARY KEY,
            producto TEXT,
            laboratorio TEXT,
            existencia INTEGER,
            precio_venta REAL,
            costo_promedio REAL,
            unid_vendidas INTEGER,
            ranking_1 INTEGER,
            val_vendido REAL,
            ranking_2 INTEGER,
            rentabilidad REAL,
            ranking_3 INTEGER,
            suma_ranking INTEGER,
            ranking_final INTEGER,
            grupo TEXT
        )
    ''')

    rows = []
    for _, r in df.iterrows():
        rows.append((
            str(r['codigo_barras']) if r['codigo_barras'] is not None else None,
            r['producto'],
            r['laboratorio'],
            int(r['existencia']),
            float(r['precio_venta']),
            float(r['costo_promedio']) if r['costo_promedio'] is not None else None,
            int(r['unid_vendidas']) if r['unid_vendidas'] is not None else 0,
            int(r.get('ranking_1') or 0),
            float(r['val_vendido']),
            int(r.get('ranking_2') or 0),
            float(r['rentabilidad']) if r['rentabilidad'] is not None else None,
            int(r.get('ranking_3') or 0),
            int(r.get('suma_ranking') or 0),
            int(r.get('ranking_final') or 0),
            r.get('grupo')
        ))

    cur.executemany('''INSERT OR REPLACE INTO matriz_bcg_new
                       (codigo_barras, producto, laboratorio, existencia, precio_venta, costo_promedio, unid_vendidas, ranking_1, val_vendido, ranking_2, rentabilidad, ranking_3, suma_ranking, ranking_final, grupo)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', rows)
    conn.commit()

    # backup old
    cur.execute('DROP TABLE IF EXISTS matriz_bcg_old_backup')
    if table_exists(cur, 'matriz_bcg'):
        cur.execute('ALTER TABLE matriz_bcg RENAME TO matriz_bcg_old_backup')
    cur.execute('ALTER TABLE matriz_bcg_new RENAME TO matriz_bcg')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_matriz_codigo_barras ON matriz_bcg(codigo_barras)')
    conn.commit()
    print('matriz_bcg normalizada y renombrada.')


def normalize_productos_especiales(conn):
    print('Normalizando productos_especiales...')
    df = pd.read_sql_query('SELECT * FROM productos_especiales', conn)
    if df.empty:
        print('productos_especiales está vacía o no existe.')
        return
    df.columns = [c.strip() for c in df.columns]
    col_map = {}
    for c in df.columns:
        lc = c.lower()
        if lc in ['cod_barras', 'cod_barras', 'cod_barras']:
            col_map[c] = 'codigo_barras'
        elif lc in ['cod_barras']:
            col_map[c] = 'codigo_barras'
        elif lc in ['cod_barras']:
            col_map[c] = 'codigo_barras'
        elif lc in ['laboratorio']:
            col_map[c] = 'laboratorio'
        elif lc in ['descripcion_completa', 'descripcion']:
            col_map[c] = 'descripcion_completa'
        elif lc in ['precio']:
            col_map[c] = 'precio_venta'
        elif lc in ['%esp', 'porcentaje_esp', 'porcentaje']:
            col_map[c] = 'porcentaje_esp'
        elif lc in ['valor']:
            col_map[c] = 'valor'
        elif lc in ['r30d']:
            col_map[c] = 'r30d'

    df = df.rename(columns=col_map)

    canonical = ['codigo_barras','laboratorio','descripcion_completa','precio_venta','porcentaje_esp','valor','r30d']
    for c in canonical:
        if c not in df.columns:
            df[c] = None

    df['precio_venta'] = df['precio_venta'].apply(to_float_safe)
    df['porcentaje_esp'] = df['porcentaje_esp'].apply(to_float_safe)
    df['valor'] = df['valor'].apply(to_float_safe)
    df['r30d'] = df['r30d'].apply(to_int_safe)

    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS productos_especiales_new')
    cur.execute('''
        CREATE TABLE productos_especiales_new (
            codigo_barras TEXT PRIMARY KEY,
            laboratorio TEXT,
            descripcion_completa TEXT,
            precio_venta REAL,
            porcentaje_esp REAL,
            valor REAL,
            r30d INTEGER
        )
    ''')

    rows = []
    for _, r in df.iterrows():
        rows.append((
            str(r['codigo_barras']) if r['codigo_barras'] is not None else None,
            r['laboratorio'],
            r['descripcion_completa'],
            float(r['precio_venta']),
            float(r['porcentaje_esp']),
            float(r['valor']),
            int(r['r30d'])
        ))

    cur.executemany('''INSERT OR REPLACE INTO productos_especiales_new
                       (codigo_barras, laboratorio, descripcion_completa, precio_venta, porcentaje_esp, valor, r30d)
                       VALUES (?,?,?,?,?,?,?)''', rows)
    conn.commit()

    cur.execute('DROP TABLE IF EXISTS productos_especiales_old_backup')
    if table_exists(cur, 'productos_especiales'):
        cur.execute('ALTER TABLE productos_especiales RENAME TO productos_especiales_old_backup')
    cur.execute('ALTER TABLE productos_especiales_new RENAME TO productos_especiales')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_prod_esp_codigo_barras ON productos_especiales(codigo_barras)')
    conn.commit()
    print('productos_especiales normalizada y renombrada.')


def main():
    asegurar_directorios(DB_PATH.parent)
    conn = sqlite3.connect(str(DB_PATH))
    normalize_matriz_bcg(conn)
    normalize_productos_especiales(conn)
    conn.close()

if __name__ == '__main__':
    main()