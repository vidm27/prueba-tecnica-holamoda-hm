from pydantic import BaseModel


class Hallazgo(BaseModel):
    regla: str
    descripcion: str
    severidad: str
    filas_afectadas: int
    total_filas: int
    evidencia: dict
