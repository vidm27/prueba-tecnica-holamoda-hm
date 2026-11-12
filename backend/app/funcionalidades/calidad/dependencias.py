from fastapi import Depends
from sqlmodel import Session

from app.funcionalidades.calidad.servicio import CalidadServicio
from app.nucleo.db import obtener_sesion


def obtener_servicio(sesion: Session = Depends(obtener_sesion)) -> CalidadServicio:
    return CalidadServicio(sesion)
