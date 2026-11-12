from fastapi import APIRouter, Depends
from sqlalchemy import Connection

from app.funcionalidades.resumen.esquemas import Resumen
from app.nucleo.db import filas, obtener_conexion
from app.nucleo.sql import UNIONES

router = APIRouter(tags=["Resumen"])


@router.get("/resumen", response_model=Resumen, summary="Indicadores generales")
def resumen(con: Connection = Depends(obtener_conexion)):
    return filas(con, f"""
        SELECT count(*) AS compras,
               (SELECT count(*) FROM clientes) AS clientes,
               (SELECT count(*) FROM productos) AS productos,
               round(sum(c.monto_usd)::numeric, 2) AS ingreso_total,
               round(avg(c.monto_usd)::numeric, 2) AS ticket_promedio,
               round(avg(c.calificacion)::numeric, 2) AS calificacion_promedio
        {UNIONES}""")[0]
