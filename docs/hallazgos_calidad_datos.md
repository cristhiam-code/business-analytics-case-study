# Hallazgos de calidad de datos — Proyecto Farmanorte

Este documento resume los problemas de calidad detectados durante el análisis, su impacto en la interpretación del negocio y la forma en que se gestionaron.

## Resumen ejecutivo

En este proyecto, la calidad de datos se trató como una parte del análisis de negocio y no solo como una tarea técnica. La intención fue verificar si los indicadores eran confiables para apoyar decisiones de operación.

Los hallazgos principales muestran que:

- el flujo de transformación puede corregir errores de formato,
- algunas columnas tienen limitaciones de origen que deben documentarse,
- y el valor de negocio no depende solo de la limpieza, sino también de la forma en que se interpreta la información.

## 1. Error de formato en precio de venta (corregido)

**Cómo se detectó:**
Se identificó una discrepancia entre el valor del precio observado en el análisis y la referencia comercial esperada para un producto relevante del portafolio.

**Investigación:**
- Se comparó la fuente disponible con la salida analítica y se confirmó que la discrepancia estaba en el tratamiento del dato, no en la fuente base.
- Se localizó el problema en la etapa de normalización y se corrigió la lógica de conversión.
**Causa raíz:**
La función estaba diseñada para limpiar precios en formato de texto
colombiano (ej. `"1.500,50"`), pero no distinguía si el valor ya llegaba
como número. Al aplicarse sobre un float ya limpio (ej. `256900.0`), la
función lo convertía a texto (`"256900.0"`) y eliminaba el punto pensando
que era separador de miles, generando `2569000.0` — un cero de más.

**Corrección aplicada:**
Se ajustó la lógica para evitar transformar valores ya normalizados como texto, preservando el formato numérico correcto antes de continuar con el análisis.

**Alcance:** afectaba la columna `precio_venta` (y por extensión
`val_vendido`) en `matriz_bcg` y `productos_especiales`, para todo valor
que llegara como número desde el Excel de origen.

**Estado:** ✅ Corregido y verificado.

---

## 2. Columna `costo_promedio` vacía en el 100% del catálogo (LIMITACIÓN CONOCIDA)

**Cómo se detectó:**
Al validar la consistencia del margen, se encontró que una parte significativa del catálogo mostraba una expectativa de costo inexistente en la fuente disponible.

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
- La columna `rentabilidad` mantiene valor analítico para la gran mayoría del catálogo.
- La ausencia de `costo_promedio` en la fuente impide usar esa columna como base de comparación de margen.
- La limitación del dato debe reconocerse explícitamente para evitar sobreinterpretación en decisiones comerciales.

**Estado:** ⚠️ Limitación conocida, no corregible desde el proyecto (depende
de que el sistema de origen exporte el costo real). Pendiente de consultar
con Farmanorte si ese dato existe en otro reporte.

---

## Recomendación ejecutiva

Para una versión de portafolio, el valor de estos hallazgos está en demostrar rigor analítico y criterio de negocio:

- se identificaron y corrigieron errores de tratamiento,
- se documentaron limitaciones reales de la fuente,
- y se evitó la generación de conclusiones basadas en datos mal interpretados.

Eso convierte la calidad de datos en una fortaleza del caso, no en un obstáculo técnico.