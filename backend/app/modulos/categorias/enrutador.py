from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.nucleo.dependencias import requerir_perfil
from app.modulos.categorias.esquemas import CategoriaEntrada, CategoriaSalida
from app.modulos.categorias.repositorio import RepositorioCategorias
from app.modulos.categorias.servicio import ServicioCategorias
from app.persistencia.sesion_trabajo import GestorTransaccion, obtener_gestor

enrutador = APIRouter(prefix="/categorias", tags=["categorias"])

_solo_admin = Depends(requerir_perfil("ADMINISTRADOR"))

def obtener_servicio(
    gestor: GestorTransaccion = Depends(obtener_gestor),
) -> ServicioCategorias:
    return ServicioCategorias(RepositorioCategorias(gestor.sesion), gestor)

@enrutador.get("", response_model=list[CategoriaSalida])
def listar(servicio: ServicioCategorias = Depends(obtener_servicio)) -> list[CategoriaSalida]:
    return servicio.listar_arbol()

@enrutador.get("/{categoria_id}", response_model=CategoriaSalida)
def detalle(
    categoria_id: int, servicio: ServicioCategorias = Depends(obtener_servicio)
) -> CategoriaSalida:
    return servicio.detalle(categoria_id)

@enrutador.post(
    "", response_model=CategoriaSalida, status_code=status.HTTP_201_CREATED,
    dependencies=[_solo_admin],
)
def crear(
    datos: CategoriaEntrada, servicio: ServicioCategorias = Depends(obtener_servicio)
) -> CategoriaSalida:
    return servicio.crear(datos)

@enrutador.put("/{categoria_id}", response_model=CategoriaSalida, dependencies=[_solo_admin])
def actualizar(
    categoria_id: int,
    datos: CategoriaEntrada,
    servicio: ServicioCategorias = Depends(obtener_servicio),
) -> CategoriaSalida:
    return servicio.actualizar(categoria_id, datos)

@enrutador.delete(
    "/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[_solo_admin]
)
def eliminar(
    categoria_id: int, servicio: ServicioCategorias = Depends(obtener_servicio)
) -> None:
    servicio.eliminar(categoria_id)
