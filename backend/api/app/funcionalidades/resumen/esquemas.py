from pydantic import BaseModel


class Resumen(BaseModel):
    compras: int
    clientes: int
    productos: int
    ingreso_total: float
    ticket_promedio: float
    calificacion_promedio: float
