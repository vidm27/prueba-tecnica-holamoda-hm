from fastapi import Depends
from sqlmodel import Session

from app.funcionalidades.suscripcion.servicio import SuscripcionServicio
from app.nucleo.db import obtener_sesion


def obtener_servicio(sesion: Session = Depends(obtener_sesion)) -> SuscripcionServicio:
    return SuscripcionServicio(sesion)
