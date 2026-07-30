-- 1. ¿Cuáles son los 20 productos más vendidos (por unidades)?
SELECT "producto", "laboratorio", "unid_vendidas", "val_vendido"
FROM "matriz_bcg"
ORDER BY "unid_vendidas" DESC
LIMIT 20;

-- 2. ¿Qué productos casi no se venden (menos unidades)?
SELECT "producto", "laboratorio", "unid_vendidas", "val_vendido"
FROM "matriz_bcg"
ORDER BY "unid_vendidas" ASC
LIMIT 20;