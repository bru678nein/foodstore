from __future__ import annotations

from typing import Optional

from sqlmodel import select

from app.persistencia.base_repositorio import BaseRepositorio
from app.persistencia.entidades.componente import Componente

class RepositorioComponentes(BaseRepositorio[Componente]):
    def listar(self) -> list[Componente]:
        consulta = select(Componente).where(Componente.eliminado_en.is_(None))
        return list(self.sesion.exec(consulta).all())

    def buscar(self, componente_id: int) -> Optional[Componente]:
        consulta = select(Componente).where(
            Componente.id == componente_id, Componente.eliminado_en.is_(None)
        )
        return self.sesion.exec(consulta).first()
