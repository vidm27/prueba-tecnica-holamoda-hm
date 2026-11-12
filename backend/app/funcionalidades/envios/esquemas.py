from pydantic import BaseModel, ConfigDict


class EnvioSegmento(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {'segmento': 'Female', 'tipo_envio': 'Free Shipping', 'compras': 249, 'pct_segmento': 20.0}})
    segmento: str
    tipo_envio: str
    compras: int
    pct_segmento: float
