from pydantic import BaseModel, ConfigDict


class CurvaTalla(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {'categoria': 'Clothing', 'talla': 'M', 'compras': 778, 'pct': 44.8}})
    categoria: str
    talla: str
    compras: int
    pct: float
