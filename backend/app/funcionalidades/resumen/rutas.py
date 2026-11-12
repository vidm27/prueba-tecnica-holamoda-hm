from fastapi import APIRouter, Depends

from app.funcionalidades.resumen.esquemas import Resumen
from app.funcionalidades.resumen.servicio import ResumenServicio
from app.funcionalidades.resumen.dependencias import obtener_servicio
from app.nucleo.respuestas import ERRORES

router = APIRouter(responses=ERRORES, tags=["Resumen"])


@router.get("/resumen", response_model=Resumen, summary="Indicadores generales")
def resumen(servicio: ResumenServicio = Depends(obtener_servicio)):
    """Indicadores generales: compras, clientes, productos, ingreso total, ticket promedio y calificación promedio."""
    return servicio.obtener()
