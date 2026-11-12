from fastapi import APIRouter, Depends

from app.funcionalidades.tallas.esquemas import CurvaTalla
from app.funcionalidades.tallas.servicio import TallasServicio
from app.funcionalidades.tallas.dependencias import obtener_servicio

router = APIRouter(tags=["Tallas"])


@router.get("/tallas/curva", response_model=list[CurvaTalla], summary="Curva de tallas por categoría")
def curva_tallas(categoria: str | None = None, servicio: TallasServicio = Depends(obtener_servicio)):
    return servicio.curva(categoria)
