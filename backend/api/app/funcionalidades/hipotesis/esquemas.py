from pydantic import BaseModel


class GrupoHipotesis(BaseModel):
    grupo: str
    n: int
    media: float


class ResultadoHipotesis(BaseModel):
    metrica: str
    variable: str
    prueba: str
    estadistico: float
    p_valor: float
    p_ajustado: float
    significativo: bool
    veredicto: str
    grupos: list[GrupoHipotesis]
