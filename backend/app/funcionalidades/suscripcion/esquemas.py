from pydantic import BaseModel, ConfigDict


class ImpactoSuscripcion(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {'suscrito': False,
         'clientes': 2847,
         'ticket_promedio': 59.87,
         'compras_previas_promedio': 25.1,
         'calificacion_promedio': 3.75,
         'gasto_anual_promedio': 1030.57}})
    suscrito: bool
    clientes: int
    ticket_promedio: float
    compras_previas_promedio: float
    calificacion_promedio: float
    gasto_anual_promedio: float
