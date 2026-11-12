from fastapi import APIRouter, Depends
from sqlalchemy import Connection

from app.funcionalidades.estacionalidad.esquemas import Estacionalidad
from app.nucleo.db import filas, obtener_conexion

router = APIRouter(tags=["Estacionalidad"])


@router.get("/productos/estacionalidad", response_model=list[Estacionalidad],
            summary="Temporada pico y valle de cada producto")
def estacionalidad(con: Connection = Depends(obtener_conexion)):
    por_producto: dict[str, dict[str, int]] = {}
    for f in filas(con, """
            SELECT p.nombre AS producto, c.temporada, count(*) AS ventas
            FROM compras c JOIN productos p ON p.id = c.producto_id GROUP BY 1, 2"""):
        por_producto.setdefault(f["producto"], {})[f["temporada"]] = f["ventas"]
    return [{"producto": p, "ventas_por_temporada": v,
             "temporada_pico": max(v, key=v.get), "temporada_valle": min(v, key=v.get)}
            for p, v in sorted(por_producto.items())]
