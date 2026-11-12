def test_curva_suma_100(cliente, auth):
    r = cliente.get("/api/v1/tallas/curva", headers=auth, params={"categoria": "Clothing"}).json()
    assert {t["categoria"] for t in r} == {"Clothing"}
    assert abs(sum(t["pct"] for t in r) - 100) < 0.5
