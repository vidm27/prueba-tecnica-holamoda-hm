"""Formato único de error de la API: {"error": {"codigo", "mensaje", "detalle"?}}."""
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class DetalleError(BaseModel):
    campo: str | None = None
    mensaje: str


class Error(BaseModel):
    codigo: str
    mensaje: str
    detalle: list[DetalleError] | None = None


class ErrorRespuesta(BaseModel):
    error: Error


def respuesta_error(estado: int, codigo: str, mensaje: str, *, detalle: list[dict] | None = None,
                    cabeceras: dict[str, str] | None = None) -> JSONResponse:
    cuerpo = {"error": {"codigo": codigo, "mensaje": mensaje, "detalle": detalle}}
    cuerpo["error"] = {k: v for k, v in cuerpo["error"].items() if v is not None}
    return JSONResponse(status_code=estado, content=cuerpo, headers=cabeceras)


# Respuestas de error que cada ruta documenta en OpenAPI. Todas las rutas las comparten.
ERRORES = {
    401: {"model": ErrorRespuesta, "description": "Falta el token, es inválido o está vencido"},
    422: {"model": ErrorRespuesta, "description": "Parámetros o datos no válidos"},
    503: {"model": ErrorRespuesta, "description": "Base de datos no disponible"},
}
