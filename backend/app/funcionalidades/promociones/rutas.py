from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.funcionalidades.promociones.esquemas import Promociones
from app.funcionalidades.promociones.servicio import PromocionesServicio
from app.nucleo.db import obtener_sesion

router = APIRouter(tags=["Promociones"])


def obtener_servicio(sesion: Session = Depends(obtener_sesion)) -> PromocionesServicio:
    return PromocionesServicio(sesion)


@router.get("/productos/promocion", response_model=Promociones,
            summary="¿De qué producto lanzar una promoción?")
def promociones(servicio: PromocionesServicio = Depends(obtener_servicio)):
    return servicio.obtener()
