from fastapi import APIRouter, Depends, Query
from sqlalchemy import Connection

from app.funcionalidades.estados.esquemas import TopEstado
from app.nucleo.db import filas, obtener_conexion

router = APIRouter(tags=["Estados"])


@router.get("/estados/top-productos", response_model=list[TopEstado],
            summary="Producto más vendido por estado, con su talla y color más comunes")
def top_por_estado(min_muestra: int = Query(10, ge=1, description="Ventas mínimas del producto para considerar la muestra suficiente"),
                   con: Connection = Depends(obtener_conexion)):
    return filas(con, """
        WITH base AS (
            SELECT cl.ubicacion AS estado, p.nombre AS producto, c.talla, c.color
            FROM compras c JOIN productos p ON p.id = c.producto_id JOIN clientes cl ON cl.id = c.cliente_id),
        conteo AS (SELECT estado, producto, count(*) AS n FROM base GROUP BY estado, producto),
        orden AS (
            SELECT *, row_number() OVER (PARTITION BY estado ORDER BY n DESC, producto) AS pos,
                   count(*) OVER (PARTITION BY estado, n) AS empatados,
                   sum(n) OVER (PARTITION BY estado) AS total
            FROM conteo)
        SELECT o.estado, o.producto, o.n AS ventas_producto, o.total AS ventas_estado,
               o.empatados AS productos_empatados,
               t.talla, t.n AS ventas_talla, k.color, k.n AS ventas_color,
               (o.n >= :min_muestra AND o.empatados = 1) AS muestra_suficiente
        FROM orden o
        CROSS JOIN LATERAL (SELECT talla, count(*) AS n FROM base b
                            WHERE b.estado = o.estado AND b.producto = o.producto
                            GROUP BY talla ORDER BY n DESC, talla LIMIT 1) t
        CROSS JOIN LATERAL (SELECT color, count(*) AS n FROM base b
                            WHERE b.estado = o.estado AND b.producto = o.producto
                            GROUP BY color ORDER BY n DESC, color LIMIT 1) k
        WHERE o.pos = 1 ORDER BY o.estado""", min_muestra=min_muestra)
