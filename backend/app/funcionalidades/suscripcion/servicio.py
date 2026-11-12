from sqlalchemy import func
from sqlmodel import Session

from app.nucleo.consultas import compras_con_detalle, filas, redondear
from app.nucleo.modelos import Cliente, Compra


class SuscripcionServicio:
    def __init__(self, sesion: Session):
        self._sesion = sesion

    def impacto(self) -> list[dict]:
        """Compara suscritos y no suscritos: ticket, historial, calificación y gasto anual."""
        filas_suscripcion = filas(self._sesion, compras_con_detalle(
            Cliente.suscrito,
            func.count(Compra.id).label("clientes"),
            func.avg(Compra.monto_usd).label("ticket_promedio"),
            func.avg(Cliente.compras_previas).label("compras_previas_promedio"),
            func.avg(Compra.calificacion).label("calificacion_promedio"),
            func.avg(Cliente.gasto_anual_estimado).label("gasto_anual_promedio"),
        ).group_by(Cliente.suscrito).order_by(Cliente.suscrito))
        for f in filas_suscripcion:
            f["ticket_promedio"] = redondear(f["ticket_promedio"], 2)
            f["compras_previas_promedio"] = redondear(f["compras_previas_promedio"], 1)
            f["calificacion_promedio"] = redondear(f["calificacion_promedio"], 2)
            f["gasto_anual_promedio"] = redondear(f["gasto_anual_promedio"], 2)
        return filas_suscripcion
