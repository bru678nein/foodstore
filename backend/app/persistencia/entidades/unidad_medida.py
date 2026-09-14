from __future__ import annotations

from typing import Optional

from sqlmodel import Field, SQLModel

class UnidadMedida(SQLModel, table=True):

    __tablename__ = "unidad_medida"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50, unique=True)
    simbolo: str = Field(max_length=10, unique=True)
    tipo: str = Field(max_length=20)
