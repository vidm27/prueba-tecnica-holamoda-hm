"""Tablas de la base de datos (SQLModel). Fuente única del esquema."""
from sqlmodel import Field, SQLModel


class Cliente(SQLModel, table=True):
    __tablename__ = "clientes"
    id: int = Field(primary_key=True)
    edad: int
    grupo_edad: str
    genero: str
    ubicacion: str
    suscrito: bool
    compras_previas: int
    metodo_pago_preferido: str
    frecuencia_compras: str


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
