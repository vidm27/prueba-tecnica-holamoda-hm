from app.nucleo.config import config

LOGIN = "/api/v1/auth/login"


def test_login_correcto(cliente):
    r = cliente.post(LOGIN, data={"username": config.admin_usuario, "password": config.admin_clave})
    assert r.status_code == 200 and r.json()["token_type"] == "bearer"


def test_login_incorrecto(cliente):
    assert cliente.post(LOGIN, data={"username": config.admin_usuario, "password": "incorrecta"}).status_code == 401
