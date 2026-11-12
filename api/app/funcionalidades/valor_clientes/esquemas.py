from pydantic import BaseModel


class NivelValor(BaseModel):
    nivel: str
    clientes: int
    gasto_anual_total: float
    pct_gasto: float
    gasto_minimo: float
    gasto_maximo: float


class Valor(BaseModel):
    pareto_top20_pct_gasto: float
    niveles: list[NivelValor]
