from app.funcionalidades.estados.servicio import calcular_top_por_estado


def test_empate_no_es_muestra_suficiente():
    productos = [{"estado": "X", "producto": "A", "n": 5},
                 {"estado": "X", "producto": "B", "n": 5},
                 {"estado": "X", "producto": "C", "n": 2}]
    tallas = [{"estado": "X", "producto": "A", "talla": "M", "n": 3},
              {"estado": "X", "producto": "A", "talla": "S", "n": 2}]
    colores = [{"estado": "X", "producto": "A", "color": "Red", "n": 5}]

    (r,) = calcular_top_por_estado(productos, tallas, colores, min_muestra=3)

    assert r["producto"] == "A"  # empate: gana el nombre alfabéticamente primero
    assert r["productos_empatados"] == 2
    assert r["muestra_suficiente"] is False
    assert r["talla"] == "M" and r["ventas_estado"] == 12


def test_ganador_claro_con_muestra_suficiente():
    productos = [{"estado": "Y", "producto": "A", "n": 8}, {"estado": "Y", "producto": "B", "n": 3}]
    (r,) = calcular_top_por_estado(productos, [], [], min_muestra=5)
    assert r["producto"] == "A" and r["muestra_suficiente"] is True
