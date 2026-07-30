from pathlib import Path
import pandas as pd


# =====================================================
# CONFIGURACIÓN DEL PROYECTO
# =====================================================

# Ruta base del proyecto, para que los scripts funcionen en cualquier equipo.
CARPETA_PROYECTO = Path(__file__).resolve().parent.parent
CARPETA_DATA = CARPETA_PROYECTO / "data"
CARPETA_RAW = CARPETA_DATA / "raw"
CARPETA_PROCESSED = CARPETA_DATA / "processed"
CARPETA_DATABASE = CARPETA_PROYECTO / "database"
ARCHIVO_DB = CARPETA_DATABASE / "farmanorte.db"


def asegurar_directorios(*rutas):
    """
    Crea los directorios necesarios antes de guardar datos.
    Esto evita errores de flujo cuando la carpeta no existe.
    """
    for ruta in rutas:
        ruta.mkdir(parents=True, exist_ok=True)


# =====================================================
# LECTURA Y ESCRITURA DE ARCHIVOS
# =====================================================

def leer_csv(ruta_archivo):
    """
    Lee un archivo CSV y devuelve un DataFrame.
    """

    return pd.read_csv(ruta_archivo)


def guardar_csv(dataframe, ruta_salida):
    """
    Guarda un DataFrame en un archivo CSV.
    """

    asegurar_directorios(ruta_salida.parent)
    dataframe.to_csv(ruta_salida, index=False)


# =====================================================
# LIMPIEZA DE COLUMNAS
# =====================================================

def renombrar_columnas(dataframe, columnas):
    """
    Renombra las columnas usando un diccionario.
    """

    return dataframe.rename(columns=columnas)


# =====================================================
# INFORMACIÓN DEL DATAFRAME
# =====================================================

def mostrar_resumen(dataframe):
    """
    Muestra un resumen general del DataFrame.
    """

    print(f"Filas: {len(dataframe)}")
    print(f"Columnas: {len(dataframe.columns)}")


def mostrar_columnas(dataframe):
    """
    Muestra los nombres de las columnas.
    """

    print("\nColumnas:")

    for columna in dataframe.columns:
        print(f"• {columna}")


def mostrar_tipos(dataframe):
    """
    Muestra el tipo de dato de cada columna.
    """

    print("\nTipos de datos:")
    print(dataframe.dtypes)


def mostrar_nulos(dataframe):
    """
    Muestra la cantidad de valores nulos por columna.
    """

    print("\nValores nulos:")

    nulos = dataframe.isna().sum()

    for columna, cantidad in nulos.items():
        print(f"• {columna}: {cantidad}")