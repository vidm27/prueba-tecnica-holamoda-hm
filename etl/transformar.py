from loguru import logger as log

import pandas as pd
from pydantic import ValidationError

from auditar import auditar
from esquemas import FilaCruda


# "Bi-Weekly" se interpreta como cada dos semanas (igual que "Fortnightly").
COMPRAS_POR_ANIO = {"Weekly": 52, "Bi-Weekly": 26, "Fortnightly": 26, "Monthly": 12,
                    "Quarterly": 4, "Every 3 Months": 4, "Annually": 1}
NIVELES_VALOR = ["Bronce", "Plata", "Oro", "Platino"]

COLUMNAS_CLIENTE = ["cliente_id", "edad", "grupo_edad", "genero", "ubicacion", "suscrito",
                    "compras_previas", "metodo_pago_preferido", "frecuencia_compras",
                    "compras_por_anio", "gasto_anual_estimado", "nivel_valor"]
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
            log.warning("Fila {} rechazada: {}", i + 2, e.errors()[0]["loc"])  # +2: cabecera y base 1
    df = pd.DataFrame(validas, columns=list(FilaCruda.model_fields))
    antes = len(df)
    df = df.drop_duplicates("cliente_id")
    if antes != len(df):
        log.warning("Duplicados por cliente_id eliminados: {}", antes - len(df))
    log.info("Validación: {} válidas, {} rechazadas", len(df), rechazadas)
    return df


def enriquecer(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega columnas derivadas: grupo de edad y segmentación por valor."""
    df = df.copy()
    df["grupo_edad"] = pd.cut(
        df.edad, bins=[-1, 24, 34, 44, 54, 64, 120],
        labels=["<=24", "25-34", "35-44", "45-54", "55-64", "65+"],
    ).astype(str)
    desconocidas = set(df.frecuencia_compras) - set(COMPRAS_POR_ANIO)
    if desconocidas:
        raise ValueError(f"Frecuencias de compra no mapeadas: {sorted(desconocidas)}")
    df["compras_por_anio"] = df.frecuencia_compras.map(COMPRAS_POR_ANIO)
    df["gasto_anual_estimado"] = df.monto_usd * df.compras_por_anio
    # Cuartiles por percentil: funciona con cualquier tamaño y con empates.
    df["nivel_valor"] = pd.cut(df.gasto_anual_estimado.rank(pct=True),
                               bins=[0, .25, .5, .75, 1], labels=NIVELES_VALOR).astype(str)
    return df


def separar(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Separa el dataset plano en las tablas clientes, productos y compras."""
    productos = (df[["producto", "categoria"]].drop_duplicates()
                 .rename(columns={"producto": "nombre"}).reset_index(drop=True))
    productos.insert(0, "id", productos.index + 1)

    df = df.merge(productos.rename(columns={"id": "producto_id", "nombre": "producto"}),
                  on=["producto", "categoria"])
    clientes = df[COLUMNAS_CLIENTE].rename(columns={"cliente_id": "id"})
    # El dataset trae una compra por cliente: id de compra = id de cliente.
    compras = df[COLUMNAS_COMPRA].copy()
    compras.insert(0, "id", compras.cliente_id)
    return {"clientes": clientes, "productos": productos, "compras": compras}


def transformar(crudo: pd.DataFrame) -> dict[str, pd.DataFrame]:
    df = enriquecer(validar(crudo))
    tablas = separar(df)
    tablas["auditoria"] = auditar(df)
    log.info("Transformado: {}", {k: len(v) for k, v in tablas.items()})
    return tablas
