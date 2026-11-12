from pydantic import BaseModel, ConfigDict


class ProductoPromocion(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {'producto': 'Jeans',
         'categoria': 'Clothing',
         'ventas': 124,
         'calificacion': 3.65,
         'pct_descuento': 0.46,
         'pct_mujeres': 0.234,
         'ticket_con_descuento': 56.12,
         'ticket_sin_descuento': 64.91,
         'recomendacion': 'revisar_producto',
         'motivo': 'Se vende poco y está mal calificado: descontar no resuelve el problema.'}})
    producto: str
    categoria: str
    ventas: int
    calificacion: float
    pct_descuento: float
    pct_mujeres: float
    ticket_con_descuento: float | None
    ticket_sin_descuento: float | None
    recomendacion: str  # promocion_exposicion | revisar_producto | riesgo_reputacion | mantener
    motivo: str


class Promociones(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {'mediana_ventas': 158.0,
         'mediana_calificacion': 3.75,
         'compras_mujeres_con_descuento': 0,
         'advertencia': 'Sin fecha de compra no se puede medir el efecto del descuento sobre el volumen de '
                        'ventas.',
         'productos': [{'producto': 'Jeans',
                        'categoria': 'Clothing',
                        'ventas': 124,
                        'calificacion': 3.65,
                        'pct_descuento': 0.46,
                        'pct_mujeres': 0.234,
                        'ticket_con_descuento': 56.12,
                        'ticket_sin_descuento': 64.91,
                        'recomendacion': 'revisar_producto',
                        'motivo': 'Se vende poco y está mal calificado: descontar no resuelve el '
                                  'problema.'},
                       {'producto': 'Gloves',
                        'categoria': 'Accessories',
                        'ventas': 140,
                        'calificacion': 3.86,
                        'pct_descuento': 0.429,
                        'pct_mujeres': 0.264,
                        'ticket_con_descuento': 58.6,
                        'ticket_sin_descuento': 62.01,
                        'recomendacion': 'promocion_exposicion',
                        'motivo': 'Bien calificado pero se vende poco: falta visibilidad, no precio.'}]}})
    mediana_ventas: float
    mediana_calificacion: float
    compras_mujeres_con_descuento: int
    advertencia: str
    productos: list[ProductoPromocion]
