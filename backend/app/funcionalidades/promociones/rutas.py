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
    """Clasifica cada producto cruzando sus ventas y su calificación con la mediana de todos.

    - `promocion_exposicion`: bien calificado pero se vende poco. Falta visibilidad, no precio.
    - `revisar_producto`: se vende poco y está mal calificado. Descontar no resuelve el problema.
    - `riesgo_reputacion`: se vende mucho pero está mal calificado.
    - `mantener`: buen volumen y buena calificación.

    `advertencia` recuerda que sin fechas no se mide el efecto de un descuento sobre las ventas."""
    return servicio.obtener(genero)
