from fastapi import APIRouter, Depends

from app.funcionalidades.satisfaccion.esquemas import Satisfaccion
from app.funcionalidades.satisfaccion.servicio import SatisfaccionServicio
from app.funcionalidades.satisfaccion.dependencias import obtener_servicio
from app.nucleo.respuestas import ERRORES

router = APIRouter(responses=ERRORES, tags=["Satisfacción"])


@router.get("/productos/satisfaccion", response_model=list[Satisfaccion],
            summary="Productos ordenados por calificación (peor primero)")
def satisfaccion(servicio: SatisfaccionServicio = Depends(obtener_servicio)):
    """Productos de peor a mejor calificación. `margen_error_95` es el margen al 95 %: si es grande, la muestra es pequeña."""
    return servicio.por_producto()
