from pydantic import BaseModel


class TopEstado(BaseModel):
    estado: str
    producto: str
    ventas_producto: int
    ventas_estado: int
    productos_empatados: int
    talla: str
    ventas_talla: int
    color: str
    ventas_color: int
    muestra_suficiente: bool
