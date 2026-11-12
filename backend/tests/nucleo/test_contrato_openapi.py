"""Todas las rutas siguen el mismo estándar: documentan el mismo formato de error."""
from app.main import app

PUBLICAS = {"/salud"}  # sin autenticación ni parámetros que validar


def test_cada_ruta_documenta_el_formato_de_error_estandar():
    esquema = app.openapi()
    referencia = "#/components/schemas/ErrorRespuesta"
    rutas = {ruta: ops for ruta, ops in esquema["paths"].items() if ruta not in PUBLICAS}
    assert len(rutas) >= 13
    for ruta, operaciones in rutas.items():
        for metodo, op in operaciones.items():
            for estado in ("401", "422", "503"):
                assert estado in op["responses"], f"{metodo} {ruta} no documenta {estado}"
                contenido = op["responses"][estado]["content"]["application/json"]["schema"]
                assert contenido == {"$ref": referencia}, f"{metodo} {ruta} {estado}"
