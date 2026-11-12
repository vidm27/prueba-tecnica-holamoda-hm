from pydantic import BaseModel


class Satisfaccion(BaseModel):
    producto: str
    categoria: str
    compras: int
    calificacion: float
    margen_error_95: float  # ±, con 1.96·σ/√n
