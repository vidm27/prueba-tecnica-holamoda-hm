from fastapi import APIRouter, Depends

from app.funcionalidades.valor_clientes.esquemas import Valor
from app.funcionalidades.valor_clientes.servicio import ValorClientesServicio
from app.funcionalidades.valor_clientes.dependencias import obtener_servicio
from app.nucleo.respuestas import ERRORES

router = APIRouter(responses=ERRORES, tags=["Valor de clientes"])


@router.get("/clientes/valor", response_model=Valor, summary="Segmentación de clientes por valor")
def valor_clientes(servicio: ValorClientesServicio = Depends(obtener_servicio)):
    return servicio.segmentacion()
