-- Para cada laboratorio en matriz_bcg, ¿cuál es el producto más caro y el más barato que vende (precio_venta)?

SELECT "laboratorio", 
       MIN("precio_venta") AS precio_minimo,
       MAX("precio_venta") AS precio_maximo
FROM "matriz_bcg"
GROUP BY "laboratorio"
ORDER BY precio_maximo DESC
LIMIT 15;