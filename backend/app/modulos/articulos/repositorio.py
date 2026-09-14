from __future__ import annotations

from typing import Optional

from sqlmodel import delete, func, select

from app.persistencia.base_repositorio import BaseRepositorio
from app.persistencia.entidades.articulo import (
    Articulo,
    ArticuloImagen,
    ArticuloCategoria,
    ComposicionArticulo,
)
from app.persistencia.entidades.categoria import Categoria
from app.persistencia.entidades.componente import Componente

class RepositorioArticulos(BaseRepositorio[Articulo]):

    def _consulta_base(self, categoria_id: Optional[int], disponible: Optional[bool], texto: Optional[str]):
        consulta = select(Articulo).where(Articulo.eliminado_en.is_(None))
        if disponible is not None:
            consulta = consulta.where(Articulo.disponible == disponible)
        if texto:
            patron = f"%{texto.lower()}%"
            consulta = consulta.where(func.lower(Articulo.titulo).like(patron))
        if categoria_id is not None:
            consulta = consulta.join(
                ArticuloCategoria, ArticuloCategoria.articulo_id == Articulo.id
            ).where(ArticuloCategoria.categoria_id == categoria_id)
        return consulta

    def contar(self, categoria_id, disponible, texto) -> int:
        consulta = self._consulta_base(categoria_id, disponible, texto)
        return len(list(self.sesion.exec(consulta).all()))

    def listar(self, categoria_id, disponible, texto, desplazamiento, limite) -> list[Articulo]:
        consulta = (
            self._consulta_base(categoria_id, disponible, texto)
            .offset(desplazamiento)
            .limit(limite)
        )
        return list(self.sesion.exec(consulta).all())

    def buscar(self, articulo_id: int) -> Optional[Articulo]:
        consulta = select(Articulo).where(
            Articulo.id == articulo_id, Articulo.eliminado_en.is_(None)
        )
        return self.sesion.exec(consulta).first()

    def categorias_de(self, articulo_id: int) -> list[int]:
        consulta = select(ArticuloCategoria.categoria_id).where(
            ArticuloCategoria.articulo_id == articulo_id
        )
        return list(self.sesion.exec(consulta).all())

    def categorias_con_nombre_de(self, articulo_id: int) -> list[tuple[int, str]]:
        consulta = (
            select(Categoria.id, Categoria.etiqueta)
            .join(ArticuloCategoria, ArticuloCategoria.categoria_id == Categoria.id)
            .where(ArticuloCategoria.articulo_id == articulo_id)
            .where(Categoria.eliminado_en.is_(None))
        )
        return list(self.sesion.exec(consulta).all())

    def reemplazar_categorias(self, articulo_id: int, categorias: list[int]) -> None:
        self.sesion.exec(
            delete(ArticuloCategoria).where(ArticuloCategoria.articulo_id == articulo_id)
        )
        for categoria_id in set(categorias):
            self.sesion.add(
                ArticuloCategoria(articulo_id=articulo_id, categoria_id=categoria_id)
            )
        self.sesion.flush()

    def composicion_de(self, articulo_id: int) -> list[tuple[int, str, bool, int]]:
        consulta = (
            select(
                ComposicionArticulo.componente_id,
                Componente.denominacion,
                ComposicionArticulo.extraible,
                ComposicionArticulo.cantidad,
            )
            .join(Componente, Componente.id == ComposicionArticulo.componente_id)
            .where(ComposicionArticulo.articulo_id == articulo_id)
        )
        return list(self.sesion.exec(consulta).all())

    def reemplazar_composicion(
        self, articulo_id: int, items: list[tuple[int, bool, int]]
    ) -> None:
        self.sesion.exec(
            delete(ComposicionArticulo).where(
                ComposicionArticulo.articulo_id == articulo_id
            )
        )
        for componente_id, extraible, cantidad_gramos in items:
            self.sesion.add(
                ComposicionArticulo(
                    articulo_id=articulo_id,
                    componente_id=componente_id,
                    extraible=extraible,
                    cantidad=cantidad_gramos,
                )
            )
        self.sesion.flush()

    def nombre_componente(self, componente_id: int) -> Optional[str]:
        comp = self.sesion.get(Componente, componente_id)
        return comp.denominacion if comp else None

    def imagenes_de(self, articulo_id: int) -> list[ArticuloImagen]:
        consulta = (
            select(ArticuloImagen)
            .where(ArticuloImagen.articulo_id == articulo_id)
            .order_by(ArticuloImagen.posicion)
        )
        return list(self.sesion.exec(consulta).all())

    def agregar_imagen(self, imagen: ArticuloImagen) -> ArticuloImagen:
        return self.guardar(imagen)

    def buscar_imagen(self, imagen_id: int) -> Optional[ArticuloImagen]:
        return self.sesion.get(ArticuloImagen, imagen_id)

    def eliminar_imagen(self, imagen: ArticuloImagen) -> None:
        self.eliminar(imagen)
