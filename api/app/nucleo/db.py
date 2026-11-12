from collections.abc import Iterator

from sqlalchemy import Connection, create_engine, text

from app.nucleo.config import config

engine = create_engine(config.url_bd, pool_pre_ping=True)


def obtener_conexion() -> Iterator[Connection]:
    with engine.connect() as conexion:
        yield conexion


def filas(conexion: Connection, sql: str, **parametros) -> list[dict]:
    """Ejecuta SQL parametrizado (nunca se concatenan valores del usuario)."""
    return [dict(f) for f in conexion.execute(text(sql), parametros).mappings()]
