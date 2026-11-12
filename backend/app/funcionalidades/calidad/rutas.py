from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.funcionalidades.calidad.esquemas import Hallazgo
from app.funcionalidades.calidad.servicio import CalidadServicio
from app.nucleo.db import obtener_sesion

router = APIRouter(tags=["Calidad de datos"])


def obtener_servicio(sesion: Session = Depends(obtener_sesion)) -> CalidadServicio:
    return CalidadServicio(sesion)


@router.get("/calidad/auditoria", response_model=list[Hallazgo],
            summary="Hallazgos de calidad detectados por el ETL")
def auditoria(servicio: CalidadServicio = Depends(obtener_servicio)):
    return servicio.hallazgos()
