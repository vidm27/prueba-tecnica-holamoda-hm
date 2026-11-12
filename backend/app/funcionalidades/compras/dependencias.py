from fastapi import Depends
from sqlmodel import Session

from app.funcionalidades.compras.servicio import ComprasServicio
from app.nucleo.db import obtener_sesion


def obtener_servicio(sesion: Session = Depends(obtener_sesion)) -> ComprasServicio:
    return ComprasServicio(sesion)
