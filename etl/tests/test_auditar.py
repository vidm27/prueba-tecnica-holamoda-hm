import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parents[1]))
from auditar import auditar  # noqa: E402
from test_transformar import fila  # noqa: E402
from transformar import enriquecer, validar  # noqa: E402


def preparar(filas):
    return enriquecer(validar(pd.DataFrame(filas)))


def reglas(df):
    return set(auditar(df).regla)


def test_detecta_sesgo_y_redundancia():
    df = preparar([
        fila(**{"Customer ID": 1, "Gender": "Female", "Subscription Status": "No",
                "Discount Applied": "No", "Promo Code Used": "No"}),
        fila(**{"Customer ID": 2, "Subscription Status": "Yes", "Discount Applied": "Yes", "Promo Code Used": "Yes"}),
    ])
    r = reglas(df)
    assert {"beneficios_por_genero", "columnas_redundantes", "suscripcion_implica_descuento"} <= r


def test_no_marca_sesgo_si_ambos_generos_tienen_beneficios():
    df = preparar([
        fila(**{"Customer ID": 1, "Gender": "Female", "Discount Applied": "Yes"}),
        fila(**{"Customer ID": 2, "Discount Applied": "Yes"}),
    ])
    assert "beneficios_por_genero" not in reglas(df)


def test_siempre_reporta_sin_fecha():
    assert "sin_dimension_temporal" in reglas(preparar([fila()]))
