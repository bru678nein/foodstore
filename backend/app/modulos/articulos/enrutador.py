from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from app.nucleo.dependencias import requerir_perfil
from app.modulos.articulos.esquemas import (
    ArticuloEntrada,
    ArticuloDetalleSalida,
    ArticuloListaSalida,
    ExistenciasEntrada,
    ImagenGaleria,
    PaginaArticulos,
)
from app.modulos.articulos.repositorio import RepositorioArticulos
from app.modulos.articulos.servicio import ServicioArticulos
from app.modulos.tiempo_real.gestor import gestor_conexiones
from app.persistencia.sesion_trabajo import GestorTransaccion, obtener_gestor

_MSG_CATALOGO = {"evento": "articulo_actualizado"}

enrutador = APIRouter(prefix="/articulos", tags=["articulos"])

_solo_admin = Depends(requerir_perfil("ADMINISTRADOR"))
_gestion_stock = Depends(requerir_perfil("ADMINISTRADOR", "INVENTARIO"))

def obtener_servicio(
    gestor: GestorTransaccion = Depends(obtener_gestor),
) -> ServicioArticulos:
    return ServicioArticulos(RepositorioArticulos(gestor.sesion), gestor)

@enrutador.get("", response_model=PaginaArticulos)
def listar(
    categoria: Optional[int] = Query(default=None),
    disponible: Optional[bool] = Query(default=None),
    q: Optional[str] = Query(default=None),
    pagina: int = Query(default=1, ge=1),
    por_pagina: int = Query(default=20, ge=1, le=100),
    servicio: ServicioArticulos = Depends(obtener_servicio),
) -> PaginaArticulos:
    return servicio.listar(categoria, disponible, q, pagina, por_pagina)

@enrutador.get("/{articulo_id}", response_model=ArticuloDetalleSalida)
def detalle(
    articulo_id: int, servicio: ServicioArticulos = Depends(obtener_servicio)
) -> ArticuloDetalleSalida:
    return servicio.detalle(articulo_id)

@enrutador.post(
    "", response_model=ArticuloDetalleSalida, status_code=status.HTTP_201_CREATED,
    dependencies=[_solo_admin],
)
async def crear(
    datos: ArticuloEntrada,
    gestor: GestorTransaccion = Depends(obtener_gestor),
    servicio: ServicioArticulos = Depends(obtener_servicio),
) -> ArticuloDetalleSalida:
    with gestor:
        resultado = servicio.crear(datos)
    await gestor_conexiones.difundir("ordenes", _MSG_CATALOGO)
    return resultado

@enrutador.put("/{articulo_id}", response_model=ArticuloDetalleSalida, dependencies=[_solo_admin])
async def actualizar(
    articulo_id: int,
    datos: ArticuloEntrada,
    gestor: GestorTransaccion = Depends(obtener_gestor),
    servicio: ServicioArticulos = Depends(obtener_servicio),
) -> ArticuloDetalleSalida:
    with gestor:
        resultado = servicio.actualizar(articulo_id, datos)
    await gestor_conexiones.difundir("ordenes", _MSG_CATALOGO)
    return resultado

@enrutador.delete(
    "/{articulo_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[_solo_admin]
)
async def eliminar(
    articulo_id: int,
    gestor: GestorTransaccion = Depends(obtener_gestor),
    servicio: ServicioArticulos = Depends(obtener_servicio),
) -> None:
    with gestor:
        servicio.eliminar(articulo_id)
    await gestor_conexiones.difundir("ordenes", _MSG_CATALOGO)

@enrutador.patch(
    "/{articulo_id}/existencias", response_model=ArticuloListaSalida,
    dependencies=[_gestion_stock],
)
async def actualizar_existencias(
    articulo_id: int,
    datos: ExistenciasEntrada,
    gestor: GestorTransaccion = Depends(obtener_gestor),
    servicio: ServicioArticulos = Depends(obtener_servicio),
) -> ArticuloListaSalida:
    with gestor:
        resultado = servicio.actualizar_existencias(articulo_id, datos.existencias)
    await gestor_conexiones.difundir("ordenes", _MSG_CATALOGO)
    return resultado

@enrutador.post(
    "/{articulo_id}/galeria", response_model=ImagenGaleria,
    status_code=status.HTTP_201_CREATED, dependencies=[_solo_admin],
)
def subir_imagen(
    articulo_id: int,
    url_imagen: str = Query(...),
    id_cdn: str = Query(...),
    posicion: int = Query(default=0),
    servicio: ServicioArticulos = Depends(obtener_servicio),
) -> ImagenGaleria:
    return servicio.agregar_imagen(articulo_id, url_imagen, id_cdn, posicion)

@enrutador.delete(
    "/{articulo_id}/galeria/{img_id}", status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[_solo_admin],
)
def eliminar_imagen(
    articulo_id: int,
    img_id: int,
    servicio: ServicioArticulos = Depends(obtener_servicio),
) -> None:
    servicio.eliminar_imagen(articulo_id, img_id)
