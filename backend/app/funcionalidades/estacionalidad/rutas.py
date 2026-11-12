from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.funcionalidades.estacionalidad.esquemas import Estacionalidad
from app.funcionalidades.estacionalidad.servicio import EstacionalidadServicio
from app.nucleo.db import obtener_sesion

router = APIRouter(tags=["Estacionalidad"])


def obtener_servicio(sesion: Session = Depends(obtener_sesion)) -> EstacionalidadServicio:
    return EstacionalidadServicio(sesion)


@router.get("/productos/estacionalidad", response_model=list[Estacionalidad],
            summary="Temporada pico y valle de cada producto")
def estacionalidad(servicio: EstacionalidadServicio = Depends(obtener_servicio)):
    return servicio.por_producto()
