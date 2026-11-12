from fastapi import APIRouter, Depends

from app.funcionalidades.promociones.esquemas import Promociones
from app.funcionalidades.promociones.servicio import PromocionesServicio
from app.funcionalidades.promociones.dependencias import obtener_servicio

router = APIRouter(tags=["Promociones"])


@router.get("/productos/promocion", response_model=Promociones,
            summary="¿De qué producto lanzar una promoción?")
def promociones(servicio: PromocionesServicio = Depends(obtener_servicio)):
    return servicio.obtener()
