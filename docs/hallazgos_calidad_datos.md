# Hallazgos de calidad de datos — Proyecto Farmanorte

Este documento registra problemas de calidad de datos detectados durante el
análisis de `matriz_bcg`, cómo se investigaron, y qué se hizo al respecto.
Se documentan como parte del proceso normal de análisis, no como errores
que invaliden el proyecto.

---

## 1. Precio de venta inflado por error en función de limpieza (CORREGIDO)

**Cómo se detectó:**
Al listar los productos con mayor valor vendido, el precio registrado de
MOUNJARO 2.5MG/0.5ML no coincidía con el precio real conocido del negocio
(el producto no supera los $250.000, pero el sistema mostraba $2.569.000).

**Investigación:**
- Se comparó el archivo fuente (`MatrizBCG2_limpio_v2.xlsx`) contra la base
  de datos: el Excel tenía el precio correcto ($256.900).
- Se identificó que el error se introducía en el script
  `src/normalize_more_tables.py`, en la función `to_float_safe()`.

**Causa raíz:**
La función estaba diseñada para limpiar precios en formato de texto
colombiano (ej. `"1.500,50"`), pero no distinguía si el valor ya llegaba
como número. Al aplicarse sobre un float ya limpio (ej. `256900.0`), la
función lo convertía a texto (`"256900.0"`) y eliminaba el punto pensando
que era separador de miles, generando `2569000.0` — un cero de más.

**Corrección aplicada:**
Se modificó `to_float_safe()` para devolver directamente el valor si ya es
numérico (`int`/`float`), y solo aplicar la limpieza de formato de texto
cuando el dato llega como string. Se volvió a correr el pipeline completo
(`run_pipeline.py`) y se regeneraron el notebook de análisis y los CSV
exportados.

**Alcance:** afectaba la columna `precio_venta` (y por extensión
`val_vendido`) en `matriz_bcg` y `productos_especiales`, para todo valor
que llegara como número desde el Excel de origen.

**Estado:** ✅ Corregido y verificado.

---

## 2. Columna `costo_promedio` vacía en el 100% del catálogo (LIMITACIÓN CONOCIDA)

**Cómo se detectó:**
Al calcular el margen de rentabilidad (`rentabilidad / val_vendido`), varios
productos mostraban un margen de exactamente 100%, lo cual no es realista
(todo producto tiene un costo de compra).

**Investigación:**
```sql
SELECT COUNT(*) AS total_productos,
    SUM(CASE WHEN costo_promedio = 0 THEN 1 ELSE 0 END) AS con_costo_cero
FROM matriz_bcg;
```
Resultado: **1143 de 1143 productos** (100% del catálogo) tienen
`costo_promedio = 0`. La columna nunca se pobló con datos reales desde el
origen.

**Matiz importante:** inicialmente se asumió que esto invalidaba también la
columna `rentabilidad` (rentabilidad = venta - 0 = venta, siempre). Se
verificó esa hipótesis:
```sql
SELECT
    SUM(CASE WHEN rentabilidad = val_vendido THEN 1 ELSE 0 END) AS coinciden,
    SUM(CASE WHEN rentabilidad != val_vendido THEN 1 ELSE 0 END) AS no_coinciden
FROM matriz_bcg;
```
Resultado: solo **5 de 1143 productos** tienen `rentabilidad = val_vendido`.
Los otros 1138 (99.6%) tienen un valor de rentabilidad distinto y
consistente con un cálculo real de margen.

**Conclusión:**
- La columna `rentabilidad` **sí es confiable** para el 99.6% del catálogo.
  Probablemente el sistema de origen calcula el margen internamente sin
  exponer el costo real en la columna `costo_promedio`.
- Los 5 casos donde `rentabilidad = val_vendido` corresponden a productos
  con `unid_vendidas = 1` (una sola venta registrada) — es probable que el
  sistema no tuviera costo de referencia para productos de tan baja
  rotación.
- La columna `costo_promedio` **no debe usarse** en ningún análisis
  mientras siga vacía en el origen.

**Estado:** ⚠️ Limitación conocida, no corregible desde el proyecto (depende
de que el sistema de origen exporte el costo real). Pendiente de consultar
con Farmanorte si ese dato existe en otro reporte.

---

## Cómo se investigan hallazgos de calidad de datos en este proyecto

1. No se asume que un dato "raro" es un error sin comprobarlo con SQL.
2. Se compara siempre contra la fuente original (Excel/CSV) antes de
   sospechar de un script.
3. Se cuantifica el alcance del problema (¿cuántas filas afecta?) antes de
   decidir si corregir o documentar.
4. Toda corrección de código se verifica con una consulta puntual después
   de aplicarla.