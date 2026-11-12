from fastapi import APIRouter, Depends

from app.funcionalidades.calidad.esquemas import Hallazgo
from app.funcionalidades.calidad.servicio import CalidadServicio
from app.funcionalidades.calidad.dependencias import obtener_servicio
from app.nucleo.respuestas import ERRORES

router = APIRouter(responses=ERRORES, tags=["Calidad de datos"])


@router.get("/calidad/auditoria", response_model=list[Hallazgo],
            summary="Hallazgos de calidad detectados por el ETL")
def auditoria(servicio: CalidadServicio = Depends(obtener_servicio)):
    return servicio.hallazgos()
