from typing import Literal

from fastapi import APIRouter, Depends, Query

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
def probar_hipotesis(metrica: Metrica = Query(..., description="Métrica a comparar: monto en USD o calificación", examples=["monto_usd"]),
                     variable: Variable = Query(..., description="Variable que define los grupos", examples=["temporada"]),
                     servicio: HipotesisServicio = Depends(obtener_servicio)):
    """Prueba si la métrica cambia según la variable, con Kruskal-Wallis.

    `p_ajustado` corrige por todas las comparaciones posibles. Si es mayor o igual a 0.05, la diferencia no es confiable.
    Responde `422 datos_insuficientes` si no hay variación suficiente para comparar los grupos."""
    return servicio.probar(metrica, variable)
