from fastapi import APIRouter, Depends

from app.funcionalidades.valor_clientes.esquemas import Valor
from app.funcionalidades.valor_clientes.servicio import ValorClientesServicio
from app.funcionalidades.valor_clientes.dependencias import obtener_servicio
from app.nucleo.respuestas import ERRORES

router = APIRouter(responses=ERRORES, tags=["Valor de clientes"])


@router.get("/clientes/valor", response_model=Valor, summary="Segmentación de clientes por valor")
def valor_clientes(servicio: ValorClientesServicio = Depends(obtener_servicio)):
    """Segmenta a los clientes en Bronce, Plata, Oro y Platino según su gasto anual estimado.

    `pareto_top20_pct_gasto` es el porcentaje del gasto que aporta el 20 % de clientes con más gasto."""
    return servicio.segmentacion()
