def test_resumen(cliente, auth):
    r = cliente.get("/api/v1/resumen", headers=auth).json()
    assert r["compras"] == r["clientes"] == 3900 and r["productos"] == 25


def test_la_dependencia_del_servicio_es_sustituible(cliente, auth):
    """Prueba la inyección de dependencias: la ruta usa el servicio que FastAPI le entrega."""
    from app.funcionalidades.resumen.dependencias import obtener_servicio
    from app.main import app

    class ServicioFalso:
        def obtener(self):
            return {"compras": 1, "clientes": 1, "productos": 1, "ingreso_total": 1.0,
                    "ticket_promedio": 1.0, "calificacion_promedio": 1.0}

    app.dependency_overrides[obtener_servicio] = lambda: ServicioFalso()
    try:
        assert cliente.get("/api/v1/resumen", headers=auth).json()["compras"] == 1
    finally:
        app.dependency_overrides.clear()
