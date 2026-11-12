def test_cuatro_temporadas_por_producto(cliente, auth):
    r = cliente.get("/api/v1/productos/estacionalidad", headers=auth).json()
    assert len(r) == 25 and set(r[0]["ventas_por_temporada"]) == {"Fall", "Spring", "Summer", "Winter"}
