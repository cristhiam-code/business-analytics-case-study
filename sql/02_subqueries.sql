-- Pregunta: ¿Qué productos de matriz_bcg tienen una rentabilidad
-- por encima del promedio de todo el catálogo?

SELECT *
FROM "matriz_bcg"
WHERE "rentabilidad" >
(
    SELECT AVG("rentabilidad")
    FROM "matriz_bcg"
);

-- 2. ¿Qué porcentaje del total vendido representan los 50 productos principales?
SELECT 
    (SELECT SUM("val_vendido") 
     FROM (SELECT "val_vendido" FROM "matriz_bcg" ORDER BY "val_vendido" DESC LIMIT 50)
    ) AS total_top50,
    (SELECT SUM("val_vendido") FROM "matriz_bcg") AS total_general,
    ROUND(
        100.0 * (SELECT SUM("val_vendido") 
                  FROM (SELECT "val_vendido" FROM "matriz_bcg" ORDER BY "val_vendido" DESC LIMIT 50))
        / (SELECT SUM("val_vendido") FROM "matriz_bcg")
    , 2) AS porcentaje;