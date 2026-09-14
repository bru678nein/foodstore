from __future__ import annotations

from typing import Optional

from sqlmodel import select

from app.persistencia.base_repositorio import BaseRepositorio
from app.persistencia.entidades.domicilio import Domicilio

class RepositorioDomicilios(BaseRepositorio[Domicilio]):
    def listar_por_cuenta(self, cuenta_id: int) -> list[Domicilio]:
        consulta = select(Domicilio).where(
            Domicilio.cuenta_id == cuenta_id,
            Domicilio.eliminado_en.is_(None),
        )
        return list(self.sesion.exec(consulta).all())

    def buscar(self, domicilio_id: int, cuenta_id: int) -> Optional[Domicilio]:
        consulta = select(Domicilio).where(
            Domicilio.id == domicilio_id,
            Domicilio.cuenta_id == cuenta_id,
            Domicilio.eliminado_en.is_(None),
        )
        return self.sesion.exec(consulta).first()

    def quitar_predeterminado(self, cuenta_id: int) -> None:
        for dom in self.listar_por_cuenta(cuenta_id):
            if dom.es_predeterminado:
                dom.es_predeterminado = False
                self.sesion.add(dom)
        self.sesion.flush()
