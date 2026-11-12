from fastapi import APIRouter, Depends

from app.funcionalidades.suscripcion.esquemas import ImpactoSuscripcion
from app.funcionalidades.suscripcion.servicio import SuscripcionServicio
from app.funcionalidades.suscripcion.dependencias import obtener_servicio

router = APIRouter(tags=["Suscripción"])


@router.get("/suscripcion/impacto", response_model=list[ImpactoSuscripcion],
            summary="¿Vale la pena la suscripción?")
def impacto_suscripcion(servicio: SuscripcionServicio = Depends(obtener_servicio)):
    return servicio.impacto()
