-- 1. ¿Qué laboratorios venden más?
-- Suma el valor vendido por laboratorio para identificar los proveedores con mayor participación.
SELECT laboratorio,
       SUM(COALESCE(val_vendido, 0)) AS total_vendido
FROM matriz_bcg
GROUP BY laboratorio
ORDER BY total_vendido DESC
LIMIT 20;

-- 2. ¿Qué productos generan más valor?
-- Ordena productos por valor vendido, mostrando el código de barras y métricas de inventario.
SELECT producto,
       codigo_barras,
       COALESCE(val_vendido, 0) AS val_vendido,
       COALESCE(existencia, 0) AS existencia,
       COALESCE(precio_venta, 0) AS precio_venta
FROM matriz_bcg
ORDER BY val_vendido DESC
LIMIT 20;

-- 3. ¿Qué vendedores tienen mejor desempeño?
-- Calcula total vendido, promedio por venta y comisiones totales por asesor.
SELECT v.nombre_vendedor,
       COUNT(*) AS cantidad_ventas,
       SUM(COALESCE(ve.valor_base, 0) * COALESCE(ve.cantidad, 0)) AS total_vendido,
       ROUND(AVG(COALESCE(ve.valor_base, 0) * COALESCE(ve.cantidad, 0)), 2) AS promedio_por_venta,
       SUM(COALESCE(ve.valor_comision, 0)) AS total_comision
FROM ventas_especiales ve
JOIN vendedores v ON ve.id_vendedor = v.id_vendedor
GROUP BY v.nombre_vendedor
ORDER BY total_vendido DESC
LIMIT 20;

-- 4. ¿Qué inventario está más comprometido?
-- Estima el valor de stock por producto y compara con el valor vendido.
SELECT producto,
       codigo_barras,
       laboratorio,
       COALESCE(existencia, 0) AS existencia,
       COALESCE(precio_venta, 0) AS precio_venta,
       COALESCE(existencia, 0) * COALESCE(precio_venta, 0) AS valor_stock,
       COALESCE(val_vendido, 0) AS val_vendido,
       COALESCE(rentabilidad, 0) AS rentabilidad
FROM matriz_bcg
ORDER BY valor_stock DESC
LIMIT 20;

-- 5. ¿Qué productos tienen bajo desempeño respecto a su inventario?
-- Un producto puede ser caro en stock pero tener baja rotación relativa.
SELECT producto,
       codigo_barras,
       laboratorio,
       COALESCE(existencia, 0) AS existencia,
       COALESCE(precio_venta, 0) AS precio_venta,
       COALESCE(existencia, 0) * COALESCE(precio_venta, 0) AS valor_stock,
       COALESCE(val_vendido, 0) AS val_vendido,
       COALESCE(rentabilidad, 0) AS rentabilidad,
       CASE WHEN COALESCE(existencia, 0) = 0 THEN NULL
            ELSE ROUND(COALESCE(val_vendido, 0) / existencia, 2)
       END AS ventas_por_stock
FROM matriz_bcg
ORDER BY ventas_por_stock ASC,
         valor_stock DESC
LIMIT 20;

-- 6. Pregunta: ¿Qué productos deberían reponerse primero? (alta rotación + poca existencia)

SELECT "producto", "laboratorio", "existencia", "unid_vendidas"
FROM "matriz_bcg"
WHERE "existencia" < 15
  AND "unid_vendidas" > 20
ORDER BY "unid_vendidas" DESC
; 

-- Pregunta: ¿Qué laboratorios concentran el 80% de las ventas totales?
-- (Análisis tipo Pareto / regla 80-20, usando función de ventana SUM() OVER())

SELECT laboratorio, total_vendido,
    SUM(total_vendido) OVER (ORDER BY total_vendido DESC) AS acumulado,
    ROUND(
        100.0 * SUM(total_vendido) OVER (ORDER BY total_vendido DESC)
        / SUM(total_vendido) OVER (), 2
    ) AS porcentaje_acumulado
FROM (
    SELECT "laboratorio", SUM("val_vendido") AS "total_vendido"
    FROM "matriz_bcg"
    GROUP BY "laboratorio"
)
ORDER BY total_vendido DESC
;

-- 7. ¿Qué productos deberían reponerse primero?
-- Prioridad alta: venden mucho y tienen poca existencia.
SELECT producto,
       laboratorio,
       COALESCE(existencia, 0) AS existencia,
       COALESCE(unid_vendidas, 0) AS unid_vendidas,
       COALESCE(val_vendido, 0) AS val_vendido,
       ROUND(COALESCE(unid_vendidas, 0) / NULLIF(COALESCE(existencia, 0), 0), 2) AS rotacion
FROM matriz_bcg
WHERE COALESCE(existencia, 0) > 0
ORDER BY rotacion DESC,
         unid_vendidas DESC
LIMIT 20;

-- 8. ¿Qué laboratorios concentran el 80% de las ventas?
WITH laboratorio_ventas AS (
    SELECT laboratorio,
           SUM(COALESCE(val_vendido, 0)) AS total_vendido
    FROM matriz_bcg
    GROUP BY laboratorio
),
ventas_rankeadas AS (
    SELECT laboratorio,
           total_vendido,
           SUM(total_vendido) OVER (ORDER BY total_vendido DESC) AS acumulado,
           SUM(total_vendido) OVER () AS total_general
    FROM laboratorio_ventas
)
SELECT laboratorio,
       total_vendido,
       ROUND(100.0 * acumulado / total_general, 2) AS porcentaje_acumulado
FROM ventas_rankeadas
WHERE ROUND(100.0 * acumulado / total_general, 2) <= 80
ORDER BY total_vendido DESC;

-- 9. ¿Qué productos tienen alta rentabilidad pero bajas ventas?
SELECT producto,
       laboratorio,
       COALESCE(rentabilidad, 0) AS rentabilidad,
       COALESCE(val_vendido, 0) AS val_vendido,
       COALESCE(unid_vendidas, 0) AS unid_vendidas
FROM matriz_bcg
ORDER BY rentabilidad DESC,
         val_vendido ASC
LIMIT 20;

-- 10. ¿Qué inventario representa mayor capital inmovilizado?
SELECT producto,
       laboratorio,
       COALESCE(existencia, 0) AS existencia,
       COALESCE(precio_venta, 0) AS precio_venta,
       COALESCE(existencia, 0) * COALESCE(precio_venta, 0) AS valor_stock
FROM matriz_bcg
ORDER BY valor_stock DESC
LIMIT 20;

-- 11. ¿Qué vendedores tienen el ticket promedio más alto?
SELECT v.nombre_vendedor,
       ROUND(AVG(COALESCE(ve.valor_base, 0) * COALESCE(ve.cantidad, 0)), 2) AS ticket_promedio,
       COUNT(*) AS cantidad_ventas,
       SUM(COALESCE(ve.valor_base, 0) * COALESCE(ve.cantidad, 0)) AS total_vendido
FROM ventas_especiales ve
JOIN vendedores v ON ve.id_vendedor = v.id_vendedor
GROUP BY v.nombre_vendedor
ORDER BY ticket_promedio DESC
LIMIT 20;

-- 12. ¿Qué productos venden muchas unidades pero generan poco ingreso?
SELECT producto,
       laboratorio,
       COALESCE(unid_vendidas, 0) AS unid_vendidas,
       COALESCE(val_vendido, 0) AS val_vendido,
       ROUND(COALESCE(val_vendido, 0) / NULLIF(COALESCE(unid_vendidas, 0), 0), 2) AS ingreso_por_unidad
FROM matriz_bcg
WHERE COALESCE(unid_vendidas, 0) > 0
ORDER BY unid_vendidas DESC,
         val_vendido ASC
LIMIT 20;

-- 13. ¿Qué productos tienen alta existencia y baja rotación?
SELECT producto,
       laboratorio,
       COALESCE(existencia, 0) AS existencia,
       COALESCE(unid_vendidas, 0) AS unid_vendidas,
       ROUND(COALESCE(unid_vendidas, 0) / NULLIF(COALESCE(existencia, 0), 0), 2) AS rotacion
FROM matriz_bcg
WHERE COALESCE(existencia, 0) > 0
ORDER BY existencia DESC,
         rotacion ASC
LIMIT 20;

-- 14. ¿Qué productos generan la mayor rentabilidad estimada?
SELECT producto,
       laboratorio,
       COALESCE(rentabilidad, 0) AS rentabilidad_estimada,
       COALESCE(val_vendido, 0) AS val_vendido,
       COALESCE(existencia, 0) AS existencia
FROM matriz_bcg
ORDER BY rentabilidad DESC
LIMIT 20;



