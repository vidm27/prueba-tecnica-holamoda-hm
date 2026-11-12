from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.funcionalidades.tallas.esquemas import CurvaTalla
from app.funcionalidades.tallas.servicio import TallasServicio
from app.nucleo.db import obtener_sesion

router = APIRouter(tags=["Tallas"])


def obtener_servicio(sesion: Session = Depends(obtener_sesion)) -> TallasServicio:
    return TallasServicio(sesion)


@router.get("/tallas/curva", response_model=list[CurvaTalla], summary="Curva de tallas por categoría")
def curva_tallas(categoria: str | None = None, servicio: TallasServicio = Depends(obtener_servicio)):
    return servicio.curva(categoria)
