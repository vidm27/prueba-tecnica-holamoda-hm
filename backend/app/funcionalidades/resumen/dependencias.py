from fastapi import Depends
from sqlmodel import Session

from app.funcionalidades.resumen.servicio import ResumenServicio
from app.nucleo.db import obtener_sesion


def obtener_servicio(sesion: Session = Depends(obtener_sesion)) -> ResumenServicio:
    return ResumenServicio(sesion)
