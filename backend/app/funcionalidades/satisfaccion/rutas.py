from fastapi import APIRouter, Depends

from app.funcionalidades.satisfaccion.esquemas import Satisfaccion
from app.funcionalidades.satisfaccion.servicio import SatisfaccionServicio
from app.funcionalidades.satisfaccion.dependencias import obtener_servicio

router = APIRouter(tags=["Satisfacción"])


@router.get("/productos/satisfaccion", response_model=list[Satisfaccion],
            summary="Productos ordenados por calificación (peor primero)")
def satisfaccion(servicio: SatisfaccionServicio = Depends(obtener_servicio)):
    return servicio.por_producto()
