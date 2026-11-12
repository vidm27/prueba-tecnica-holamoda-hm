from pydantic import BaseModel


class EnvioSegmento(BaseModel):
    segmento: str
    tipo_envio: str
    compras: int
    pct_segmento: float
