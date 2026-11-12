"""Logger del proyecto: loguru.

Todo el backend (la app, uvicorn, SQLAlchemy y slowapi) escribe por loguru, con un único formato.
Para depurar: LOG_NIVEL=DEBUG en .env.
"""
import logging
import sys

from loguru import logger

from app.nucleo.config import config

FORMATO = ("<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | "
           "<cyan>{extra[request_id]}</cyan> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

# Bibliotecas que usan logging estándar: sus mensajes pasan por loguru.
BIBLIOTECAS = ("uvicorn", "uvicorn.error", "uvicorn.access", "sqlalchemy.engine", "slowapi")


class InterceptarLogging(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            nivel = logger.level(record.levelname).name
        except ValueError:
            nivel = record.levelno
        # Sube la pila saltando los frames del módulo logging, para que loguru muestre
        # el archivo que originó el mensaje (y no logging/__init__.py).
        frame, profundidad = sys._getframe(1), 1
        while frame is not None and frame.f_globals.get("__name__", "").startswith("logging"):
            frame = frame.f_back
            profundidad += 1
        logger.opt(depth=profundidad, exception=record.exc_info).log(nivel, record.getMessage())


def configurar_logs() -> None:
    logger.remove()
    # diagnose=False a propósito: loguru mostraría variables locales en los tracebacks,
    # y en el login hay claves en memoria.
    logger.configure(extra={"request_id": "-"})
    logger.add(sys.stderr, level=config.log_nivel.upper(), format=FORMATO, diagnose=False, backtrace=False)

    logging.basicConfig(handlers=[InterceptarLogging()], level=0, force=True)
    for nombre in BIBLIOTECAS:
        biblioteca = logging.getLogger(nombre)
        biblioteca.handlers = [InterceptarLogging()]
        biblioteca.propagate = False
