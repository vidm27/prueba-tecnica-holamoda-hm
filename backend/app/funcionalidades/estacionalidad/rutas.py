from fastapi import APIRouter, Depends

from app.funcionalidades.estacionalidad.esquemas import Estacionalidad
from app.funcionalidades.estacionalidad.servicio import EstacionalidadServicio
from app.funcionalidades.estacionalidad.dependencias import obtener_servicio
from app.nucleo.respuestas import ERRORES

router = APIRouter(responses=ERRORES, tags=["Estacionalidad"])


@router.get("/productos/estacionalidad", response_model=list[Estacionalidad],
            summary="Temporada pico y valle de cada producto")
def estacionalidad(servicio: EstacionalidadServicio = Depends(obtener_servicio)):
    return servicio.por_producto()
