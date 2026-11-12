from typing import Literal

from fastapi import APIRouter, Depends

from app.funcionalidades.envios.esquemas import EnvioSegmento
from app.funcionalidades.envios.servicio import EnviosServicio
from app.funcionalidades.envios.dependencias import obtener_servicio
from app.nucleo.respuestas import ERRORES

router = APIRouter(responses=ERRORES, tags=["Envíos"])


@router.get("/envios/por-segmento", response_model=list[EnvioSegmento],
            summary="Tipo de envío por segmento de clientes")
def envios_por_segmento(
    segmento: Literal["nivel_valor", "grupo_edad", "genero"] = "nivel_valor",
    servicio: EnviosServicio = Depends(obtener_servicio),
):
    return servicio.por_segmento(segmento)
