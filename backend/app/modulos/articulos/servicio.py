from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException, status

from app.modulos.articulos.esquemas import (
    ArticuloEntrada,
    ArticuloListaSalida,
    ArticuloDetalleSalida,
    CategoriaBasica,
    ComposicionItem,
    ImagenGaleria,
    PaginaArticulos,
)
from app.modulos.articulos.repositorio import RepositorioArticulos
from app.persistencia.entidades.articulo import Articulo, ArticuloImagen
from app.persistencia.sesion_trabajo import GestorTransaccion

class ServicioArticulos:
    def __init__(self, repositorio: RepositorioArticulos, gestor: GestorTransaccion) -> None:
        self.repositorio = repositorio
        self.gestor = gestor

    def _categorias(self, articulo_id: int) -> list[CategoriaBasica]:
        return [
            CategoriaBasica(id=cid, nombre=nombre)
            for cid, nombre in self.repositorio.categorias_con_nombre_de(articulo_id)
        ]

    def _a_lista(self, articulo: Articulo) -> ArticuloListaSalida:
        imagenes = self.repositorio.imagenes_de(articulo.id)
        imagen_principal = imagenes[0].url_imagen if imagenes else None
        return ArticuloListaSalida(
            id=articulo.id,
            titulo=articulo.titulo,
            precio_unitario=articulo.precio_unitario,
            existencias=articulo.existencias,
            disponible=articulo.disponible,
            es_prefabricado=articulo.es_prefabricado,
            categorias=self._categorias(articulo.id),
            imagen_principal=imagen_principal,
        )

    def _a_detalle(self, articulo: Articulo) -> ArticuloDetalleSalida:
        imagenes = self.repositorio.imagenes_de(articulo.id)
        galeria = [
            ImagenGaleria(id=img.id, url=img.url_imagen, orden=img.posicion)
            for img in imagenes
        ]
        imagen_principal = imagenes[0].url_imagen if imagenes else None
        composicion = [
            ComposicionItem(id=cid, denominacion=nombre, extraible=ext, cantidad_gramos=int(cantidad))
            for cid, nombre, ext, cantidad in self.repositorio.composicion_de(articulo.id)
        ]
        return ArticuloDetalleSalida(
            id=articulo.id,
            titulo=articulo.titulo,
            descripcion=articulo.descripcion,
            precio_unitario=articulo.precio_unitario,
            existencias=articulo.existencias,
            disponible=articulo.disponible,
            es_prefabricado=articulo.es_prefabricado,
            categorias=self._categorias(articulo.id),
            imagen_principal=imagen_principal,
            galeria=galeria,
            composicion=composicion,
        )

    def _obtener(self, articulo_id: int) -> Articulo:
        articulo = self.repositorio.buscar(articulo_id)
        if articulo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Articulo no encontrado",
            )
        return articulo

    def listar(
        self,
        categoria_id: Optional[int],
        disponible: Optional[bool],
        texto: Optional[str],
        pagina: int,
        por_pagina: int,
    ) -> PaginaArticulos:
        desplazamiento = (pagina - 1) * por_pagina
        total = self.repositorio.contar(categoria_id, disponible, texto)
        articulos = self.repositorio.listar(categoria_id, disponible, texto, desplazamiento, por_pagina)
        return PaginaArticulos.construir(
            total=total,
            pagina=pagina,
            por_pagina=por_pagina,
            items=[self._a_lista(a) for a in articulos],
        )

    def detalle(self, articulo_id: int) -> ArticuloDetalleSalida:
        return self._a_detalle(self._obtener(articulo_id))

    def _aplicar_relaciones(self, articulo_id: int, datos: ArticuloEntrada) -> None:
        self.repositorio.reemplazar_categorias(articulo_id, datos.categorias)
        self.repositorio.reemplazar_composicion(
            articulo_id,
            [(c.componente_id, c.extraible, c.cantidad_gramos) for c in datos.composicion],
        )

    def crear(self, datos: ArticuloEntrada) -> ArticuloDetalleSalida:
        articulo = Articulo(
            titulo=datos.titulo,
            descripcion=datos.descripcion,
            precio_unitario=datos.precio_unitario,
            existencias=datos.existencias,
            disponible=datos.disponible,
            es_prefabricado=datos.es_prefabricado,
        )
        self.repositorio.guardar(articulo)
        self._aplicar_relaciones(articulo.id, datos)
        return self._a_detalle(articulo)

    def actualizar(self, articulo_id: int, datos: ArticuloEntrada) -> ArticuloDetalleSalida:
        articulo = self._obtener(articulo_id)
        articulo.titulo = datos.titulo
        articulo.descripcion = datos.descripcion
        articulo.precio_unitario = datos.precio_unitario
        articulo.existencias = datos.existencias
        articulo.disponible = datos.disponible
        articulo.es_prefabricado = datos.es_prefabricado
        articulo.modificado_en = datetime.now(timezone.utc)
        self.repositorio.guardar(articulo)
        self._aplicar_relaciones(articulo.id, datos)
        return self._a_detalle(articulo)

    def eliminar(self, articulo_id: int) -> None:
        articulo = self._obtener(articulo_id)
        articulo.eliminado_en = datetime.now(timezone.utc)
        articulo.disponible = False
        self.repositorio.guardar(articulo)

    def actualizar_existencias(self, articulo_id: int, existencias: int) -> ArticuloListaSalida:
        articulo = self._obtener(articulo_id)
        articulo.existencias = existencias
        articulo.modificado_en = datetime.now(timezone.utc)
        self.repositorio.guardar(articulo)
        return self._a_lista(articulo)

    def agregar_imagen(
        self, articulo_id: int, url_imagen: str, id_cdn: str, posicion: int
    ) -> ImagenGaleria:
        self._obtener(articulo_id)
        imagen = ArticuloImagen(
            articulo_id=articulo_id,
            url_imagen=url_imagen,
            id_cdn=id_cdn,
            posicion=posicion,
        )
        self.repositorio.agregar_imagen(imagen)
        return ImagenGaleria(id=imagen.id, url=imagen.url_imagen, orden=imagen.posicion)

    def eliminar_imagen(self, articulo_id: int, imagen_id: int) -> None:
        self._obtener(articulo_id)
        imagen = self.repositorio.buscar_imagen(imagen_id)
        if imagen is None or imagen.articulo_id != articulo_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Imagen no encontrada",
            )
        self.repositorio.eliminar_imagen(imagen)
