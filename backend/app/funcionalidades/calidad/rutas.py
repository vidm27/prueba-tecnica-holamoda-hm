from fastapi import APIRouter, Depends
from sqlalchemy import Connection

from app.funcionalidades.calidad.esquemas import Hallazgo
from app.nucleo.db import filas, obtener_conexion

router = APIRouter(tags=["Calidad de datos"])


@router.get("/calidad/auditoria", response_model=list[Hallazgo],
            summary="Hallazgos de calidad detectados por el ETL")
def auditoria(con: Connection = Depends(obtener_conexion)):
    return filas(con, """
        SELECT regla, descripcion, severidad, filas_afectadas, total_filas, evidencia
        FROM auditoria ORDER BY CASE severidad WHEN 'alta' THEN 0 WHEN 'media' THEN 1 ELSE 2 END, id""")
