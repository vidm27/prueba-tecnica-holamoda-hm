from fastapi import APIRouter, Depends, Query

from app.funcionalidades.compras.esquemas import PaginaCompras
from app.funcionalidades.compras.servicio import ComprasServicio
from app.funcionalidades.compras.dependencias import obtener_servicio
from app.nucleo.respuestas import ERRORES

router = APIRouter(responses=ERRORES, tags=["Compras"])


@router.get("/compras", response_model=PaginaCompras, summary="Listado paginado de compras con filtros")
def listar_compras(
    categoria: str | None = Query(None, description="Filtra por categoría: Clothing, Accessories, Footwear u Outerwear", examples=["Footwear"]),
    genero: str | None = Query(None, description="Filtra por género: Male o Female", examples=["Female"]),
    temporada: str | None = Query(None, description="Filtra por temporada: Fall, Spring, Summer o Winter", examples=["Winter"]),
    estado: str | None = Query(None, description="Filtra por estado de EE.UU., nombre completo", examples=["California"]),
    limite: int = Query(50, ge=1, le=200, description="Compras por página (máximo 200)"),
    desplazamiento: int = Query(0, ge=0, description="Cuántas compras saltar; 0 es la primera página"),
    servicio: ComprasServicio = Depends(obtener_servicio),
):
    """Listado paginado de compras con filtros opcionales. `limite` admite hasta 200; para la siguiente página, suma `limite` a `desplazamiento`."""
    return servicio.listar(categoria=categoria, genero=genero, temporada=temporada, estado=estado,
                           limite=limite, desplazamiento=desplazamiento)
