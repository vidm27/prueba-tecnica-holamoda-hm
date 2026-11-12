from pydantic import BaseModel, ConfigDict


class Hallazgo(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # se construye desde el modelo ORM

    regla: str
    descripcion: str
    severidad: str
    filas_afectadas: int
    total_filas: int
    evidencia: dict
