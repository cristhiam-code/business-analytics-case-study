# =====================================================
# Script: importar_ventas_vendedores.py
# Objetivo: leer listado_especiales_completo.csv y
# productos_especiales (1).csv, y cargarlos en
# farmanorte.db como 3 tablas relacionadas:
#   - vendedores        (nombres unicos de asesores)
#   - ventas_especiales (cada venta, con FK a vendedores)
#   - productos_especiales
# =====================================================

import csv
import sqlite3

from utilidades import CARPETA_RAW, CARPETA_DATABASE, ARCHIVO_DB, asegurar_directorios

# --- Rutas del proyecto, no rutas absolutas del equipo ---
CSV_VENTAS = CARPETA_RAW / "listado_especiales_completo.csv"
CSV_PRODUCTOS_ESP = CARPETA_RAW / "productos_especiales (1).csv"
DB_PATH = ARCHIVO_DB


def limpiar_numero(valor):
    """
    Convierte un texto como '9,000' en el numero 9000.0
    Si el campo viene vacio, devuelve 0.0 en vez de fallar.
    """
    if valor is None or valor.strip() == "":
        return 0.0
    limpio = valor.replace(",", "").replace('"', "").strip()
    try:
        return float(limpio)
    except ValueError:
        return 0.0


def crear_tablas(conn):
    """
    Borra las 3 tablas si ya existian, y las vuelve a crear
    vacias, con sus columnas, tipos, y la relacion (FK)
    entre ventas_especiales y vendedores.
    """
    conn.execute('DROP TABLE IF EXISTS "ventas_especiales"')
    conn.execute('DROP TABLE IF EXISTS "vendedores"')
    conn.execute('DROP TABLE IF EXISTS "productos_especiales"')

    # Tabla de vendedores: cada nombre unico tiene su propio id
    conn.execute('''
        CREATE TABLE "vendedores" (
            "id_vendedor" INTEGER PRIMARY KEY AUTOINCREMENT,
            "nombre_vendedor" TEXT UNIQUE
        )
    ''')

    # Tabla de ventas: en vez de repetir el nombre del asesor
    # en cada fila, guarda solo su id (id_vendedor), que apunta
    # a la tabla vendedores. Eso es la clave foranea (FOREIGN KEY).
    conn.execute('''
        CREATE TABLE "ventas_especiales" (
            "id_venta" INTEGER PRIMARY KEY AUTOINCREMENT,
            "fecha" TEXT,
            "id_vendedor" INTEGER,
            "producto" TEXT,
            "valor_base" REAL,
            "cantidad" INTEGER,
            "valor_comision" REAL,
            FOREIGN KEY ("id_vendedor") REFERENCES "vendedores"("id_vendedor")
        )
    ''')

    # Tabla de productos especiales, independiente por ahora
    conn.execute('''
        CREATE TABLE "productos_especiales" (
            "cod_barras" TEXT PRIMARY KEY,
            "laboratorio" TEXT,
            "descripcion_completa" TEXT,
            "precio" REAL,
            "porcentaje_esp" REAL,
            "valor" REAL,
            "r30d" INTEGER
        )
    ''')


def importar_vendedores_y_ventas(conn):
    """
    Lee el CSV de ventas, extrae los nombres unicos de asesores
    para llenar "vendedores" primero, y luego inserta cada venta
    en "ventas_especiales" usando el id correspondiente del vendedor.
    """
    # Paso 1: leer todas las filas del CSV a memoria
    with open(CSV_VENTAS, encoding="utf-8-sig", newline="") as f:
        lector = csv.DictReader(f)
        filas_csv = list(lector)

    # Paso 2: sacar los nombres de asesor unicos, sin duplicados
    nombres_unicos = sorted(set(fila["asesor"].strip() for fila in filas_csv))

    # Paso 3: insertar cada nombre unico en la tabla vendedores
    for nombre in nombres_unicos:
        conn.execute(
            'INSERT INTO "vendedores" ("nombre_vendedor") VALUES (?)',
            (nombre,)
        )

    # Paso 4: construir un diccionario nombre -> id_vendedor
    cursor = conn.execute('SELECT "id_vendedor", "nombre_vendedor" FROM "vendedores"')
    mapa_nombre_a_id = {nombre: id_v for id_v, nombre in cursor.fetchall()}

    # Paso 5: preparar las filas de ventas, reemplazando el nombre
    # de texto por el id_vendedor correspondiente
    filas_ventas = []
    for fila in filas_csv:
        nombre = fila["asesor"].strip()
        id_vendedor = mapa_nombre_a_id[nombre]
        filas_ventas.append((
            fila["fecha"].strip(),
            id_vendedor,
            fila["producto"].strip(),
            limpiar_numero(fila["valor_Base"]),
            int(limpiar_numero(fila["cantidad"])),
            limpiar_numero(fila["valor_comision"]),
        ))

    # Paso 6: insertar todas las ventas de una sola vez
    conn.executemany(
        '''INSERT INTO "ventas_especiales"
           ("fecha", "id_vendedor", "producto", "valor_base", "cantidad", "valor_comision")
           VALUES (?,?,?,?,?,?)''',
        filas_ventas
    )

    print(f"vendedores: {len(nombres_unicos)} vendedores unicos importados")
    print(f"ventas_especiales: {len(filas_ventas)} ventas importadas")


def importar_productos_especiales(conn):
    """
    Lee productos_especiales (1).csv y lo inserta directo.
    """
    with open(CSV_PRODUCTOS_ESP, encoding="utf-8-sig", newline="") as f:
        lector = csv.DictReader(f)
        filas = []
        for fila in lector:
            filas.append((
                fila["COD_BARRAS"].strip(),
                fila["LABORATORIO"].strip(),
                fila["DESCRIPCION_COMPLETA"].strip(),
                limpiar_numero(fila["PRECIO"]),
                limpiar_numero(fila["%ESP"]),
                limpiar_numero(fila["VALOR"]),
                int(limpiar_numero(fila["R30D"])),
            ))

    conn.executemany(
        'INSERT INTO "productos_especiales" VALUES (?,?,?,?,?,?,?)',
        filas
    )
    print(f"productos_especiales: {len(filas)} filas importadas")


def main():
    """
    Orquesta todo: conecta, crea tablas, importa datos,
    guarda cambios y cierra.
    """
    asegurar_directorios(CARPETA_DATABASE)
    conn = sqlite3.connect(DB_PATH)

    crear_tablas(conn)
    importar_vendedores_y_ventas(conn)
    importar_productos_especiales(conn)

    conn.commit()
    conn.close()

    print("Listo.")


if __name__ == "__main__":
    main()