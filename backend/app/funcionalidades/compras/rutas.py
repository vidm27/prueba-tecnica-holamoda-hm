from fastapi import APIRouter, Depends, Query

from app.funcionalidades.compras.esquemas import PaginaCompras
from app.funcionalidades.compras.servicio import ComprasServicio
from app.funcionalidades.compras.dependencias import obtener_servicio

router = APIRouter(tags=["Compras"])


@router.get("/compras", response_model=PaginaCompras, summary="Listado paginado de compras con filtros")
def listar_compras(
    categoria: str | None = None,
    genero: str | None = None,
    temporada: str | None = None,
    estado: str | None = None,
    limite: int = Query(50, ge=1, le=200),
    desplazamiento: int = Query(0, ge=0),
    servicio: ComprasServicio = Depends(obtener_servicio),
):
    return servicio.listar(categoria=categoria, genero=genero, temporada=temporada, estado=estado,
                           limite=limite, desplazamiento=desplazamiento)
