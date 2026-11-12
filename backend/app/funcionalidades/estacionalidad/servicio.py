from collections import defaultdict

from sqlalchemy import func
from sqlmodel import Session

from app.nucleo.consultas import compras_con_detalle, filas
from app.nucleo.modelos import Compra, Producto


class EstacionalidadServicio:
    def __init__(self, sesion: Session):
        self._sesion = sesion

    def por_producto(self) -> list[dict]:
        """Ventas de cada producto por temporada, con su pico y su valle."""
        ventas = defaultdict(dict)
        for f in filas(self._sesion, compras_con_detalle(
            Producto.nombre.label("producto"), Compra.temporada, func.count(Compra.id).label("ventas"),
        ).group_by(Producto.nombre, Compra.temporada)):
            ventas[f["producto"]][f["temporada"]] = f["ventas"]
        return [
            {"producto": p, "ventas_por_temporada": v,
             "temporada_pico": max(v, key=v.get), "temporada_valle": min(v, key=v.get)}
            for p, v in sorted(ventas.items())
        ]
