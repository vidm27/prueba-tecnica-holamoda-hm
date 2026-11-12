from app.funcionalidades.promociones.servicio import recomendar


def test_cuatro_cruces_de_volumen_y_calificacion():
    assert recomendar({"ventas": 10, "calificacion": 4.0}, 20, 3.5)[0] == "promocion_exposicion"
    assert recomendar({"ventas": 10, "calificacion": 3.0}, 20, 3.5)[0] == "revisar_producto"
    assert recomendar({"ventas": 30, "calificacion": 3.0}, 20, 3.5)[0] == "riesgo_reputacion"
    assert recomendar({"ventas": 30, "calificacion": 4.0}, 20, 3.5)[0] == "mantener"
