from typing import Literal

from fastapi import APIRouter, Depends, Query

from app.funcionalidades.promociones.esquemas import Promociones
from app.funcionalidades.promociones.servicio import PromocionesServicio
from app.funcionalidades.promociones.dependencias import obtener_servicio
from app.nucleo.respuestas import ERRORES

router = APIRouter(responses=ERRORES, tags=["Promociones"])


@router.get("/productos/promocion", response_model=Promociones,
            summary="¿De qué producto lanzar una promoción?")
def promociones(
    genero: Literal["Female", "Male"] | None = Query(
        None, description="Filtra las compras por género para recalcular las oportunidades de ese segmento."),
    servicio: PromocionesServicio = Depends(obtener_servicio),
):
    return servicio.obtener(genero)
