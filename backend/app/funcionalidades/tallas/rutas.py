from fastapi import APIRouter, Depends
from sqlalchemy import Connection

from app.funcionalidades.tallas.esquemas import CurvaTalla
from app.nucleo.db import filas, obtener_conexion

router = APIRouter(tags=["Tallas"])


@router.get("/tallas/curva", response_model=list[CurvaTalla], summary="Curva de tallas por categoría")
def curva_tallas(categoria: str | None = None, con: Connection = Depends(obtener_conexion)):
    return filas(con, """
        SELECT p.categoria, c.talla, count(*) AS compras,
               round((100.0 * count(*) / sum(count(*)) OVER (PARTITION BY p.categoria))::numeric, 1) AS pct
        FROM compras c JOIN productos p ON p.id = c.producto_id
        WHERE CAST(:categoria AS text) IS NULL OR p.categoria = :categoria
        GROUP BY p.categoria, c.talla ORDER BY p.categoria, pct DESC""", categoria=categoria)
