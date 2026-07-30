from pathlib import Path
import sqlite3
import pandas as pd

from utilidades import CARPETA_PROCESSED, ARCHIVO_DB, asegurar_directorios

CSV_PATH = CARPETA_PROCESSED / "kardex_productos.csv"
DB_PATH = ARCHIVO_DB


def clean_number(value):
    if pd.isna(value):
        return 0.0
    s = str(value).strip()
    if s == "":
        return 0.0
    # Eliminar separadores de miles y caracteres no numéricos (coma y punto)
    s = s.replace('.', '').replace(',', '')
    # Eliminar simbolos no numericos
    s = ''.join(ch for ch in s if ch.isdigit())
    if s == "":
        return 0.0
    return float(s)


def table_exists(cursor, table_name):
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,)
    )
    return cursor.fetchone() is not None


def main():
    print("Leyendo:", CSV_PATH)
    df = pd.read_csv(CSV_PATH, dtype=str)

    # Asegurar que las columnas que esperamos existan
    expected = ["laboratorio", "codigo_barras", "producto",
                "existencias_cajas", "existencias_unidades",
                "valor_unitario", "valor_total"]

    # Normalizar nombres si vienen con otros nombres
    cols_map = {}
    for c in df.columns:
        lc = c.strip()
        if lc.lower() in ["laboratorio"]:
            cols_map[c] = "laboratorio"
        if lc.lower() in ["cod_barra", "cod_barra"]:
            cols_map[c] = "codigo_barras"
        if lc.lower() in ["producto"]:
            cols_map[c] = "producto"
        if lc.lower() in ["exist_caja", "existencias_cajas"]:
            cols_map[c] = "existencias_cajas"
        if lc.lower() in ["sist_unid", "existencias_unidades"]:
            cols_map[c] = "existencias_unidades"
        if lc.lower() in ["valor_unid", "valor_unitario", "valor_unitar"]:
            cols_map[c] = "valor_unitario"
        if lc.lower() in ["valor_total"]:
            cols_map[c] = "valor_total"

    df = df.rename(columns=cols_map)

    # Asegurar columnas esperadas
    for col in expected:
        if col not in df.columns:
            df[col] = None

    # Convertir tipos
    df["existencias_cajas"] = df["existencias_cajas"].fillna(0).apply(lambda x: int(float(x)) if str(x).strip() != '' else 0)
    df["existencias_unidades"] = df["existencias_unidades"].fillna(0).apply(lambda x: int(float(x)) if str(x).strip() != '' else 0)
    df["valor_unitario"] = df["valor_unitario"].fillna('0').apply(clean_number)
    df["valor_total"] = df["valor_total"].fillna('0').apply(clean_number)

    # Preparar inserción en SQLite
    asegurar_directorios(DB_PATH.parent)
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.cursor()

    # Crear tabla nueva normalizada
    cur.execute('DROP TABLE IF EXISTS productos_new')
    cur.execute('''
        CREATE TABLE productos_new (
            codigo_barras TEXT PRIMARY KEY,
            laboratorio TEXT,
            producto TEXT,
            existencias_cajas INTEGER,
            existencias_unidades INTEGER,
            valor_unitario REAL,
            valor_total REAL
        )
    ''')

    # Insertar filas (INSERT OR REPLACE para evitar duplicados)
    rows = []
    for _, r in df.iterrows():
        rows.append((
            str(r["codigo_barras"]).strip() if r["codigo_barras"] is not None else None,
            r["laboratorio"],
            r["producto"],
            int(r["existencias_cajas"]),
            int(r["existencias_unidades"]),
            float(r["valor_unitario"]),
            float(r["valor_total"]),
        ))

    cur.executemany('''INSERT OR REPLACE INTO productos_new
                       (codigo_barras, laboratorio, producto, existencias_cajas, existencias_unidades, valor_unitario, valor_total)
                       VALUES (?,?,?,?,?,?,?)''', rows)

    conn.commit()

    # Respaldar tabla antigua renombrándola
    cur.execute('DROP TABLE IF EXISTS productos_old_backup')
    if table_exists(cur, 'productos'):
        cur.execute("ALTER TABLE productos RENAME TO productos_old_backup")

    # Renombrar nueva a productos
    cur.execute('ALTER TABLE productos_new RENAME TO productos')

    # Crear indice en codigo_barras
    cur.execute('CREATE INDEX IF NOT EXISTS idx_productos_codigo_barras ON productos(codigo_barras)')

    conn.commit()
    cnt = cur.execute('SELECT COUNT(*) FROM productos').fetchone()[0]
    print(f"Migración completada. Filas en productos: {cnt}")
    conn.close()


if __name__ == '__main__':
    main()
