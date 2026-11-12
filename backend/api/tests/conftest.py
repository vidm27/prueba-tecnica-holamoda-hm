import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.main import app
from app.nucleo.config import config
from app.nucleo.db import engine
from app.nucleo.limitador import limitador


@pytest.fixture(autouse=True)
def limitador_limpio():
    """Cada test parte (y termina) sin intentos acumulados, para no afectar a la fixture `auth`."""
    limitador.reset()
    yield
    limitador.reset()


@pytest.fixture(scope="session")
def cliente():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def hay_datos():
    """Los tests de endpoints son de integración: requieren haber corrido el ETL."""
    with engine.connect() as con:
        if not con.execute(text("SELECT count(*) FROM compras")).scalar():
            pytest.skip("Base vacía: corre el ETL primero")


@pytest.fixture(scope="session")
def auth(cliente, hay_datos):
    r = cliente.post("/api/v1/auth/login", data={"username": config.admin_usuario, "password": config.admin_clave})
    assert r.status_code == 200
    return {"Authorization": f"Bearer {r.json()['access_token']}"}
