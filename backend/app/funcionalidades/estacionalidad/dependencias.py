from fastapi import Depends
from sqlmodel import Session

from app.funcionalidades.estacionalidad.servicio import EstacionalidadServicio
from app.nucleo.db import obtener_sesion


def obtener_servicio(sesion: Session = Depends(obtener_sesion)) -> EstacionalidadServicio:
    return EstacionalidadServicio(sesion)
