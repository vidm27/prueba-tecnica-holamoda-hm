import logging

import pandas as pd
from sqlalchemy import Engine, text
from sqlmodel import Session, SQLModel

from modelos import Cliente, Compra, Producto

log = logging.getLogger(__name__)
ORDEN = [("clientes", Cliente), ("productos", Producto), ("compras", Compra)]  # respeta FKs


def cargar(tablas: dict[str, pd.DataFrame], engine: Engine) -> None:
    """Recarga completa e idempotente en una sola transacción:
    si algo falla, la BD queda como estaba."""
    SQLModel.metadata.create_all(engine)
    with Session(engine) as sesion:
        sesion.execute(text("TRUNCATE compras, clientes, productos"))
        for nombre, modelo in ORDEN:
            sesion.add_all(modelo(**r) for r in tablas[nombre].to_dict("records"))
            sesion.flush()
            log.info("Cargada %s: %d filas", nombre, len(tablas[nombre]))
        sesion.commit()
