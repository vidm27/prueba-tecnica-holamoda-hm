"""El logger del proyecto registra cada petición con su request_id y su duración."""
from loguru import logger

from app.main import app
from fastapi.testclient import TestClient


def test_cada_peticion_queda_registrada_con_request_id():
    mensajes = []
    id_sink = logger.add(lambda m: mensajes.append(m.record), level="INFO")
    try:
        with TestClient(app) as cliente:
            r = cliente.get("/salud", headers={"X-Request-ID": "prueba-123"})
    finally:
        logger.remove(id_sink)

    assert r.headers["X-Request-ID"] == "prueba-123"
    lineas = [m for m in mensajes if "/salud" in m["message"]]
    assert lineas and "200" in lineas[0]["message"] and "ms" in lineas[0]["message"]
    assert lineas[0]["extra"]["request_id"] == "prueba-123"


def test_logs_de_la_biblioteca_estandar_pasan_por_loguru():
    import logging
    mensajes = []
    id_sink = logger.add(lambda m: mensajes.append(m.record["message"]), level="INFO")
    try:
        logging.getLogger("sqlalchemy.engine").warning("mensaje de prueba de SQLAlchemy")
    finally:
        logger.remove(id_sink)
    assert "mensaje de prueba de SQLAlchemy" in mensajes
