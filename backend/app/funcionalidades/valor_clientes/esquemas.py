from pydantic import BaseModel, ConfigDict


class NivelValor(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {'nivel': 'Bronce',
         'clientes': 974,
         'gasto_anual_total': 87147.0,
         'pct_gasto': 2.2,
         'gasto_minimo': 20.0,
         'gasto_maximo': 184.0}})
    nivel: str
    clientes: int
    gasto_anual_total: float
    pct_gasto: float
    gasto_minimo: float
    gasto_maximo: float


class Valor(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {'pareto_top20_pct_gasto': 56.7,
         'niveles': [{'nivel': 'Bronce',
                      'clientes': 974,
                      'gasto_anual_total': 87147.0,
                      'pct_gasto': 2.2,
                      'gasto_minimo': 20.0,
                      'gasto_maximo': 184.0},
                     {'nivel': 'Plata',
                      'clientes': 974,
                      'gasto_anual_total': 320122.0,
                      'pct_gasto': 7.9,
                      'gasto_minimo': 188.0,
                      'gasto_maximo': 564.0},
                     {'nivel': 'Oro',
                      'clientes': 980,
                      'gasto_anual_total': 1008524.0,
                      'pct_gasto': 24.9,
                      'gasto_minimo': 572.0,
                      'gasto_maximo': 1638.0},
                     {'nivel': 'Platino',
                      'clientes': 972,
                      'gasto_anual_total': 2636036.0,
                      'pct_gasto': 65.1,
                      'gasto_minimo': 1664.0,
                      'gasto_maximo': 5200.0}]}})
    pareto_top20_pct_gasto: float
    niveles: list[NivelValor]
