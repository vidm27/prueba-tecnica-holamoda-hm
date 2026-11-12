from fastapi import APIRouter, Depends
from sqlalchemy import Connection

from app.funcionalidades.suscripcion.esquemas import ImpactoSuscripcion
from app.nucleo.db import filas, obtener_conexion
from app.nucleo.sql import UNIONES

router = APIRouter(tags=["Suscripción"])


@router.get("/suscripcion/impacto", response_model=list[ImpactoSuscripcion],
            summary="¿Vale la pena la suscripción?")
def impacto_suscripcion(con: Connection = Depends(obtener_conexion)):
    return filas(con, f"""
        SELECT cl.suscrito, count(*) AS clientes,
               round(avg(c.monto_usd)::numeric, 2) AS ticket_promedio,
               round(avg(cl.compras_previas)::numeric, 1) AS compras_previas_promedio,
               round(avg(c.calificacion)::numeric, 2) AS calificacion_promedio,
               round(avg(cl.gasto_anual_estimado)::numeric, 2) AS gasto_anual_promedio
        {UNIONES} GROUP BY cl.suscrito ORDER BY cl.suscrito""")
