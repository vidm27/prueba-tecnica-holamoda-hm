from fastapi import APIRouter, Depends, Query

from app.funcionalidades.tallas.esquemas import CurvaTalla
from app.funcionalidades.tallas.servicio import TallasServicio
from app.funcionalidades.tallas.dependencias import obtener_servicio
from app.nucleo.respuestas import ERRORES

router = APIRouter(responses=ERRORES, tags=["Tallas"])


@router.get("/tallas/curva", response_model=list[CurvaTalla], summary="Curva de tallas por categoría")
def curva_tallas(categoria: str | None = Query(None, description="Categoría a consultar; sin valor, devuelve todas", examples=["Clothing"]), servicio: TallasServicio = Depends(obtener_servicio)):
    """Porcentaje de compras por talla dentro de cada categoría. Sirve para decidir el inventario por talla."""
    return servicio.curva(categoria)
