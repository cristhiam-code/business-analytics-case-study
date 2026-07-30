-- BUSQUEDAS CON LIKE EN PRODUCTOS ESPECIALES

-- 1. ¿Qué productos contienen "IBUPROFENO" en su descripción?
-- El % antes y después de la palabra busca coincidencias en cualquier parte del texto
SELECT "descripcion_completa", "laboratorio", "precio_venta"
FROM "productos_especiales"
WHERE "descripcion_completa" LIKE '%IBUPROFENO%'
ORDER BY "descripcion_completa";

-- 2. ¿Cuántas unidades y qué valor se ha vendido de un producto específico?
-- (cambiar 'MOUNJARO' por el producto que se quiera consultar)
SELECT "producto", "laboratorio", "unid_vendidas", "val_vendido"
FROM "matriz_bcg"
WHERE "producto" LIKE '%MOUNJARO%'
ORDER BY "val_vendido" DESC;