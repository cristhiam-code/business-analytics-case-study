-- BENEFICIOS PARA EL VENDEDOR EN PRODUCTOS ESPECIALES
-- ============================================================

-- 1. ¿Cuántos laboratorios distintos tenemos registrados?
SELECT COUNT(DISTINCT "laboratorio")
FROM "productos_especiales";


-- 2. ¿Cuáles son los 10 laboratorios con mayor bonificación promedio?
-- Nota: no tiene en cuenta el volumen de productos (ver consulta 5)
SELECT "laboratorio", AVG("porcentaje_esp") AS promedio_margen 
FROM "productos_especiales"
GROUP BY "laboratorio"
ORDER BY promedio_margen DESC
LIMIT 10;

-- 3. ¿Qué productos tiene un laboratorio específico y cuánto
--    bonifica cada uno?
SELECT "descripcion_completa", "porcentaje_esp", "precio_venta", "valor"
FROM "productos_especiales"
WHERE "laboratorio" = 'INTERBEL'
ORDER BY "porcentaje_esp" DESC;

-- 4. ¿Qué laboratorios tienen una bonificación promedio mayor
--    al 10%?
--
-- NOTA TÉCNICA: usamos HAVING en vez de WHERE porque estamos
-- filtrando sobre un valor calculado (AVG), y WHERE solo puede
-- filtrar filas individuales ANTES de agrupar.
-- ------------------------------------------------------------
SELECT "laboratorio", AVG("porcentaje_esp") AS promedio_margen
FROM "productos_especiales"
GROUP BY "laboratorio"
HAVING AVG("porcentaje_esp") > 10
ORDER BY promedio_margen DESC;

-- 5. ¿Qué laboratorios ofrecen la mejor bonificación de forma
--    CONFIABLE, es decir, respaldada por un volumen razonable
--    de productos (más de 10)?
--
-- POR QUÉ IMPORTA: corrige el problema de la consulta 2. Un
-- laboratorio con 1 solo producto al 20% no es representativo;
-- por eso exigimos AMBAS condiciones con AND: buen margen
-- Y suficiente cantidad de productos.
-- ------------------------------------------------------------
SELECT 
    "laboratorio",
    AVG("porcentaje_esp") AS promedio_margen,   -- bonificación promedio del laboratorio
    COUNT(*) AS cantidad_productos               -- cuántos productos respaldan ese promedio
FROM "productos_especiales"
GROUP BY "laboratorio"                            -- un grupo por cada laboratorio distinto
HAVING 
    AVG("porcentaje_esp") > 10                    -- solo laboratorios con más del 10% de margen
    AND COUNT(*) > 10                             -- y con más de 10 productos (evita datos aislados)
ORDER BY promedio_margen DESC;                    -- de mayor a menor bonificación

-- 6. ¿Qué productos bonifican más del 10% y cuántos son en total?
SELECT "descripcion_completa", "laboratorio", "porcentaje_esp", "precio_venta", "valor"
FROM "productos_especiales"
WHERE "porcentaje_esp" > 10
ORDER BY "porcentaje_esp" DESC;

SELECT COUNT(*)
FROM "productos_especiales"
WHERE "porcentaje_esp" > 10;    

-- 7. ¿Qué laboratorio vende más (valor total vendido)?
SELECT "laboratorio", SUM("val_vendido") AS total_vendido
FROM "matriz_bcg"
GROUP BY "laboratorio"
ORDER BY total_vendido DESC
LIMIT 10;