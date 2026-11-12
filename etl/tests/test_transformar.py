import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))
from transformar import transformar  # noqa: E402


def fila(**cambios):
    base = {
        "Customer ID": 1, "Age": 30, "Gender": " Male ", "Item Purchased": "Blouse",
        "Category": "Clothing", "Purchase Amount (USD)": 50, "Location": "Panama",
        "Size": "M", "Color": "Red", "Season": "Summer", "Review Rating": 4.5,
        "Subscription Status": "Yes", "Payment Method": "Cash", "Shipping Type": "Express",
        "Discount Applied": "No", "Promo Code Used": "No", "Previous Purchases": 3,
        "Preferred Payment Method": "Cash", "Frequency of Purchases": "Weekly",
    }
    return {**base, **cambios}


def test_separa_tablas_y_normaliza():
    df = pd.DataFrame([fila(), fila(**{"Customer ID": 2, "Item Purchased": "Shirt", "Age": 70})])
    t = transformar(df)
    assert len(t["clientes"]) == 2 and len(t["productos"]) == 2
    assert t["clientes"].genero.iloc[0] == "Male"  # strip
    assert t["clientes"].suscrito.iloc[0]
    assert not t["compras"].descuento.iloc[0]
    assert list(t["clientes"].grupo_edad) == ["25-34", "65+"]
    assert set(t["compras"].producto_id) == set(t["productos"].id)
    assert "auditoria" in t


def test_segmentacion_por_valor():
    frecs = ["Annually", "Quarterly", "Monthly", "Weekly"]
    df = pd.DataFrame([fila(**{"Customer ID": i + 1, "Frequency of Purchases": f}) for i, f in enumerate(frecs)])
    c = transformar(df)["clientes"].set_index("id")
    assert list(c.compras_por_anio) == [1, 4, 12, 52]
    assert c.gasto_anual_estimado[4] == 50 * 52
    assert list(c.nivel_valor) == ["Bronce", "Plata", "Oro", "Platino"]


def test_falla_con_frecuencia_desconocida():
    with pytest.raises(ValueError):
        transformar(pd.DataFrame([fila(**{"Frequency of Purchases": "Daily"})]))


def test_descarta_duplicados_e_invalidos():
    df = pd.DataFrame([
        fila(), fila(),  # duplicado
        fila(**{"Customer ID": 3, "Purchase Amount (USD)": -5}),
        fila(**{"Customer ID": 4, "Review Rating": 9}),
        fila(**{"Customer ID": 5, "Age": None}),
        fila(**{"Customer ID": 6, "Subscription Status": "Maybe"}),
    ])
    assert len(transformar(df)["compras"]) == 1


def test_falla_si_faltan_columnas():
    with pytest.raises(ValueError):
        transformar(pd.DataFrame([fila()]).drop(columns=["Age"]))
