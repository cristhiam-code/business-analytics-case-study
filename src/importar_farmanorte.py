import sqlite3
import pandas as pd

from utilidades import CARPETA_PROCESSED, CARPETA_DATABASE, ARCHIVO_DB, asegurar_directorios

# =====================================================
# CONFIGURACIÓN DEL PROYECTO
# =====================================================

# El archivo limpio debe venir de data/processed, que es el paso intermedio del flujo.
ARCHIVO_CSV = CARPETA_PROCESSED / "kardex_productos.csv"


# =====================================================
# FUNCIONES
# =====================================================

def leer_kardex():
    """
    Lee el kardex limpio desde la ruta del proyecto.
    """

    if not ARCHIVO_CSV.exists():
        raise FileNotFoundError(
            "No se encontró el archivo limpio. Primero ejecuta limpiar_kardex.py"
        )

    return pd.read_csv(ARCHIVO_CSV)


def conectar_bd():
    """
    Crea la conexión con SQLite usando la ruta establecida para la base de datos.
    """

    asegurar_directorios(CARPETA_DATABASE)
    return sqlite3.connect(ARCHIVO_DB)


def importar_productos(dataframe, conexion):
    """
    Importa el DataFrame a la tabla productos.
    """

    dataframe.to_sql(
        "productos",
        conexion,
        if_exists="replace",
        index=False
    )


# =====================================================
# PROGRAMA PRINCIPAL
# =====================================================

if __name__ == "__main__":

    print("=" * 50)
    print("IMPORTANDO KARDEX A SQLITE")
    print("=" * 50)

    kardex = leer_kardex()

    conexion = conectar_bd()

    importar_productos(kardex, conexion)

    conexion.close()

    print(f"\nProductos importados: {len(kardex)}")
    print("Tabla creada: productos")
    print("Base de datos actualizada correctamente.")


def main():
    print("=" * 50)
    print("IMPORTANDO KARDEX A SQLITE")
    print("=" * 50)

    kardex = leer_kardex()

    conexion = conectar_bd()

    importar_productos(kardex, conexion)

    conexion.close()

    print(f"\nProductos importados: {len(kardex)}")
    print("Tabla creada: productos")
    print("Base de datos actualizada correctamente.")


if __name__ == "__main__":
    main()