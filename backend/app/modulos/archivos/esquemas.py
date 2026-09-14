from __future__ import annotations

from pydantic import BaseModel

class ImagenSubidaSalida(BaseModel):
    url: str
    id_cdn: str
    simulado: bool = False
