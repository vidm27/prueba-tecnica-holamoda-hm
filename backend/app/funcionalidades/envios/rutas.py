from typing import Literal

from fastapi import APIRouter, Depends
from sqlalchemy import Connection

from app.funcionalidades.envios.esquemas import EnvioSegmento
from app.nucleo.db import filas, obtener_conexion
from app.nucleo.sql import UNIONES

router = APIRouter(tags=["Envíos"])


@router.get("/envios/por-segmento", response_model=list[EnvioSegmento],
            summary="Tipo de envío por segmento de clientes")
def envios_por_segmento(segmento: Literal["nivel_valor", "grupo_edad", "genero"] = "nivel_valor",
                        con: Connection = Depends(obtener_conexion)):
    # `segmento` es un Literal validado por FastAPI: es seguro interpolarlo como nombre de columna.
    return filas(con, f"""
        SELECT cl.{segmento} AS segmento, c.tipo_envio, count(*) AS compras,
               round((100.0 * count(*) / sum(count(*)) OVER (PARTITION BY cl.{segmento}))::numeric, 1) AS pct_segmento
        {UNIONES} GROUP BY 1, 2 ORDER BY 1, pct_segmento DESC""")
