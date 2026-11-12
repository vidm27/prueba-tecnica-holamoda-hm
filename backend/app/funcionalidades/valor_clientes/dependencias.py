from fastapi import Depends
from sqlmodel import Session

from app.funcionalidades.valor_clientes.servicio import ValorClientesServicio
from app.nucleo.db import obtener_sesion


def obtener_servicio(sesion: Session = Depends(obtener_sesion)) -> ValorClientesServicio:
    return ValorClientesServicio(sesion)
