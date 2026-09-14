from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class CuentaDetalle(BaseModel):
    id: int
    correo: str
    nombre_completo: str
    habilitado: bool
    perfiles: list[str] = []
    creado_en: Optional[datetime] = None

class CambioEstadoEntrada(BaseModel):
    habilitado: bool

class AsignarPerfilEntrada(BaseModel):
    perfil: str
