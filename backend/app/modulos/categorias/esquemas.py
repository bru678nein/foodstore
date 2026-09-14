from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

class CategoriaEntrada(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: Optional[str] = Field(default=None, max_length=500)
    imagen_url: Optional[str] = None
    imagen_id_cdn: Optional[str] = None
    padre_id: Optional[int] = None

class CategoriaSalida(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    padre_id: Optional[int] = None
    hijos: list["CategoriaSalida"] = []

CategoriaSalida.model_rebuild()
