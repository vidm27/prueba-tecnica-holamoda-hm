"""Toda ruta de la API exige token, salvo el login que lo emite."""
from fastapi.routing import APIRoute

from app.main import app
from app.nucleo.seguridad import usuario_actual

PUBLICAS = {"/api/v1/auth/login"}


def _protegida(ruta: APIRoute) -> bool:
    return any(dep.call is usuario_actual for dep in ruta.dependant.dependencies)


def test_todas_las_rutas_de_la_api_estan_protegidas_salvo_el_login():
    rutas_api = [r for r in app.routes if isinstance(r, APIRoute) and r.path.startswith("/api/v1")]
    assert len(rutas_api) == 13  # login + 12 funcionalidades protegidas
    for ruta in rutas_api:
        if ruta.path in PUBLICAS:
            assert not _protegida(ruta), ruta.path
        else:
            assert _protegida(ruta), f"{ruta.path} no exige autenticación"


def test_salud_queda_fuera_de_la_api():
    rutas = {r.path for r in app.routes if isinstance(r, APIRoute)}
    assert "/salud" in rutas
    assert not any(p == "/salud" and p.startswith("/api") for p in rutas)
