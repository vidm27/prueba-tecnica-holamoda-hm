from app.nucleo.config import config

MAL = {"username": config.admin_usuario, "password": "incorrecta"}
BIEN = {"username": config.admin_usuario, "password": config.admin_clave}
LOGIN = "/api/v1/auth/login"
MAXIMO = int(config.login_limite.split("/")[0])


def test_login_correcto(cliente):
    r = cliente.post(LOGIN, data=BIEN)
    assert r.status_code == 200 and r.json()["token_type"] == "bearer"


def test_login_incorrecto(cliente):
    assert cliente.post(LOGIN, data=MAL).status_code == 401


def test_se_bloquea_al_superar_el_limite(cliente):
    for _ in range(MAXIMO):
        assert cliente.post(LOGIN, data=MAL).status_code == 401
    r = cliente.post(LOGIN, data=MAL)
    assert r.status_code == 429
    assert int(r.headers["Retry-After"]) > 0 and "Demasiados intentos" in r.json()["detail"]


def test_bloqueado_no_entra_ni_con_la_clave_correcta(cliente):
    for _ in range(MAXIMO):
        cliente.post(LOGIN, data=MAL)
    assert cliente.post(LOGIN, data=BIEN).status_code == 429
