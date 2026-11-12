import logging

import pandas as pd

log = logging.getLogger(__name__)


def extraer(ruta: str) -> pd.DataFrame:
    """Lee el CSV crudo tal cual viene (sin transformar)."""
    df = pd.read_csv(ruta)
    log.info("Extraídas %d filas y %d columnas de %s", len(df), df.shape[1], ruta)
    return df
