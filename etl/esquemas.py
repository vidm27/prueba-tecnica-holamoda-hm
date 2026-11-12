"""Contrato de una fila cruda del CSV (Pydantic). Valida tipos y rangos."""
from pydantic import BaseModel, ConfigDict, Field


class FilaCruda(BaseModel):
    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    cliente_id: int = Field(alias="Customer ID", ge=1)
    edad: int = Field(alias="Age", ge=0, le=120)
    genero: str = Field(alias="Gender", min_length=1)
    producto: str = Field(alias="Item Purchased", min_length=1)
    categoria: str = Field(alias="Category", min_length=1)
    monto_usd: float = Field(alias="Purchase Amount (USD)", gt=0)
    ubicacion: str = Field(alias="Location", min_length=1)
    talla: str = Field(alias="Size", min_length=1)
    color: str = Field(alias="Color", min_length=1)
    temporada: str = Field(alias="Season", min_length=1)
    calificacion: float = Field(alias="Review Rating", ge=1, le=5)
    suscrito: bool = Field(alias="Subscription Status")  # acepta Yes/No
    metodo_pago: str = Field(alias="Payment Method", min_length=1)
    tipo_envio: str = Field(alias="Shipping Type", min_length=1)
    descuento: bool = Field(alias="Discount Applied")
    codigo_promo: bool = Field(alias="Promo Code Used")
    compras_previas: int = Field(alias="Previous Purchases", ge=0)
    metodo_pago_preferido: str = Field(alias="Preferred Payment Method", min_length=1)
    frecuencia_compras: str = Field(alias="Frequency of Purchases", min_length=1)
