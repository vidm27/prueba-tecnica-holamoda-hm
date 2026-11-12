from fastapi import APIRouter, Depends, Query

from app.funcionalidades.estados.esquemas import TopEstado
from app.funcionalidades.estados.servicio import EstadosServicio
from app.funcionalidades.estados.dependencias import obtener_servicio
from app.nucleo.respuestas import ERRORES

router = APIRouter(responses=ERRORES, tags=["Estados"])


@router.get("/estados/top-productos", response_model=list[TopEstado],
            summary="Producto más vendido por estado, con su talla y color más comunes")
def top_por_estado(
    min_muestra: int = Query(10, ge=1, description="Ventas mínimas para considerar la muestra suficiente"),
    servicio: EstadosServicio = Depends(obtener_servicio),
):
    return servicio.top_productos(min_muestra)
