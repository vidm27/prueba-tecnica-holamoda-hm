from typing import Literal

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.funcionalidades.envios.esquemas import EnvioSegmento
from app.funcionalidades.envios.servicio import EnviosServicio
from app.nucleo.db import obtener_sesion

router = APIRouter(tags=["Envíos"])


def obtener_servicio(sesion: Session = Depends(obtener_sesion)) -> EnviosServicio:
    return EnviosServicio(sesion)


@router.get("/envios/por-segmento", response_model=list[EnvioSegmento],
            summary="Tipo de envío por segmento de clientes")
def envios_por_segmento(
    segmento: Literal["nivel_valor", "grupo_edad", "genero"] = "nivel_valor",
    servicio: EnviosServicio = Depends(obtener_servicio),
):
    return servicio.por_segmento(segmento)
