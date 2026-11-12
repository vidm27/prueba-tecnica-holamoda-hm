from fastapi import APIRouter, Depends, Query
from sqlalchemy import Connection

from app.funcionalidades.compras.esquemas import PaginaCompras
from app.nucleo.db import filas, obtener_conexion
from app.nucleo.sql import UNIONES

router = APIRouter(tags=["Compras"])

FILTROS = """
    WHERE (CAST(:categoria AS text) IS NULL OR p.categoria = :categoria)
      AND (CAST(:genero AS text) IS NULL OR cl.genero = :genero)
      AND (CAST(:temporada AS text) IS NULL OR c.temporada = :temporada)
      AND (CAST(:estado AS text) IS NULL OR cl.ubicacion = :estado)"""


@router.get("/compras", response_model=PaginaCompras, summary="Listado paginado de compras con filtros")
def listar_compras(categoria: str | None = None, genero: str | None = None,
                   temporada: str | None = None, estado: str | None = None,
                   limite: int = Query(50, ge=1, le=200), desplazamiento: int = Query(0, ge=0),
                   con: Connection = Depends(obtener_conexion)):
    filtros = dict(categoria=categoria, genero=genero, temporada=temporada, estado=estado)
    total = filas(con, f"SELECT count(*) AS n {UNIONES} {FILTROS}", **filtros)[0]["n"]
    items = filas(con, f"""
        SELECT c.id, p.nombre AS producto, p.categoria, cl.genero, cl.edad, cl.ubicacion AS estado,
               c.monto_usd, c.talla, c.color, c.temporada, c.calificacion, c.tipo_envio,
               c.descuento, c.metodo_pago, cl.nivel_valor
        {UNIONES} {FILTROS} ORDER BY c.id LIMIT :limite OFFSET :desplazamiento""",
                  **filtros, limite=limite, desplazamiento=desplazamiento)
    return {"total": total, "limite": limite, "desplazamiento": desplazamiento, "items": items}
