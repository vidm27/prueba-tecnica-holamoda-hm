from sqlalchemy import case, select
from sqlmodel import Session

from app.nucleo.modelos import HallazgoAuditoria


class CalidadServicio:
    def __init__(self, sesion: Session):
        self._sesion = sesion

    def hallazgos(self) -> list[HallazgoAuditoria]:
        """Hallazgos del ETL, de mayor a menor severidad."""
        orden = case({"alta": 0, "media": 1}, value=HallazgoAuditoria.severidad, else_=2)
        return list(self._sesion.scalars(select(HallazgoAuditoria).order_by(orden, HallazgoAuditoria.id)))
