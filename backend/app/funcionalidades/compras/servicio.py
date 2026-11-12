from sqlalchemy import func
from sqlmodel import Session

from app.nucleo.consultas import compras_con_detalle, filas
from app.nucleo.modelos import Cliente, Compra, Producto


def _filtrar(consulta, categoria, genero, temporada, estado):
    if categoria is not None:
        consulta = consulta.where(Producto.categoria == categoria)
    if genero is not None:
        consulta = consulta.where(Cliente.genero == genero)
    if temporada is not None:
        consulta = consulta.where(Compra.temporada == temporada)
    if estado is not None:
        consulta = consulta.where(Cliente.ubicacion == estado)
    return consulta


class ComprasServicio:
    def __init__(self, sesion: Session):
        self._sesion = sesion

    def listar(self, *, categoria, genero, temporada, estado, limite: int, desplazamiento: int) -> dict:
        filtros = dict(categoria=categoria, genero=genero, temporada=temporada, estado=estado)
        total = self._sesion.scalar(_filtrar(compras_con_detalle(func.count(Compra.id)), **filtros))
        items = filas(self._sesion, _filtrar(compras_con_detalle(
            Compra.id,
            Producto.nombre.label("producto"),
            Producto.categoria,
            Cliente.genero,
            Cliente.edad,
            Cliente.ubicacion.label("estado"),
            Compra.monto_usd,
            Compra.talla,
            Compra.color,
            Compra.temporada,
            Compra.calificacion,
            Compra.tipo_envio,
            Compra.descuento,
            Compra.metodo_pago,
            Cliente.nivel_valor,
        ), **filtros).order_by(Compra.id).limit(limite).offset(desplazamiento))
        return {"total": total, "limite": limite, "desplazamiento": desplazamiento, "items": items}
