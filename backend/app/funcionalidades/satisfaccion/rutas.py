from fastapi import APIRouter, Depends
from sqlalchemy import Connection

from app.funcionalidades.satisfaccion.esquemas import Satisfaccion
from app.nucleo.db import filas, obtener_conexion

router = APIRouter(tags=["Satisfacción"])


@router.get("/productos/satisfaccion", response_model=list[Satisfaccion],
            summary="Productos ordenados por calificación (peor primero)")
def satisfaccion(con: Connection = Depends(obtener_conexion)):
    return filas(con, """
        SELECT p.nombre AS producto, p.categoria, count(*) AS compras,
               round(avg(c.calificacion)::numeric, 2) AS calificacion,
               round((1.96 * stddev_samp(c.calificacion) / sqrt(count(*)))::numeric, 2) AS margen_error_95
        FROM compras c JOIN productos p ON p.id = c.producto_id
        GROUP BY p.nombre, p.categoria ORDER BY calificacion, compras DESC""")
