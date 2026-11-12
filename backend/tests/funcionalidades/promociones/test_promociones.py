def test_clasifica_todos_los_productos(cliente, auth):
    r = cliente.get("/api/v1/productos/promocion", headers=auth).json()
    assert len(r["productos"]) == 25
    assert r["compras_mujeres_con_descuento"] == 0
    assert {p["recomendacion"] for p in r["productos"]} <= {
        "promocion_exposicion", "revisar_producto", "riesgo_reputacion", "mantener"}
