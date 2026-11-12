from fastapi import Depends
from sqlmodel import Session

from app.funcionalidades.hipotesis.servicio import HipotesisServicio
from app.nucleo.db import obtener_sesion


def obtener_servicio(sesion: Session = Depends(obtener_sesion)) -> HipotesisServicio:
    return HipotesisServicio(sesion)
