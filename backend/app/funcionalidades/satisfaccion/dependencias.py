from fastapi import Depends
from sqlmodel import Session

from app.funcionalidades.satisfaccion.servicio import SatisfaccionServicio
from app.nucleo.db import obtener_sesion


def obtener_servicio(sesion: Session = Depends(obtener_sesion)) -> SatisfaccionServicio:
    return SatisfaccionServicio(sesion)
