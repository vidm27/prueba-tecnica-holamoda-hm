from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlmodel import Session

from app.nucleo.config import config

engine = create_engine(config.url_bd, pool_pre_ping=True)


def obtener_sesion() -> Iterator[Session]:
    """Dependencia de FastAPI: una sesión por petición, cerrada al terminar."""
    with Session(engine) as sesion:
        yield sesion
