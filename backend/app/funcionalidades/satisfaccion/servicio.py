from math import sqrt

from sqlalchemy import func
from sqlmodel import Session

from app.nucleo.consultas import compras_con_detalle, filas, redondear
from app.nucleo.modelos import Compra, Producto


class SatisfaccionServicio:
    def __init__(self, sesion: Session):
        self._sesion = sesion

    def por_producto(self) -> list[dict]:
        """Productos de peor a mejor calificación, con margen de error al 95%."""
        productos = filas(self._sesion, compras_con_detalle(
            Producto.nombre.label("producto"),
            Producto.categoria,
            func.count(Compra.id).label("compras"),
            func.avg(Compra.calificacion).label("calificacion"),
            func.stddev_samp(Compra.calificacion).label("desviacion"),
        ).group_by(Producto.nombre, Producto.categoria))
        for p in productos:
            p["calificacion"] = redondear(p["calificacion"], 2)
            # margen = 1.96 · σ / √n
            p["margen_error_95"] = round(1.96 * p["desviacion"] / sqrt(p["compras"]), 2)
            del p["desviacion"]
        return sorted(productos, key=lambda p: (p["calificacion"], -p["compras"]))
