def test_niveles_y_pareto(cliente, auth):
    r = cliente.get("/api/v1/clientes/valor", headers=auth).json()
    assert [n["nivel"] for n in r["niveles"]] == ["Bronce", "Plata", "Oro", "Platino"]
    assert abs(sum(n["pct_gasto"] for n in r["niveles"]) - 100) < 0.5
    assert 50 < r["pareto_top20_pct_gasto"] < 100
