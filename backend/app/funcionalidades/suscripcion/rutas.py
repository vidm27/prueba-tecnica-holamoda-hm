from fastapi import APIRouter, Depends

from app.funcionalidades.suscripcion.esquemas import ImpactoSuscripcion
from app.funcionalidades.suscripcion.servicio import SuscripcionServicio
from app.funcionalidades.suscripcion.dependencias import obtener_servicio
from app.nucleo.respuestas import ERRORES

router = APIRouter(responses=ERRORES, tags=["Suscripción"])


@router.get("/suscripcion/impacto", response_model=list[ImpactoSuscripcion],
            summary="¿Vale la pena la suscripción?")
def impacto_suscripcion(servicio: SuscripcionServicio = Depends(obtener_servicio)):
    """Compara suscritos y no suscritos: ticket, compras previas, calificación y gasto anual estimado."""
    return servicio.impacto()
