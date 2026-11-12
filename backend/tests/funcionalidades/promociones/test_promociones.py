def test_clasifica_todos_los_productos(cliente, auth):
    r = cliente.get("/api/v1/productos/promocion", headers=auth).json()
    assert len(r["productos"]) == 25
    assert r["compras_mujeres_con_descuento"] == 0
    assert {p["recomendacion"] for p in r["productos"]} <= {
        "promocion_exposicion", "revisar_producto", "riesgo_reputacion", "mantener"}


def test_filtra_oportunidades_por_genero(cliente, auth):
    mujeres = cliente.get("/api/v1/productos/promocion?genero=Female", headers=auth).json()
    hombres = cliente.get("/api/v1/productos/promocion?genero=Male", headers=auth).json()
    assert len(mujeres["productos"]) == 25
    assert len(hombres["productos"]) == 25
    assert mujeres["mediana_ventas"] < hombres["mediana_ventas"]
    assert all(p["pct_mujeres"] == 1.0 for p in mujeres["productos"])
    assert all(p["pct_mujeres"] == 0.0 for p in hombres["productos"])
