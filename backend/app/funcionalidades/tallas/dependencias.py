from fastapi import Depends
from sqlmodel import Session

from app.funcionalidades.tallas.servicio import TallasServicio
from app.nucleo.db import obtener_sesion


def obtener_servicio(sesion: Session = Depends(obtener_sesion)) -> TallasServicio:
    return TallasServicio(sesion)
