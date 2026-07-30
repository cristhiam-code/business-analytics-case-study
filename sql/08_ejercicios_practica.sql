-- EJERCICIOS DE PRACTICA DE AGREGACIONES

-- 1. ¿Cuantos laboratorios diferentes hay en la tabla matriz_bcg?
SELECT COUNT(DISTINCT laboratorio) AS cantidad_laboratorios
FROM matriz_bcg;    

--2. ¿Cuantos productos distintos vende cada laboratorio?
SELECT laboratorio,
       COUNT(*) AS cantidad_productos
FROM matriz_bcg
GROUP BY laboratorio
ORDER BY cantidad_productos DESC
LIMIT 20;   

--3. ¿Cuantos productos vendio cada vendedor?
-- cambio de tabla a ventas_especiales
SELECT v.nombre_vendedor,
SUM(ve.cantidad) AS "total_productos"
FROM ventas_especiales ve
JOIN vendedores v ON ve.id_vendedor = v.id_vendedor
GROUP BY v.nombre_vendedor
ORDER BY total_productos DESC;