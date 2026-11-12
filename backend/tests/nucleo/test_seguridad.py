import jwt

from app.nucleo.seguridad import ALGORITMO, crear_token

RUTA_PROTEGIDA = "/api/v1/resumen"


def test_sin_token_es_401(cliente):
    assert cliente.get(RUTA_PROTEGIDA).status_code == 401


def test_token_vencido_es_401(cliente):
    token = crear_token("admin", minutos=-1)
    assert cliente.get(RUTA_PROTEGIDA, headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_token_firmado_con_otra_llave_es_401(cliente):
    falso = jwt.encode({"sub": "admin", "exp": 9999999999}, "x" * 32, algorithm=ALGORITMO)
    assert cliente.get(RUTA_PROTEGIDA, headers={"Authorization": f"Bearer {falso}"}).status_code == 401


def test_salud_es_publico(cliente):
    assert cliente.get("/salud").json() == {"estado": "ok"}
