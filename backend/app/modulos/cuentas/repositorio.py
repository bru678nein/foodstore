from __future__ import annotations

from typing import Optional

from sqlmodel import delete, select

from app.persistencia.base_repositorio import BaseRepositorio
from app.persistencia.entidades.cuenta import (
    Cuenta,
    CuentaPerfil,
    Perfil,
)

class RepositorioCuentas(BaseRepositorio[Cuenta]):
    def listar_todas(self) -> list[Cuenta]:
        consulta = select(Cuenta).where(Cuenta.eliminado_en.is_(None))
        return list(self.sesion.exec(consulta).all())

    def buscar_por_id(self, cuenta_id: int) -> Optional[Cuenta]:
        consulta = select(Cuenta).where(
            Cuenta.id == cuenta_id, Cuenta.eliminado_en.is_(None)
        )
        return self.sesion.exec(consulta).first()

    def consultar_perfiles(self, cuenta_id: int) -> list[str]:
        consulta = (
            select(Perfil.nombre)
            .join(CuentaPerfil, CuentaPerfil.perfil_id == Perfil.id)
            .where(CuentaPerfil.cuenta_id == cuenta_id)
        )
        return list(self.sesion.exec(consulta).all())

    def buscar_perfil_por_nombre(self, nombre: str) -> Optional[Perfil]:
        return self.sesion.exec(
            select(Perfil).where(Perfil.nombre == nombre)
        ).first()

    def reemplazar_perfiles(self, cuenta_id: int, perfil: Perfil) -> None:
        self.sesion.exec(
            delete(CuentaPerfil).where(CuentaPerfil.cuenta_id == cuenta_id)
        )
        self.sesion.add(CuentaPerfil(cuenta_id=cuenta_id, perfil_id=perfil.id))
        self.sesion.flush()
