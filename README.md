  # Farmanorte Portfolio Analytics

## Resumen ejecutivo

Este repositorio presenta un caso de análisis comercial aplicado a una operación de droguería. El objetivo del proyecto es convertir datos operativos en señales útiles para la toma de decisiones en ventas, inventario y rentabilidad.

La historia de negocio del proyecto es clara:

- identificar qué laboratorios y productos concentran mayor valor,
- detectar qué inventario requiere revisión por su nivel de compromiso,
- apoyar decisiones de operación con una base analítica reproducible.

## Contexto del negocio

El análisis se enfoca en un escenario de retail farmacéutico, donde el valor del negocio depende de la combinación entre:

- volumen de ventas,
- mix de productos,
- participación de laboratorios,
- inventario y rotación.

## Problema de negocio

La empresa necesita entender dónde está concentrado el valor del negocio y qué segmentos requieren atención operativa. El proyecto responde a esa necesidad mediante limpieza, normalización y análisis estructurado de las fuentes disponibles.

## Preguntas de negocio

- ¿Qué laboratorios aportan mayor valor comercial?
- ¿Qué productos concentran más ventas y mayor relevancia en el portafolio?
- ¿Qué inventario está más comprometido o requiere intervención?
- ¿Qué señales permiten apoyar decisiones de ventas y reposición?

## Qué demuestra este proyecto

El proyecto evidencia que el autor puede:

- preparar datos para análisis,
- construir un flujo reproducible,
- trabajar con SQL y Python,
- documentar hallazgos de calidad,
- transformar datos operativos en insights accionables.

## Estructura del repositorio

- `data/raw/`: fuentes crudas locales y no públicas.
- `data/processed/`: datos preparados para importación y para mostrarse como evidencia analítica.
- `database/`: base SQLite local usada para análisis; no debe publicarse en la versión abierta.
- `docs/diccionario_datos.md`: diccionario de tablas y columnas.
- `docs/hallazgos_calidad_datos.md`: hallazgos de negocio y calidad de datos.
- `docs/publicacion_segura.md`: guía de preparación para una versión `safe publish`.
- `src/`: scripts de limpieza, importación y normalización.
- `sql/`: consultas analíticas del caso.
- `notebooks/`: notebook como entregable final.

## Requisitos

```bash
pip install -r requirements.txt
```

## Ejecución reproducible

```bash
python3 src/run_pipeline.py
```

El pipeline ejecuta las etapas principales en orden:

1. limpieza del kardex,
2. importación a SQLite,
3. carga de la matriz BCG,
4. carga de ventas y productos especiales,
5. normalización de tablas principales.

## Scripts principales

- `src/limpiar_kardex.py`: limpia y normaliza el archivo de inventario.
- `src/importar_farmanorte.py`: importa el kardex a SQLite.
- `src/importar_matriz_bcg.py`: carga la matriz BCG.
- `src/importar_ventas_vendedores.py`: carga ventas y vendedores.
- `src/normalize_productos.py`: normaliza la tabla principal.
- `src/normalize_more_tables.py`: normaliza tablas complementarias.

## Consultas de negocio

La consulta central de este caso está en `sql/06_preguntas_negocio.sql` y sirve como evidencia del análisis de negocio.

## Hallazgos clave

Este proyecto permite identificar patrones de negocio importantes como:

- concentración de valor en pocos laboratorios,
- relevancia de ciertos productos en el mix comercial,
- inventario con alto valor asociado y necesidad de revisión,
- señales de desempeño útiles para priorizar decisiones operativas.

## Versión pública y segura

La versión pública del repositorio debe presentar el caso analítico sin incluir información operativa sensible. Para una publicación en GitHub o LinkedIn, conviene:

- mantener el código, la documentación y el notebook como evidencia,
- excluir la base local y las fuentes crudas,
- publicar solo la capa analítica y documentada del proyecto.

La estrategia recomendada está resumida en `docs/publicacion_segura.md`.

## Notas de calidad y reproducibilidad

- El flujo se mantiene reproducible.
- La documentación expone limitaciones y correcciones aplicadas.
- La versión pública debe usar solo una capa segura de outputs y documentación, sin incluir datos crudos ni la base local.
- El proyecto está preparado para ser presentado como un caso analítico, no solo como un conjunto de scripts.

## Verificación del análisis

```bash
cd /home/cristhiam/data-analytics-portafolio/proyecto-farmanorte
sqlite3 database/farmanorte.db
.headers on
.mode column
.read sql/06_preguntas_negocio.sql
```

> En la versión pública, esta verificación debe ejecutarse con un dataset local seguro y no con la fuente de producción original.

## Autor

**Cristhiam Adrián Botero Rojas**

Proyecto desarrollado como caso de análisis de negocio para mostrar habilidades en SQL, Python, preparación de datos, análisis exploratorio y uso de información para decisiones comerciales. 