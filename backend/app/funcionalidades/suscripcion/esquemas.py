from pydantic import BaseModel


class ImpactoSuscripcion(BaseModel):
    suscrito: bool
    clientes: int
    ticket_promedio: float
    compras_previas_promedio: float
    calificacion_promedio: float
    gasto_anual_promedio: float
