from loguru import logger as log
import os
import sys

from sqlalchemy import create_engine

from cargar import cargar
from extraer import extraer
from transformar import transformar


def main() -> int:
    e = os.environ
    url = (f"postgresql+psycopg2://{e['POSTGRES_USER']}:{e['POSTGRES_PASSWORD']}"
           f"@{e['POSTGRES_HOST']}:{e.get('POSTGRES_PORT', '5432')}/{e['POSTGRES_DB']}")
    try:
        crudo = extraer(e.get("CSV_RUTA", "/datos/shopping_trends.csv"))
        cargar(transformar(crudo), create_engine(url))
    except Exception:
        log.exception("ETL falló")
        return 1
    log.info("ETL terminado correctamente")
    return 0


if __name__ == "__main__":
    sys.exit(main())
