from pydantic import BaseModel


class Estacionalidad(BaseModel):
    producto: str
    ventas_por_temporada: dict[str, int]
    temporada_pico: str
    temporada_valle: str
