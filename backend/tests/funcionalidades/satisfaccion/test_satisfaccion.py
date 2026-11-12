def test_ordenada_de_peor_a_mejor(cliente, auth):
    r = cliente.get("/api/v1/productos/satisfaccion", headers=auth).json()
    califs = [p["calificacion"] for p in r]
    assert califs == sorted(califs) and len(r) == 25
