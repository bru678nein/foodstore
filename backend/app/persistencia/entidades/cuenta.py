from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel

def _instante_actual() -> datetime:
    return datetime.now(timezone.utc)

class Perfil(SQLModel, table=True):

    __tablename__ = "perfil"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50, unique=True, index=True)

class CuentaPerfil(SQLModel, table=True):

    __tablename__ = "cuenta_perfil"

    cuenta_id: int = Field(foreign_key="cuenta.id", primary_key=True)
    perfil_id: int = Field(foreign_key="perfil.id", primary_key=True)

class Cuenta(SQLModel, table=True):

    __tablename__ = "cuenta"

    id: Optional[int] = Field(default=None, primary_key=True)
    correo: str = Field(index=True, unique=True, max_length=255)
    clave_hash: str = Field(max_length=255)
    nombre_completo: str = Field(max_length=100)
    habilitado: bool = Field(default=True)
    creado_en: datetime = Field(default_factory=_instante_actual)
    modificado_en: datetime = Field(default_factory=_instante_actual)
    eliminado_en: Optional[datetime] = Field(default=None)

class TokenRenovacion(SQLModel, table=True):

    __tablename__ = "token_renovacion"

    id: Optional[int] = Field(default=None, primary_key=True)
    valor: str = Field(max_length=512, unique=True, index=True)
    cuenta_id: int = Field(foreign_key="cuenta.id")
    vence_en: datetime
    revocado: bool = Field(default=False)
    creado_en: datetime = Field(default_factory=_instante_actual)
