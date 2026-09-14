from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

class Categoria(SQLModel, table=True):

    __tablename__ = "categoria"

    id: Optional[int] = Field(default=None, primary_key=True)
    etiqueta: str = Field(max_length=100, index=True)
    descripcion: Optional[str] = Field(default=None, max_length=500)
    imagen_url: Optional[str] = Field(default=None, max_length=500)
    imagen_id_cdn: Optional[str] = Field(default=None, max_length=200)
    padre_id: Optional[int] = Field(default=None, foreign_key="categoria.id")
    eliminado_en: Optional[datetime] = Field(default=None)
