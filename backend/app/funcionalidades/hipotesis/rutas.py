from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.funcionalidades.hipotesis.esquemas import ResultadoHipotesis
from app.funcionalidades.hipotesis.servicio import DatosInsuficientes, HipotesisServicio
from app.nucleo.db import obtener_sesion

router = APIRouter(tags=["Hipótesis"])

Metrica = Literal["monto_usd", "calificacion"]
Variable = Literal["genero", "suscrito", "grupo_edad", "estado", "nivel_valor", "frecuencia", "categoria",
                   "producto", "talla", "color", "temporada", "tipo_envio", "metodo_pago", "descuento"]


def obtener_servicio(sesion: Session = Depends(obtener_sesion)) -> HipotesisServicio:
    return HipotesisServicio(sesion)


@router.get("/hipotesis", response_model=ResultadoHipotesis,
            summary="¿Cambia la métrica según la variable? (Kruskal-Wallis con corrección)")
def probar_hipotesis(metrica: Metrica, variable: Variable,
                     servicio: HipotesisServicio = Depends(obtener_servicio)):
    try:
        return servicio.probar(metrica, variable)
    except DatosInsuficientes:
        raise HTTPException(422, "No hay variación suficiente para comparar los grupos")
