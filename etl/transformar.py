import logging

import pandas as pd
from pydantic import ValidationError

from esquemas import FilaCruda

log = logging.getLogger(__name__)

COLUMNAS_CLIENTE = ["cliente_id", "edad", "grupo_edad", "genero", "ubicacion", "suscrito",
                    "compras_previas", "metodo_pago_preferido", "frecuencia_compras"]
COLUMNAS_COMPRA = ["cliente_id", "producto_id", "monto_usd", "talla", "color", "temporada",
                   "calificacion", "tipo_envio", "descuento", "codigo_promo", "metodo_pago"]


def validar(crudo: pd.DataFrame) -> pd.DataFrame:
    """Valida cada fila con Pydantic; las inválidas se descartan y se registran."""
    esperadas = {f.alias for f in FilaCruda.model_fields.values()}
    if faltan := esperadas - set(crudo.columns):
        raise ValueError(f"Faltan columnas en el CSV: {sorted(faltan)}")

    validas, rechazadas = [], 0
    for i, fila in enumerate(crudo.to_dict("records")):
        try:
            validas.append(FilaCruda.model_validate(fila).model_dump())
        except ValidationError as e:
            rechazadas += 1
            log.warning("Fila %d rechazada: %s", i + 2, e.errors()[0]["loc"])  # +2: cabecera y base 1
    df = pd.DataFrame(validas)
    antes = len(df)
    df = df.drop_duplicates("cliente_id")
    if antes != len(df):
        log.warning("Duplicados por cliente_id eliminados: %d", antes - len(df))
    log.info("Validación: %d válidas, %d rechazadas", len(df), rechazadas)
    return df


def transformar(crudo: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Separa el CSV plano en las tablas clientes, productos y compras."""
    df = validar(crudo)

    productos = (df[["producto", "categoria"]].drop_duplicates()
                 .rename(columns={"producto": "nombre"}).reset_index(drop=True))
    productos.insert(0, "id", productos.index + 1)

    df = df.merge(productos.rename(columns={"id": "producto_id", "nombre": "producto"}),
                  on=["producto", "categoria"])
    df["grupo_edad"] = pd.cut(
        df.edad, bins=[-1, 24, 34, 44, 54, 64, 120],
        labels=["<=24", "25-34", "35-44", "45-54", "55-64", "65+"],
    ).astype(str)

    clientes = df[COLUMNAS_CLIENTE].rename(columns={"cliente_id": "id"})
    # El dataset trae una compra por cliente: id de compra = id de cliente.
    compras = df[COLUMNAS_COMPRA].copy()
    compras.insert(0, "id", compras.cliente_id)

    log.info("Transformado: %d clientes, %d productos, %d compras",
             len(clientes), len(productos), len(compras))
    return {"clientes": clientes, "productos": productos, "compras": compras}
