from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.nucleo.ajustes import ajustes
_contexto_clave = CryptContext(schemes=["bcrypt"], deprecated="auto")

def cifrar_clave(clave: str) -> str:
    return _contexto_clave.hash(clave)

def verificar_clave(clave: str, hash_almacenado: str) -> bool:
    try:
        return _contexto_clave.verify(clave, hash_almacenado)
    except ValueError:
        return False

def generar_token_acceso(datos: dict[str, Any]) -> str:
    carga = datos.copy()
    expira = datetime.now(timezone.utc) + timedelta(minutes=ajustes.minutos_acceso)
    carga.update({"exp": expira, "tipo": "acceso"})
    return jwt.encode(carga, ajustes.clave_secreta, algorithm=ajustes.algoritmo)

def generar_token_renovacion() -> str:
    return secrets.token_urlsafe(64)

def decodificar_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, ajustes.clave_secreta, algorithms=[ajustes.algoritmo])

__all__ = [
    "cifrar_clave",
    "verificar_clave",
    "generar_token_acceso",
    "generar_token_renovacion",
    "decodificar_token",
    "JWTError",
]
