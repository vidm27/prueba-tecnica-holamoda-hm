from pydantic import BaseModel, ConfigDict


class Estacionalidad(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {'producto': 'Backpack',
         'ventas_por_temporada': {'Winter': 25, 'Spring': 39, 'Summer': 45, 'Fall': 34},
         'temporada_pico': 'Summer',
         'temporada_valle': 'Winter'}})
    producto: str
    ventas_por_temporada: dict[str, int]
    temporada_pico: str
    temporada_valle: str
