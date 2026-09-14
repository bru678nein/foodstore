from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

class Domicilio(SQLModel, table=True):

    __tablename__ = "domicilio"

    id: Optional[int] = Field(default=None, primary_key=True)
    cuenta_id: int = Field(foreign_key="cuenta.id", index=True)
    via: str = Field(max_length=200)
    altura: str = Field(max_length=20)
    localidad: str = Field(max_length=100)
    provincia: str = Field(max_length=100)
    codigo_postal: Optional[str] = Field(default=None, max_length=20)
    es_predeterminado: bool = Field(default=False)
    eliminado_en: Optional[datetime] = Field(default=None)
