from __future__ import annotations

from typing import Optional

from sqlmodel import select

from app.persistencia.base_repositorio import BaseRepositorio
from app.persistencia.entidades.categoria import Categoria

class RepositorioCategorias(BaseRepositorio[Categoria]):
    def listar(self) -> list[Categoria]:
        consulta = select(Categoria).where(Categoria.eliminado_en.is_(None))
        return list(self.sesion.exec(consulta).all())

    def buscar(self, categoria_id: int) -> Optional[Categoria]:
        consulta = select(Categoria).where(
            Categoria.id == categoria_id, Categoria.eliminado_en.is_(None)
        )
        return self.sesion.exec(consulta).first()

    def tiene_hijos(self, categoria_id: int) -> bool:
        consulta = select(Categoria.id).where(
            Categoria.padre_id == categoria_id, Categoria.eliminado_en.is_(None)
        )
        return self.sesion.exec(consulta).first() is not None
