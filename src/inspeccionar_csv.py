from pathlib import Path
import pandas as pd

# =====================================================
# CONFIGURACIÓN DEL PROYECTO
# =====================================================

# Carpeta principal del proyecto (mis-datos)
CARPETA_PROYECTO = Path(__file__).resolve().parent.parent

# Carpeta donde están los archivos CSV
CARPETA_CSV = CARPETA_PROYECTO / "csv"

# Carpeta donde está la base de datos
CARPETA_BASES = CARPETA_PROYECTO / "bases"


# =====================================================
# FUNCIONES
# =====================================================

def obtener_archivos_csv():
    """
    Devuelve todos los archivos CSV encontrados
    dentro de la carpeta csv.
    """
    return list(CARPETA_CSV.glob("*.csv"))


# =====================================================
# PROGRAMA PRINCIPAL
# =====================================================

if __name__ == "__main__":

    archivos_csv = obtener_archivos_csv()

    print("=" * 50)
    print("INSPECCIÓN DE ARCHIVOS CSV")
    print("=" * 50)

    print(f"\nSe encontraron {len(archivos_csv)} archivo(s).\n")

    for archivo in archivos_csv:

        print("-" * 50)
        print(f"Archivo: {archivo.name}")
        print("-" * 50)

        # Leer CSV
        df = pd.read_csv(archivo)

        # Información general
        print(f"Filas: {df.shape[0]}")
        print(f"Columnas: {df.shape[1]}")

        # Columnas
        print("\nNombres de las columnas:")

        for columna in df.columns:
            print(f"  • {columna}")

        # Tipos
        print("\nTipos de datos:")
        print(df.dtypes)

        # Valores nulos
        print("\nValores nulos:")

        valores_nulos = df.isna().sum()

        for columna, cantidad in valores_nulos.items():
            print(f"  • {columna}: {cantidad}")

        print()