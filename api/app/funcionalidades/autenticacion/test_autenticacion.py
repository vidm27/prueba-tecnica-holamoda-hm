from app.nucleo.config import config

MAL = {"username": config.admin_usuario, "password": "incorrecta"}
BIEN = {"username": config.admin_usuario, "password": config.admin_clave}
LOGIN = "/api/v1/auth/login"


def test_login_correcto(cliente):
    r = cliente.post(LOGIN, data=BIEN)
    assert r.status_code == 200 and r.json()["token_type"] == "bearer"


def test_login_incorrecto(cliente):
    assert cliente.post(LOGIN, data=MAL).status_code == 401


def test_se_bloquea_tras_los_fallos_permitidos(cliente):
    for _ in range(config.login_max_fallos_ip):
        assert cliente.post(LOGIN, data=MAL).status_code == 401
    r = cliente.post(LOGIN, data=MAL)
    assert r.status_code == 429 and int(r.headers["Retry-After"]) > 0


def test_bloqueado_no_entra_ni_con_la_clave_correcta(cliente):
    for _ in range(config.login_max_fallos_ip):
        cliente.post(LOGIN, data=MAL)
    assert cliente.post(LOGIN, data=BIEN).status_code == 429


def test_login_correcto_reinicia_el_contador_de_ip(cliente):
    for _ in range(config.login_max_fallos_ip - 1):
        cliente.post(LOGIN, data=MAL)
    assert cliente.post(LOGIN, data=BIEN).status_code == 200
    for _ in range(config.login_max_fallos_ip - 1):  # vuelve a tener todos los intentos
        assert cliente.post(LOGIN, data=MAL).status_code == 401
