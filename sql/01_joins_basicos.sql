--  Pregunta: ¿Cual es el detalle de cada venta especial, mostrando
-- el nombre real del vendedor en vez de su ID?
SELECT  ve.fecha, ve.producto, ve.valor_base, v.nombre_vendedor
FROM ventas_especiales ve
JOIN vendedores v ON ve.id_vendedor = v.id_vendedor;
