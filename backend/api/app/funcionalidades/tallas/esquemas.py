from pydantic import BaseModel


class CurvaTalla(BaseModel):
    categoria: str
    talla: str
    compras: int
    pct: float
