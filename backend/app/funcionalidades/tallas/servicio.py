from collections import Counter

from sqlalchemy import func
from sqlmodel import Session

from app.nucleo.consultas import compras_con_detalle, filas
from app.nucleo.modelos import Compra, Producto


class TallasServicio:
    def __init__(self, sesion: Session):
        self._sesion = sesion

    def curva(self, categoria: str | None) -> list[dict]:
        """Distribución porcentual de tallas dentro de cada categoría."""
        consulta = compras_con_detalle(
            Producto.categoria, Compra.talla, func.count(Compra.id).label("compras"),
        ).group_by(Producto.categoria, Compra.talla)
        if categoria is not None:
            consulta = consulta.where(Producto.categoria == categoria)
        filas_tallas = filas(self._sesion, consulta)

        total_por_categoria = Counter()
        for f in filas_tallas:
            total_por_categoria[f["categoria"]] += f["compras"]
        for f in filas_tallas:
            f["pct"] = round(100.0 * f["compras"] / total_por_categoria[f["categoria"]], 1)
        return sorted(filas_tallas, key=lambda f: (f["categoria"], -f["pct"], f["talla"]))
