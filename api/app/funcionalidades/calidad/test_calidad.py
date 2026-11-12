def test_ordenada_por_severidad(cliente, auth):
    r = cliente.get("/api/v1/calidad/auditoria", headers=auth).json()
    assert r[0]["severidad"] == "alta"
