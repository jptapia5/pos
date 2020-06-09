SELECT * FROM mydb.ventas WHERE folioBoleta = 0 AND idMedioPago = 0;
SELECT * FROM mydb.ventas WHERE idVenta = 64;

-- ***********************************    ELIMINACIÓN RECURSIVA   ****************************************************
DELETE d FROM mydb.detalle_venta d INNER JOIN mydb.ventas v ON d.idVenta = v.idVenta WHERE v.folioBoleta = 0 AND v.idMedioPago = 0;
DELETE FROM mydb.ventas WHERE idVenta = 64; 


DELETE p FROM mydb.detalle_venta d 
INNER JOIN mydb.productos p 
ON d.idProducto = v.idProducto 
WHERE d.idProducto = 0;