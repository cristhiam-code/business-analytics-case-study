  # Proyecto Farmanorte Analytics

  ## Descripción general

  Este proyecto analiza datos de Farmanorte a partir de varios archivos CSV y una base de datos SQLite. El objetivo es mostrar un flujo completo de limpieza, normalización e importación de datos, junto con consultas SQL que responden preguntas de negocio.

  ## Objetivos

- Analizar el comportamiento de las ventas.
- Identificar los productos con mayor impacto en el negocio.
- Evaluar el desempeño de los laboratorios.
- Analizar el rendimiento de los vendedores.
- Detectar oportunidades de mejora en el inventario.
- Construir un flujo de trabajo reproducible para el análisis de datos.

    
  ## Estructura del proyecto

  - `data/raw/`: datos originales crudos
  - `data/processed/`: datos procesados y listos para importar
  - `database/`: base de datos SQLite (`farmanorte.db`) y backup (`farmanorte.db.bak`)
  - `docs/diccionario_datos.md`: diccionario de datos del proyecto
  - `src/`: scripts Python para limpieza, importación y normalización
  - `sql/`: consultas SQL con ejemplos y preguntas de negocio

  ## Requisitos

  Instala las dependencias del proyecto con:

  ```bash
  pip install -r requirements.txt
  ```

  ## Scripts principales

  ### 1. Limpiar y procesar datos

  `python3 src/limpiar_kardex.py`

  - Lee `data/raw/kardex_productos.csv`
  - Renombra columnas a formato canónico
  - Guarda el archivo limpio en `data/processed/kardex_productos.csv`

  ### 2. Importar datos a SQLite

  `python3 src/importar_farmanorte.py`

  - Importa `data/processed/kardex_productos.csv` a la tabla `productos` en `database/farmanorte.db`

  `python3 src/importar_matriz_bcg.py`

  - Importa `data/raw/MatrizBCG2_limpio_v2.xlsx` a la tabla `matriz_bcg`

  `python3 src/importar_ventas_vendedores.py`

  - Importa `data/raw/listado_especiales_completo.csv` y `data/raw/productos_especiales (1).csv`
  - Crea las tablas `vendedores`, `ventas_especiales` y `productos_especiales`

  ### 3. Normalización adicional

  `python3 src/normalize_productos.py`

  - Normaliza la tabla `productos` en la base de datos para usar nombres canónicos y tipos numéricos correctos.

  `python3 src/normalize_more_tables.py`

  - Normaliza las tablas `matriz_bcg` y `productos_especiales`
  - Conserva los respaldos en tablas con sufijo `_old_backup`

  ## Pipeline completo

  Ejecuta los siguientes comandos en el orden indicado para reproducir el flujo completo:

  ```bash
  pip install -r requirements.txt
  python3 src/run_pipeline.py
  ```

  Después puedes abrir la base de datos con SQLite y ejecutar las consultas en `sql/06_preguntas_negocio.sql`.

  ## Consultas SQL

  ### Archivos existentes

  - `sql/01_joins_basicos.sql`
  - `sql/02_subqueries.sql`
  - `sql/03_agregaciones_group_by.sql`
  - `sql/04_busquedas_like.sql`
  - `sql/05_rankings_ventas.sql`
  - `sql/06_preguntas_negocio.sql`

  ### Preguntas de negocio atendidas

  El archivo `sql/06_preguntas_negocio.sql` responde directamente a estas preguntas:
  - ¿Qué laboratorios venden más?
  - ¿Qué productos generan más valor?
  - ¿Qué vendedores tienen mejor desempeño?
  - ¿Qué inventario está más comprometido o menos rentable?

  ## Resultados principales

  Estos son los resultados obtenidos tras ejecutar las consultas sobre la base normalizada:

  - Laboratorios top por valor vendido:
    - `TRIDEX FARMACEUTICA`: 78.250.000
    - `NESTLE NUTRICION`: 50.797.000
    - `ABBOTT NUTRICION`: 47.612.700
    - `A.G. MEDICAMENTOS`: 32.895.000
    - `HALEON (GLAXO OTC)`: 30.121.700

  - Productos top por valor vendido:
    - `MOUNJARO 2.5MG/0.5ML * 1 AMP`
    - `ELECTROLIT MARACUYA * 625 ML`
    - `ENTEROGERMINA * 10 AMP`
    - `NESTOGENO TOTAL COMFORT *400 GR`
    - `PEDIALYTE MAX ZINC 60 FRESA * 500 ML`

  - Vendedores top por desempeño (total vendido):
    - `Cristhiam Adrian Botero Rojas`
    - `Jorge Hernando Sanjuan Vega`
    - `John Pablo  Hernandez  Arevalo`

  - Inventario más comprometido por valor de stock:
    - `MOUNJARO 2.5MG/0.5ML * 1 AMP`
    - `CONGESTEX * 10 CAP`
    - `ELECTROLIT MARACUYA * 625 ML`

  ## Notas importantes

  - Se creó un backup de la base de datos original en `database/farmanorte.db.bak`.
  - Las tablas con datos transformados y respaldos existen como:
    - `productos_old_backup`
    - `matriz_bcg_old_backup`
    - `productos_especiales_old_backup`

  ## Cómo verificar los datos

  Para ejecutar una consulta SQL desde la terminal:

  ```bash
  cd /home/cristhiam/data-analytics-portafolio/proyecto-farmanorte
  sqlite3 database/farmanorte.db
  .headers on
  .mode column
  .read sql/06_preguntas_negocio.sql
  ```

  También puedes copiar cualquier consulta de los archivos en `sql/` y ejecutarla directamente en SQLite.

## Autor

**Cristhiam Adrián Botero Rojas**

Proyecto desarrollado como parte de un portafolio de análisis de datos utilizando información real de una droguería para demostrar habilidades en SQL, Python, análisis exploratorio y resolución de problemas de negocio.