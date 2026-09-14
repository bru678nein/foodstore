from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.modulos.categorias.esquemas import CategoriaEntrada, CategoriaSalida
from app.modulos.categorias.repositorio import RepositorioCategorias
from app.persistencia.entidades.categoria import Categoria
from app.persistencia.sesion_trabajo import GestorTransaccion

class ServicioCategorias:
    def __init__(self, repositorio: RepositorioCategorias, gestor: GestorTransaccion) -> None:
        self.repositorio = repositorio
        self.gestor = gestor

    def _obtener(self, categoria_id: int) -> Categoria:
        categoria = self.repositorio.buscar(categoria_id)
        if categoria is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoria no encontrada",
            )
        return categoria

    def _a_salida(self, c: Categoria, hijos: list[CategoriaSalida] | None = None) -> CategoriaSalida:
        return CategoriaSalida(
            id=c.id,
            nombre=c.etiqueta,
            descripcion=c.descripcion,
            imagen_url=c.imagen_url,
            padre_id=c.padre_id,
            hijos=hijos or [],
        )

    def listar_arbol(self) -> list[CategoriaSalida]:
        categorias = self.repositorio.listar()
        nodos: dict[int, CategoriaSalida] = {
            c.id: self._a_salida(c)
            for c in categorias
        }
        raices: list[CategoriaSalida] = []
        for c in categorias:
            nodo = nodos[c.id]
            if c.padre_id is not None and c.padre_id in nodos:
                nodos[c.padre_id].hijos.append(nodo)
            else:
                raices.append(nodo)
        return raices

    def detalle(self, categoria_id: int) -> CategoriaSalida:
        return self._a_salida(self._obtener(categoria_id))

    def crear(self, datos: CategoriaEntrada) -> CategoriaSalida:
        if datos.padre_id is not None and self.repositorio.buscar(datos.padre_id) is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La categoria padre no existe",
            )
        categoria = Categoria(
            etiqueta=datos.nombre,
            descripcion=datos.descripcion,
            imagen_url=datos.imagen_url,
            imagen_id_cdn=datos.imagen_id_cdn,
            padre_id=datos.padre_id,
        )
        self.repositorio.guardar(categoria)
        return self.detalle(categoria.id)

    def actualizar(self, categoria_id: int, datos: CategoriaEntrada) -> CategoriaSalida:
        categoria = self._obtener(categoria_id)
        if datos.padre_id == categoria_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Una categoria no puede ser su propio padre",
            )
        categoria.etiqueta = datos.nombre
        categoria.descripcion = datos.descripcion
        categoria.imagen_url = datos.imagen_url
        categoria.imagen_id_cdn = datos.imagen_id_cdn
        categoria.padre_id = datos.padre_id
        self.repositorio.guardar(categoria)
        return self.detalle(categoria.id)

    def eliminar(self, categoria_id: int) -> None:
        categoria = self._obtener(categoria_id)
        if self.repositorio.tiene_hijos(categoria_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se puede eliminar una categoria con subcategorias activas",
            )
        categoria.eliminado_en = datetime.now(timezone.utc)
        self.repositorio.guardar(categoria)
