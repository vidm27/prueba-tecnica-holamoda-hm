from pydantic import BaseModel, ConfigDict


class TopEstado(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {'estado': 'Alabama',
         'producto': 'Jewelry',
         'ventas_producto': 8,
         'ventas_estado': 89,
         'productos_empatados': 1,
         'talla': 'S',
         'ventas_talla': 3,
         'color': 'Black',
         'ventas_color': 1,
         'muestra_suficiente': False}})
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
