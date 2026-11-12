def test_ajuste_nunca_menor_que_p(cliente, auth):
    r = cliente.get("/api/v1/hipotesis", headers=auth, params={"metrica": "monto_usd", "variable": "temporada"}).json()
    assert r["p_ajustado"] >= r["p_valor"] and len(r["grupos"]) == 4
    assert not r["significativo"]  # en este dataset ninguna variable sobrevive la corrección


def test_variable_invalida(cliente, auth):
    r = cliente.get("/api/v1/hipotesis", headers=auth, params={"metrica": "monto_usd", "variable": "x; DROP TABLE"})
    assert r.status_code == 422
