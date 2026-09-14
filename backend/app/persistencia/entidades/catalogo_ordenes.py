from __future__ import annotations

from sqlmodel import Field, SQLModel

class EstadoPedido(SQLModel, table=True):

    __tablename__ = "estado_pedido"

    codigo: str = Field(max_length=20, primary_key=True)
    descripcion: str = Field(max_length=100)
    orden: int
    es_terminal: bool = Field(default=False)

class FormaPago(SQLModel, table=True):

    __tablename__ = "forma_pago"

    codigo: str = Field(max_length=20, primary_key=True)
    descripcion: str = Field(max_length=100)
    habilitada: bool = Field(default=True)
