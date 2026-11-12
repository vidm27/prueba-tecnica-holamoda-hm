# Uniones comunes: una fila por compra con su producto y su cliente.
UNIONES = "FROM compras c JOIN productos p ON p.id = c.producto_id JOIN clientes cl ON cl.id = c.cliente_id"
