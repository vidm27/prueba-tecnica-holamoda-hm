def get(cliente, auth, **params):
    r = cliente.get("/api/v1/compras", headers=auth, params=params)
    assert r.status_code == 200, r.text
    return r.json()


def test_paginacion_y_filtros(cliente, auth):
    r = get(cliente, auth, categoria="Footwear", limite=5)
    assert r["total"] == 599 and len(r["items"]) == 5
    assert all(i["categoria"] == "Footwear" for i in r["items"])
    assert get(cliente, auth, limite=5, desplazamiento=5)["items"][0]["id"] == 6


def test_limite_invalido(cliente, auth):
    assert cliente.get("/api/v1/compras", headers=auth, params={"limite": 1000}).status_code == 422
