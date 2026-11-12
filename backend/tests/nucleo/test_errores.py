"""Contrato de errores: todo fallo de la API responde {"error": {codigo, mensaje, detalle?}}."""
from app.nucleo.errores import ErrorAplicacion


def assert_error(r, estado: int, codigo: str):
    assert r.status_code == estado, r.text
    cuerpo = r.json()
    assert set(cuerpo) == {"error"}
    assert cuerpo["error"]["codigo"] == codigo
    assert cuerpo["error"]["mensaje"]


def test_ruta_inexistente(cliente):
    assert_error(cliente.get("/api/v1/no_existe"), 404, "no_encontrado")


def test_parametro_invalido_lista_los_campos(cliente, auth):
    r = cliente.get("/api/v1/compras", headers=auth, params={"limite": 1000})
    assert_error(r, 422, "validacion")
    assert r.json()["error"]["detalle"][0]["campo"] == "limite"


def test_sin_token(cliente):
    assert_error(cliente.get("/api/v1/resumen"), 401, "token_invalido")


def test_token_invalido(cliente):
    r = cliente.get("/api/v1/resumen", headers={"Authorization": "Bearer basura"})
    assert_error(r, 401, "token_invalido")
    assert r.headers["WWW-Authenticate"] == "Bearer"


def test_errores_de_aplicacion_declaran_estado_y_codigo():
    import app.nucleo.errores as errores
    subclases = [c for c in vars(errores).values()
                 if isinstance(c, type) and issubclass(c, ErrorAplicacion) and c is not ErrorAplicacion]
    assert subclases
    for c in subclases:
        assert c.estado >= 400 and c.codigo and c.codigo == c.codigo.lower()
