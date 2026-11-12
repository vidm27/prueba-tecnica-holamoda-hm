def test_top_por_estado(cliente, auth):
    r = cliente.get("/api/v1/estados/top-productos", headers=auth).json()
    assert len(r) == 50
    assert all(e["ventas_producto"] <= e["ventas_estado"] for e in r)
    assert all(e["productos_empatados"] >= 1 for e in r)
