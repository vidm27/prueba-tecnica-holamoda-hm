"""Piezas reutilizables de consulta sobre el modelo de compras (SQLAlchemy ORM)."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.nucleo.modelos import Cliente, Compra, Producto


def compras_con_detalle(*columnas):
    """SELECT de columnas sobre compras, unido a su producto y a su cliente.

    Es la base de casi todas las consultas analíticas: cada análisis solo
    decide qué columnas agrupa, filtra y agrega.
    """
    return (
        select(*columnas)
        .select_from(Compra)
        .join(Producto, Producto.id == Compra.producto_id)
        .join(Cliente, Cliente.id == Compra.cliente_id)
    )


def filas(sesion: Session, consulta) -> list[dict]:
    """Ejecuta una consulta y devuelve cada fila como diccionario."""
    return [dict(fila) for fila in sesion.execute(consulta).mappings()]


def redondear(valor: float | None, decimales: int) -> float | None:
    return None if valor is None else round(float(valor), decimales)
