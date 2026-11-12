from pydantic import BaseModel, ConfigDict


class CompraDetalle(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {'id': 1,
         'producto': 'Blouse',
         'categoria': 'Clothing',
         'genero': 'Male',
         'edad': 55,
         'estado': 'Kentucky',
         'monto_usd': 53.0,
         'talla': 'L',
         'color': 'Gray',
         'temporada': 'Winter',
         'calificacion': 3.1,
         'tipo_envio': 'Express',
         'descuento': True,
         'metodo_pago': 'Credit Card',
         'nivel_valor': 'Oro'}})
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
    model_config = ConfigDict(json_schema_extra={"example": {'total': 3900,
         'limite': 1,
         'desplazamiento': 0,
         'items': [{'id': 1,
                    'producto': 'Blouse',
                    'categoria': 'Clothing',
                    'genero': 'Male',
                    'edad': 55,
                    'estado': 'Kentucky',
                    'monto_usd': 53.0,
                    'talla': 'L',
                    'color': 'Gray',
                    'temporada': 'Winter',
                    'calificacion': 3.1,
                    'tipo_envio': 'Express',
                    'descuento': True,
                    'metodo_pago': 'Credit Card',
                    'nivel_valor': 'Oro'}]}})
    total: int
    limite: int
    desplazamiento: int
    items: list[CompraDetalle]
