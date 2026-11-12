from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.funcionalidades.satisfaccion.esquemas import Satisfaccion
from app.funcionalidades.satisfaccion.servicio import SatisfaccionServicio
from app.nucleo.db import obtener_sesion

router = APIRouter(tags=["Satisfacción"])


def obtener_servicio(sesion: Session = Depends(obtener_sesion)) -> SatisfaccionServicio:
    return SatisfaccionServicio(sesion)


@router.get("/productos/satisfaccion", response_model=list[Satisfaccion],
            summary="Productos ordenados por calificación (peor primero)")
def satisfaccion(servicio: SatisfaccionServicio = Depends(obtener_servicio)):
    return servicio.por_producto()
