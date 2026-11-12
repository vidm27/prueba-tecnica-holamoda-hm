from collections import defaultdict

from sqlalchemy import func
from sqlmodel import Session

from app.nucleo.consultas import compras_con_detalle, filas
from app.nucleo.modelos import Cliente, Compra, Producto

UBICACION = Cliente.ubicacion.label("estado")
NOMBRE = Producto.nombre.label("producto")


def _mayor(candidatos: list[tuple[str, int]]) -> tuple[str | None, int]:
    """Mayor conteo; ante empate, el nombre alfabéticamente primero (criterio estable)."""
    if not candidatos:
        return None, 0
    return min(candidatos, key=lambda c: (-c[1], c[0]))


def calcular_top_por_estado(productos: list[dict], tallas: list[dict], colores: list[dict],
                            min_muestra: int) -> list[dict]:
    """Producto líder por estado, con su talla y color más comunes.

    `muestra_suficiente` es falso si el producto tiene menos de `min_muestra`
    ventas o si hay empate: así no se sobreinterpretan conteos pequeños.
    """
    por_estado = defaultdict(list)
    for r in productos:
        por_estado[r["estado"]].append((r["producto"], r["n"]))
    tallas_por = defaultdict(list)
    for r in tallas:
        tallas_por[(r["estado"], r["producto"])].append((r["talla"], r["n"]))
    colores_por = defaultdict(list)
    for r in colores:
        colores_por[(r["estado"], r["producto"])].append((r["color"], r["n"]))

    resultado = []
    for estado in sorted(por_estado):
        candidatos = por_estado[estado]
        producto, ventas = _mayor(candidatos)
        empatados = sum(1 for _, n in candidatos if n == ventas)
        talla, ventas_talla = _mayor(tallas_por[(estado, producto)])
        color, ventas_color = _mayor(colores_por[(estado, producto)])
        resultado.append({
            "estado": estado,
            "producto": producto,
            "ventas_producto": ventas,
            "ventas_estado": sum(n for _, n in candidatos),
            "productos_empatados": empatados,
            "talla": talla,
            "ventas_talla": ventas_talla,
            "color": color,
            "ventas_color": ventas_color,
            "muestra_suficiente": ventas >= min_muestra and empatados == 1,
        })
    return resultado


class EstadosServicio:
    def __init__(self, sesion: Session):
        self._sesion = sesion

    def top_productos(self, min_muestra: int) -> list[dict]:
        productos = filas(self._sesion, compras_con_detalle(
            UBICACION, NOMBRE, func.count(Compra.id).label("n"),
        ).group_by(Cliente.ubicacion, Producto.nombre))
        tallas = filas(self._sesion, compras_con_detalle(
            UBICACION, NOMBRE, Compra.talla, func.count(Compra.id).label("n"),
        ).group_by(Cliente.ubicacion, Producto.nombre, Compra.talla))
        colores = filas(self._sesion, compras_con_detalle(
            UBICACION, NOMBRE, Compra.color, func.count(Compra.id).label("n"),
        ).group_by(Cliente.ubicacion, Producto.nombre, Compra.color))
        return calcular_top_por_estado(productos, tallas, colores, min_muestra)
