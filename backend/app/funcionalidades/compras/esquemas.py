from pydantic import BaseModel


class CompraDetalle(BaseModel):
    id: int
    producto: str
    categoria: str
    genero: str
    edad: int
    estado: str
    monto_usd: float
    talla: str
    color: str
    temporada: str
    calificacion: float
    tipo_envio: str
    descuento: bool
    metodo_pago: str
    nivel_valor: str


class PaginaCompras(BaseModel):
    total: int
    limite: int
    desplazamiento: int
    items: list[CompraDetalle]
