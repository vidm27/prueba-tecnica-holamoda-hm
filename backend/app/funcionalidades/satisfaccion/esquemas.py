from pydantic import BaseModel, ConfigDict


class Satisfaccion(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {'producto': 'Shirt',
         'categoria': 'Clothing',
         'compras': 169,
         'calificacion': 3.63,
         'margen_error_95': 0.11}})
    producto: str
    categoria: str
    compras: int
    calificacion: float
    margen_error_95: float  # ±, con 1.96·σ/√n
