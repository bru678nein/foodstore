from __future__ import annotations

from typing import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select

from app.nucleo.ajustes import ajustes
from app.nucleo.proteccion import JWTError, decodificar_token
from app.persistencia.entidades.cuenta import Cuenta, CuentaPerfil, Perfil
from app.persistencia.sesion_trabajo import GestorTransaccion, obtener_gestor

esquema_oauth = OAuth2PasswordBearer(tokenUrl=f"{ajustes.prefijo_api}/sesion/iniciar")

_CREDENCIAL_INVALIDA = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="No se pudieron validar las credenciales",
    headers={"WWW-Authenticate": "Bearer"},
)

def obtener_cuenta_activa(
    token: str = Depends(esquema_oauth),
    gestor: GestorTransaccion = Depends(obtener_gestor),
) -> Cuenta:
    try:
        carga = decodificar_token(token)
        identificador = carga.get("sub")
        if identificador is None:
            raise _CREDENCIAL_INVALIDA
        cuenta_id = int(identificador)
    except (JWTError, ValueError):
        raise _CREDENCIAL_INVALIDA

    cuenta = gestor.sesion.get(Cuenta, cuenta_id)
    if cuenta is None or cuenta.eliminado_en is not None:
        raise _CREDENCIAL_INVALIDA
    if not cuenta.habilitado:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="La cuenta se encuentra deshabilitada",
        )
    return cuenta

def perfiles_de_cuenta(gestor: GestorTransaccion, cuenta_id: int) -> list[str]:
    consulta = (
        select(Perfil.nombre)
        .join(CuentaPerfil, CuentaPerfil.perfil_id == Perfil.id)
        .where(CuentaPerfil.cuenta_id == cuenta_id)
    )
    return list(gestor.sesion.exec(consulta).all())

def requerir_perfil(*perfiles: str) -> Callable[..., Cuenta]:

    def verificador(
        cuenta: Cuenta = Depends(obtener_cuenta_activa),
        gestor: GestorTransaccion = Depends(obtener_gestor),
    ) -> Cuenta:
        asignados = set(perfiles_de_cuenta(gestor, cuenta.id))
        if not asignados.intersection(perfiles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No cuenta con los permisos necesarios",
            )
        return cuenta

    return verificador
