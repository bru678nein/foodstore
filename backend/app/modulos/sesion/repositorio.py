from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import select

from app.persistencia.base_repositorio import BaseRepositorio
from app.persistencia.entidades.cuenta import (
    Cuenta,
    CuentaPerfil,
    Perfil,
    TokenRenovacion,
)

class RepositorioSesion(BaseRepositorio[Cuenta]):

    def buscar_cuenta_por_correo(self, correo: str) -> Optional[Cuenta]:
        consulta = select(Cuenta).where(
            Cuenta.correo == correo, Cuenta.eliminado_en.is_(None)
        )
        return self.sesion.exec(consulta).first()

    def buscar_cuenta_por_id(self, cuenta_id: int) -> Optional[Cuenta]:
        consulta = select(Cuenta).where(
            Cuenta.id == cuenta_id, Cuenta.eliminado_en.is_(None)
        )
        return self.sesion.exec(consulta).first()

    def crear_cuenta(self, cuenta: Cuenta) -> Cuenta:
        return self.guardar(cuenta)

    def buscar_perfil_por_nombre(self, nombre: str) -> Optional[Perfil]:
        return self.sesion.exec(
            select(Perfil).where(Perfil.nombre == nombre)
        ).first()

    def consultar_perfiles(self, cuenta_id: int) -> list[str]:
        consulta = (
            select(Perfil.nombre)
            .join(CuentaPerfil, CuentaPerfil.perfil_id == Perfil.id)
            .where(CuentaPerfil.cuenta_id == cuenta_id)
        )
        return list(self.sesion.exec(consulta).all())

    def asignar_perfil(self, cuenta_id: int, perfil: Perfil) -> None:
        existente = self.sesion.get(CuentaPerfil, (cuenta_id, perfil.id))
        if existente is None:
            self.sesion.add(
                CuentaPerfil(cuenta_id=cuenta_id, perfil_id=perfil.id)
            )
            self.sesion.flush()

    def guardar_token(self, token: TokenRenovacion) -> TokenRenovacion:
        return self.guardar(token)

    def buscar_token(self, valor: str) -> Optional[TokenRenovacion]:
        return self.sesion.exec(
            select(TokenRenovacion).where(TokenRenovacion.valor == valor)
        ).first()

    def revocar_token(self, token: TokenRenovacion) -> None:
        token.revocado = True
        self.guardar(token)

    @staticmethod
    def token_vigente(token: TokenRenovacion) -> bool:
        if token.revocado:
            return False
        vence = token.vence_en
        if vence.tzinfo is None:
            vence = vence.replace(tzinfo=timezone.utc)
        return vence > datetime.now(timezone.utc)
