from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.nucleo.dependencias import obtener_cuenta_activa, requerir_perfil
from app.modulos.componentes.esquemas import ComponenteEntrada, ComponenteSalida
from app.modulos.componentes.repositorio import RepositorioComponentes
from app.modulos.componentes.servicio import ServicioComponentes
from app.persistencia.sesion_trabajo import GestorTransaccion, obtener_gestor

enrutador = APIRouter(prefix="/componentes", tags=["componentes"])

_gestion = Depends(requerir_perfil("ADMINISTRADOR", "INVENTARIO"))
_solo_admin = Depends(requerir_perfil("ADMINISTRADOR"))

def obtener_servicio(
    gestor: GestorTransaccion = Depends(obtener_gestor),
) -> ServicioComponentes:
    return ServicioComponentes(RepositorioComponentes(gestor.sesion), gestor)

@enrutador.get(
    "", response_model=list[ComponenteSalida],
    dependencies=[Depends(obtener_cuenta_activa)],
)
def listar(
    servicio: ServicioComponentes = Depends(obtener_servicio),
) -> list[ComponenteSalida]:
    return servicio.listar()

@enrutador.post(
    "", response_model=ComponenteSalida, status_code=status.HTTP_201_CREATED,
    dependencies=[_gestion],
)
def crear(
    datos: ComponenteEntrada,
    servicio: ServicioComponentes = Depends(obtener_servicio),
) -> ComponenteSalida:
    return servicio.crear(datos)

@enrutador.put(
    "/{componente_id}", response_model=ComponenteSalida, dependencies=[_gestion]
)
def actualizar(
    componente_id: int,
    datos: ComponenteEntrada,
    servicio: ServicioComponentes = Depends(obtener_servicio),
) -> ComponenteSalida:
    return servicio.actualizar(componente_id, datos)

@enrutador.delete(
    "/{componente_id}", status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[_solo_admin],
)
def eliminar(
    componente_id: int,
    servicio: ServicioComponentes = Depends(obtener_servicio),
) -> None:
    servicio.eliminar(componente_id)
