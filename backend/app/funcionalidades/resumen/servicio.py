from sqlalchemy import func, select
from sqlmodel import Session

from app.nucleo.modelos import Cliente, Compra, Producto
from app.nucleo.consultas import redondear


class ResumenServicio:
    def __init__(self, sesion: Session):
        self._sesion = sesion

    def obtener(self) -> dict:
        compras, ingreso, ticket, calificacion = self._sesion.execute(
            select(func.count(Compra.id), func.sum(Compra.monto_usd),
                   func.avg(Compra.monto_usd), func.avg(Compra.calificacion))
        ).one()
        return {
            "compras": compras,
            "clientes": self._sesion.scalar(select(func.count(Cliente.id))),
            "productos": self._sesion.scalar(select(func.count(Producto.id))),
            "ingreso_total": redondear(ingreso, 2),
            "ticket_promedio": redondear(ticket, 2),
            "calificacion_promedio": redondear(calificacion, 2),
        }
