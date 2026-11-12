def test_segmento_valido(cliente, auth):
    assert cliente.get("/api/v1/envios/por-segmento", headers=auth, params={"segmento": "genero"}).status_code == 200


def test_segmento_invalido_se_rechaza(cliente, auth):
    r = cliente.get("/api/v1/envios/por-segmento", headers=auth, params={"segmento": "ubicacion; DROP"})
    assert r.status_code == 422
