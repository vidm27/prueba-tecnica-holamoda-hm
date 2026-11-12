from loguru import logger as log

import pandas as pd
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel

from modelos import Cliente, Compra, HallazgoAuditoria, Producto

ORDEN = [("clientes", Cliente), ("productos", Producto), ("compras", Compra),
         ("auditoria", HallazgoAuditoria)]  # respeta llaves foráneas


def cargar(tablas: dict[str, pd.DataFrame], engine: Engine) -> None:
    """Recarga completa en una sola transacción (Postgres soporta DDL transaccional):
    se recrea el esquema y se insertan los datos; si algo falla, la BD queda como estaba."""
    with Session(engine) as sesion:
        conexion = sesion.connection()
        SQLModel.metadata.drop_all(conexion)
        SQLModel.metadata.create_all(conexion)
        for nombre, modelo in ORDEN:
            sesion.add_all(modelo(**r) for r in tablas[nombre].to_dict("records"))
            sesion.flush()
            log.info("Cargada {}: {} filas", nombre, len(tablas[nombre]))
        sesion.commit()
