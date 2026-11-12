from pydantic import BaseModel


class ProductoPromocion(BaseModel):
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
    mediana_ventas: float
    mediana_calificacion: float
    compras_mujeres_con_descuento: int
    advertencia: str
    productos: list[ProductoPromocion]
