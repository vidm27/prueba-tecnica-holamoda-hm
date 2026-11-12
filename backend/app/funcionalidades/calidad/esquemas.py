from pydantic import BaseModel, ConfigDict


class Hallazgo(BaseModel):
    model_config = ConfigDict(from_attributes=True, json_schema_extra={"example": {'regla': 'beneficios_por_genero',
         'descripcion': 'Ningún cliente de género Female tiene suscripción ni descuento: sesgo de origen '
                        'en los datos, no un comportamiento real.',
         'severidad': 'alta',
         'filas_afectadas': 1248,
         'total_filas': 3900,
         'evidencia': {'tasas': {'Female': {'suscrito': 0.0, 'descuento': 0.0},
                                 'Male': {'suscrito': 0.397, 'descuento': 0.632}}}}})  # se construye desde el modelo ORM

    regla: str
    descripcion: str
    severidad: str
    filas_afectadas: int
    total_filas: int
    evidencia: dict
