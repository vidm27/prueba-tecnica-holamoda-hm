def test_resumen(cliente, auth):
    r = cliente.get("/api/v1/resumen", headers=auth).json()
    assert r["compras"] == r["clientes"] == 3900 and r["productos"] == 25
