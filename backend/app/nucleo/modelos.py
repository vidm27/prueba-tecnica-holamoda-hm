"""Modelos ORM de lectura. El ETL es el único que escribe; este archivo describe las mismas tablas."""
from datetime import datetime

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class Cliente(SQLModel, table=True):
    __tablename__ = "clientes"
    id: int = Field(primary_key=True)
    edad: int
    grupo_edad: str
    genero: str
    ubicacion: str = Field(index=True)
    suscrito: bool
    compras_previas: int
    metodo_pago_preferido: str
    frecuencia_compras: str
    compras_por_anio: int
    gasto_anual_estimado: float
    nivel_valor: str = Field(index=True)


class Producto(SQLModel, table=True):
    __tablename__ = "productos"
    id: int = Field(primary_key=True)
    nombre: str
    categoria: str = Field(index=True)


class Compra(SQLModel, table=True):
    __tablename__ = "compras"
    id: int = Field(primary_key=True)
    cliente_id: int = Field(foreign_key="clientes.id", index=True)
    producto_id: int = Field(foreign_key="productos.id", index=True)
    monto_usd: float
    talla: str
    color: str
    temporada: str = Field(index=True)
    calificacion: float
    tipo_envio: str
    descuento: bool
    codigo_promo: bool
    metodo_pago: str


class HallazgoAuditoria(SQLModel, table=True):
    __tablename__ = "auditoria"
    id: int | None = Field(default=None, primary_key=True)
    regla: str
    descripcion: str
    severidad: str
    filas_afectadas: int
    total_filas: int
    evidencia: dict = Field(sa_column=Column(JSON, nullable=False))
    ejecutado_en: datetime
