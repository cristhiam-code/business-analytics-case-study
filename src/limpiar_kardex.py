import pandas as pd

from utilidades import CARPETA_RAW, CARPETA_PROCESSED, asegurar_directorios

# =====================================================
# CONFIGURACIÓN DEL PROYECTO
# =====================================================

# Se usa la carpeta data/raw del proyecto, que es la ubicación real de los datos crudos.
ARCHIVO_ENTRADA = CARPETA_RAW / "kardex_productos.csv"

# Se guarda el resultado limpio en data/processed, que es la ruta usada por el flujo posterior.
ARCHIVO_SALIDA = CARPETA_PROCESSED / "kardex_productos.csv"


# =====================================================
# FUNCIONES
# =====================================================

def leer_kardex():
    """
    Lee el archivo del kardex desde la ruta correcta del proyecto.
    """

    dataframe = pd.read_csv(ARCHIVO_ENTRADA)

    return dataframe


def obtener_columnas_kardex():
    """
    Devuelve los nombres estándar que utilizará Farmanorte Analytics.
    Se usa un mapeo compatible con los nombres reales del archivo CSV actual.
    """

    return {
        "laboratorio": "laboratorio",
        "cod_Barra": "codigo_barras",
        "producto": "producto",
        "exist_Caja": "existencias_cajas",
        "sist_Unid": "existencias_unidades",
        "valor_unid": "valor_unitario",
        "valor_total": "valor_total"
    }


def renombrar_columnas(dataframe):
    """
    Cambia los nombres originales por los nombres estándar.
    """

    columnas = obtener_columnas_kardex()

    dataframe = dataframe.rename(columns=columnas)

    return dataframe


def guardar_kardex(dataframe):
    """
    Guarda el archivo limpio y crea la carpeta de salida si no existe.
    """

    asegurar_directorios(CARPETA_PROCESSED)
    dataframe.to_csv(ARCHIVO_SALIDA, index=False)


# =====================================================
# PROGRAMA PRINCIPAL
# =====================================================

if __name__ == "__main__":

    print("=" * 50)
    print("LIMPIEZA DEL KARDEX")
    print("=" * 50)

    kardex = leer_kardex()

    print(f"\nFilas originales: {len(kardex)}")

    kardex = renombrar_columnas(kardex)

    guardar_kardex(kardex)

    print("\nColumnas finales:")

    for columna in kardex.columns:
        print(f"• {columna}")

    print("\nProceso finalizado correctamente.")
    print(f"\nArchivo generado:")
    print(ARCHIVO_SALIDA)


def main():
    print("=" * 50)
    print("LIMPIEZA DEL KARDEX")
    print("=" * 50)

    kardex = leer_kardex()

    print(f"\nFilas originales: {len(kardex)}")

    kardex = renombrar_columnas(kardex)

    guardar_kardex(kardex)

    print("\nColumnas finales:")

    for columna in kardex.columns:
        print(f"• {columna}")

    print("\nProceso finalizado correctamente.")
    print(f"\nArchivo generado:")
    print(ARCHIVO_SALIDA)


if __name__ == "__main__":
    main()