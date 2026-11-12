from loguru import logger as log

import pandas as pd



def extraer(ruta: str) -> pd.DataFrame:
    """Lee el CSV crudo tal cual viene (sin transformar)."""
    df = pd.read_csv(ruta)
    log.info("Extraídas {} filas y {} columnas de {}", len(df), df.shape[1], ruta)
    return df
