from pathlib import Path
import sys

SRC_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SRC_DIR))

from limpiar_kardex import main as limpiar_main
from importar_farmanorte import main as importar_farmanorte_main
from importar_matriz_bcg import main as importar_matriz_bcg_main
from importar_ventas_vendedores import main as importar_ventas_vendedores_main
from normalize_productos import main as normalize_productos_main
from normalize_more_tables import main as normalize_more_tables_main


def main():
    steps = [
        ("Limpiar kardex", limpiar_main),
        ("Importar kardex a SQLite", importar_farmanorte_main),
        ("Importar matriz BCG", importar_matriz_bcg_main),
        ("Importar ventas y productos especiales", importar_ventas_vendedores_main),
        ("Normalizar productos", normalize_productos_main),
        ("Normalizar más tablas", normalize_more_tables_main),
    ]

    print("=" * 70)
    print("PIPELINE COMPLETO FARMANORTE")
    print("=" * 70)

    for label, func in steps:
        print("\n" + "-" * 70)
        print(f"Ejecutando: {label}")
        func()

    print("\n" + "=" * 70)
    print("Pipeline completo.")


if __name__ == "__main__":
    main()
