from typing import Literal

from fastapi import APIRouter, Depends

from app.funcionalidades.hipotesis.esquemas import ResultadoHipotesis
from app.funcionalidades.hipotesis.servicio import HipotesisServicio
from app.funcionalidades.hipotesis.dependencias import obtener_servicio
from app.nucleo.respuestas import ERRORES

router = APIRouter(responses=ERRORES, tags=["Hipótesis"])

Metrica = Literal["monto_usd", "calificacion"]
Variable = Literal["genero", "suscrito", "grupo_edad", "estado", "nivel_valor", "frecuencia", "categoria",
                   "producto", "talla", "color", "temporada", "tipo_envio", "metodo_pago", "descuento"]


@router.get("/hipotesis", response_model=ResultadoHipotesis,
            summary="¿Cambia la métrica según la variable? (Kruskal-Wallis con corrección)")
def probar_hipotesis(metrica: Metrica, variable: Variable,
                     servicio: HipotesisServicio = Depends(obtener_servicio)):
    return servicio.probar(metrica, variable)
