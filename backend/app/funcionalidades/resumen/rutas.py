from fastapi import APIRouter, Depends

from app.funcionalidades.resumen.esquemas import Resumen
from app.funcionalidades.resumen.servicio import ResumenServicio
from app.funcionalidades.resumen.dependencias import obtener_servicio

router = APIRouter(tags=["Resumen"])


@router.get("/resumen", response_model=Resumen, summary="Indicadores generales")
def resumen(servicio: ResumenServicio = Depends(obtener_servicio)):
    return servicio.obtener()
