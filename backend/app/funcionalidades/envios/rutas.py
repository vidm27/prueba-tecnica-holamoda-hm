from typing import Literal

from fastapi import APIRouter, Depends, Query

from app.funcionalidades.envios.esquemas import EnvioSegmento
from app.funcionalidades.envios.servicio import EnviosServicio
from app.funcionalidades.envios.dependencias import obtener_servicio
from app.nucleo.respuestas import ERRORES

router = APIRouter(responses=ERRORES, tags=["Envíos"])


@router.get("/envios/por-segmento", response_model=list[EnvioSegmento],
            summary="Tipo de envío por segmento de clientes")
def envios_por_segmento(
    segmento: Literal["nivel_valor", "grupo_edad", "genero"] = Query("nivel_valor", description="Segmento por el que se agrupan los clientes"),
    servicio: EnviosServicio = Depends(obtener_servicio),
):
    """Reparto de tipos de envío dentro de cada segmento: nivel de valor, grupo de edad o género."""
    return servicio.por_segmento(segmento)
