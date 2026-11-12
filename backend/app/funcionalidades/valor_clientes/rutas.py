from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.funcionalidades.valor_clientes.esquemas import Valor
from app.funcionalidades.valor_clientes.servicio import ValorClientesServicio
from app.nucleo.db import obtener_sesion

router = APIRouter(tags=["Valor de clientes"])


def obtener_servicio(sesion: Session = Depends(obtener_sesion)) -> ValorClientesServicio:
    return ValorClientesServicio(sesion)


@router.get("/clientes/valor", response_model=Valor, summary="Segmentación de clientes por valor")
def valor_clientes(servicio: ValorClientesServicio = Depends(obtener_servicio)):
    return servicio.segmentacion()
