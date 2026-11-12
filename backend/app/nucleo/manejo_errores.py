"""Convierte cualquier error en la respuesta estándar. Es el único lugar que decide el formato."""
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from slowapi.errors import RateLimitExceeded
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as ErrorHTTP

from app.nucleo.errores import ErrorAplicacion, LimiteExcedido, ServicioNoDisponible
from app.nucleo.respuestas import respuesta_error

log = logging.getLogger("api")

CODIGOS_HTTP = {400: "solicitud_invalida", 401: "no_autorizado", 403: "prohibido",
                404: "no_encontrado", 405: "metodo_no_permitido"}
MENSAJES_HTTP = {404: "La ruta solicitada no existe", 405: "Método no permitido para esta ruta"}


def _desde_aplicacion(error: ErrorAplicacion):
    return respuesta_error(error.estatus, error.codigo, error.mensaje,
                           detalle=error.detalle, cabeceras=error.cabeceras)


def registrar_manejadores(app: FastAPI) -> None:
    @app.exception_handler(ErrorAplicacion)
    async def error_aplicacion(_: Request, exc: ErrorAplicacion):
        return _desde_aplicacion(exc)

    @app.exception_handler(RateLimitExceeded)
    async def limite_excedido(_: Request, exc: RateLimitExceeded):
        return _desde_aplicacion(LimiteExcedido(exc.limit.limit.get_expiry()))

    @app.exception_handler(RequestValidationError)
    async def validacion(_: Request, exc: RequestValidationError):
        detalle = [{"campo": ".".join(str(p) for p in e["loc"][1:]) or None, "mensaje": e["msg"]}
                   for e in exc.errors()]
        return respuesta_error(422, "validacion", "Datos de entrada no válidos", detalle=detalle)

    @app.exception_handler(ErrorHTTP)
    async def error_http(_: Request, exc: ErrorHTTP):
        codigo = CODIGOS_HTTP.get(exc.status_code, "error_http")
        mensaje = MENSAJES_HTTP.get(exc.status_code, str(exc.detail))
        return respuesta_error(exc.status_code, codigo, mensaje, cabeceras=exc.headers)

    @app.exception_handler(SQLAlchemyError)
    async def error_bd(_: Request, exc: SQLAlchemyError):
        log.exception("Error de base de datos")
        return _desde_aplicacion(ServicioNoDisponible())

    @app.exception_handler(Exception)
    async def error_inesperado(_: Request, exc: Exception):
        log.exception("Error no controlado")
        return respuesta_error(500, "error_interno", "Error interno del servidor")
