from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.funcionalidades.suscripcion.esquemas import ImpactoSuscripcion
from app.funcionalidades.suscripcion.servicio import SuscripcionServicio
from app.nucleo.db import obtener_sesion

router = APIRouter(tags=["Suscripción"])


def obtener_servicio(sesion: Session = Depends(obtener_sesion)) -> SuscripcionServicio:
    return SuscripcionServicio(sesion)


@router.get("/suscripcion/impacto", response_model=list[ImpactoSuscripcion],
            summary="¿Vale la pena la suscripción?")
def impacto_suscripcion(servicio: SuscripcionServicio = Depends(obtener_servicio)):
    return servicio.impacto()
