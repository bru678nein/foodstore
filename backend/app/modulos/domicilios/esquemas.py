from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

class DomicilioEntrada(BaseModel):
    via: str = Field(min_length=1, max_length=200)
    altura: str = Field(min_length=1, max_length=20)
    localidad: str = Field(min_length=1, max_length=100)
    provincia: str = Field(min_length=1, max_length=100)
    codigo_postal: Optional[str] = Field(default=None, max_length=20)
    es_predeterminado: bool = False

class DomicilioSalida(BaseModel):
    id: int
    via: str
    altura: str
    localidad: str
    provincia: str
    codigo_postal: Optional[str] = None
    es_predeterminado: bool
