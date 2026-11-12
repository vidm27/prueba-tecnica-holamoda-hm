from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.funcionalidades.resumen.esquemas import Resumen
from app.funcionalidades.resumen.servicio import ResumenServicio
from app.nucleo.db import obtener_sesion

router = APIRouter(tags=["Resumen"])


def obtener_servicio(sesion: Session = Depends(obtener_sesion)) -> ResumenServicio:
    return ResumenServicio(sesion)


@router.get("/resumen", response_model=Resumen, summary="Indicadores generales")
def resumen(servicio: ResumenServicio = Depends(obtener_servicio)):
    return servicio.obtener()
