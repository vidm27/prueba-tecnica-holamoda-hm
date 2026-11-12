from pydantic import BaseModel, ConfigDict


class GrupoHipotesis(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {'grupo': 'Fall', 'n': 975, 'media': 61.55692307692308}})
    grupo: str
    n: int
    media: float


class ResultadoHipotesis(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {'metrica': 'monto_usd',
         'variable': 'temporada',
         'prueba': 'Kruskal-Wallis',
         'estadistico': 11.378473087189425,
         'p_valor': 0.0098458649229873,
         'p_ajustado': 0.2756842178436444,
         'significativo': False,
         'veredicto': 'Parece significativa pero NO sobrevive la corrección por comparaciones múltiples: '
                      'probable falso positivo.',
         'grupos': [{'grupo': 'Fall', 'n': 975, 'media': 61.55692307692308},
                    {'grupo': 'Spring', 'n': 999, 'media': 58.73773773773774},
                    {'grupo': 'Summer', 'n': 955, 'media': 58.405235602094244},
                    {'grupo': 'Winter', 'n': 971, 'media': 60.35736354273944}]}})
    metrica: str
    variable: str
    prueba: str
    estadistico: float
    p_valor: float
    p_ajustado: float
    significativo: bool
    veredicto: str
    grupos: list[GrupoHipotesis]
