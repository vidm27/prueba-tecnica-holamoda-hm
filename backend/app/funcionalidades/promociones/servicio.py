from statistics import median

from sqlalchemy import case, desc, func, not_
from sqlmodel import Session

from app.nucleo.consultas import compras_con_detalle, filas, redondear
from app.nucleo.modelos import Cliente, Compra, Producto

ADVERTENCIA = "Sin fecha de compra no se puede medir el efecto del descuento sobre el volumen de ventas."


def recomendar(producto: dict, mediana_ventas: float, mediana_calificacion: float) -> tuple[str, str]:
    """Cruza volumen y calificación frente a la mediana de los productos."""
    vende_poco = producto["ventas"] < mediana_ventas
    bien_calificado = producto["calificacion"] >= mediana_calificacion
    if vende_poco and bien_calificado:
        return "promocion_exposicion", "Bien calificado pero se vende poco: falta visibilidad, no precio."
    if vende_poco:
        return "revisar_producto", "Se vende poco y está mal calificado: descontar no resuelve el problema."
    if not bien_calificado:
        return "riesgo_reputacion", "Se vende mucho pero está mal calificado."
    return "mantener", "Buen volumen y buena calificación."


class PromocionesServicio:
    def __init__(self, sesion: Session):
        self._sesion = sesion

    def obtener(self) -> dict:
        productos = filas(self._sesion, compras_con_detalle(
            Producto.nombre.label("producto"),
            Producto.categoria,
            func.count(Compra.id).label("ventas"),
            func.avg(Compra.calificacion).label("calificacion"),
            func.avg(case((Compra.descuento, 1), else_=0)).label("pct_descuento"),
            func.avg(case((Cliente.genero == "Female", 1), else_=0)).label("pct_mujeres"),
            func.avg(Compra.monto_usd).filter(Compra.descuento).label("ticket_con_descuento"),
            func.avg(Compra.monto_usd).filter(not_(Compra.descuento)).label("ticket_sin_descuento"),
        ).group_by(Producto.nombre, Producto.categoria)
          .order_by(func.count(Compra.id), desc(func.avg(Compra.calificacion))))

        for p in productos:
            p["calificacion"] = redondear(p["calificacion"], 2)
            p["pct_descuento"] = redondear(p["pct_descuento"], 3)
            p["pct_mujeres"] = redondear(p["pct_mujeres"], 3)
            p["ticket_con_descuento"] = redondear(p["ticket_con_descuento"], 2)
            p["ticket_sin_descuento"] = redondear(p["ticket_sin_descuento"], 2)

        mediana_ventas = median(p["ventas"] for p in productos)
        mediana_calificacion = float(median(p["calificacion"] for p in productos))
        for p in productos:
            p["recomendacion"], p["motivo"] = recomendar(p, mediana_ventas, mediana_calificacion)

        mujeres_con_descuento = self._sesion.scalar(
            compras_con_detalle(func.count(Compra.id)).where(Cliente.genero == "Female", Compra.descuento))
        return {
            "mediana_ventas": mediana_ventas,
            "mediana_calificacion": mediana_calificacion,
            "compras_mujeres_con_descuento": mujeres_con_descuento,
            "advertencia": ADVERTENCIA,
            "productos": productos,
        }
