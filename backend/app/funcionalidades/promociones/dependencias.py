from fastapi import Depends
from sqlmodel import Session

from app.funcionalidades.promociones.servicio import PromocionesServicio
from app.nucleo.db import obtener_sesion


def obtener_servicio(sesion: Session = Depends(obtener_sesion)) -> PromocionesServicio:
    return PromocionesServicio(sesion)
