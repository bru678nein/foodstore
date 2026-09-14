from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field

class RegistroEntrada(BaseModel):
    correo: EmailStr
    contrasena: str = Field(min_length=8, max_length=128, alias="contrasena")
    nombre_completo: str = Field(min_length=1, max_length=100)

    model_config = {"populate_by_name": True}

class InicioSesionEntrada(BaseModel):
    correo: EmailStr
    contrasena: str

class RenovarEntrada(BaseModel):
    token_renovacion: str

class CerrarEntrada(BaseModel):
    token_renovacion: str

class CuentaBasica(BaseModel):
    id: int
    correo: str
    nombre_completo: str
    perfiles: list[str] = []

class RespuestaToken(BaseModel):
    token_acceso: str
    token_renovacion: str
    tipo: str = "portador"
    cuenta: CuentaBasica

class RespuestaAcceso(BaseModel):
    token_acceso: str
    tipo: str = "portador"
