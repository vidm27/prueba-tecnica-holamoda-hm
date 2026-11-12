from pydantic import BaseModel, ConfigDict


class Resumen(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {'compras': 3900,
         'clientes': 3900,
         'productos': 25,
         'ingreso_total': 233081.0,
         'ticket_promedio': 59.76,
         'calificacion_promedio': 3.75}})
    compras: int
    clientes: int
    productos: int
    ingreso_total: float
    ticket_promedio: float
    calificacion_promedio: float
