from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.nucleo.dependencias import requerir_perfil
from app.modulos.cuentas.esquemas import (
    AsignarPerfilEntrada,
    CambioEstadoEntrada,
    CuentaDetalle,
)
from app.modulos.cuentas.repositorio import RepositorioCuentas
from app.modulos.cuentas.servicio import ServicioCuentas
from app.persistencia.sesion_trabajo import GestorTransaccion, obtener_gestor

enrutador = APIRouter(
    prefix="/cuentas",
    tags=["cuentas"],
    dependencies=[Depends(requerir_perfil("ADMINISTRADOR"))],
)

def obtener_servicio(
    gestor: GestorTransaccion = Depends(obtener_gestor),
) -> ServicioCuentas:
    return ServicioCuentas(RepositorioCuentas(gestor.sesion), gestor)

@enrutador.get("", response_model=list[CuentaDetalle])
def listar(servicio: ServicioCuentas = Depends(obtener_servicio)) -> list[CuentaDetalle]:
    return servicio.listar()

@enrutador.get("/{cuenta_id}", response_model=CuentaDetalle)
def detalle(
    cuenta_id: int, servicio: ServicioCuentas = Depends(obtener_servicio)
) -> CuentaDetalle:
    return servicio.detalle(cuenta_id)

@enrutador.patch("/{cuenta_id}/estado", response_model=CuentaDetalle)
def cambiar_estado(
    cuenta_id: int,
    datos: CambioEstadoEntrada,
    servicio: ServicioCuentas = Depends(obtener_servicio),
) -> CuentaDetalle:
    return servicio.cambiar_estado(cuenta_id, datos.habilitado)

@enrutador.patch("/{cuenta_id}/perfil", response_model=CuentaDetalle)
def asignar_perfil(
    cuenta_id: int,
    datos: AsignarPerfilEntrada,
    servicio: ServicioCuentas = Depends(obtener_servicio),
) -> CuentaDetalle:
    return servicio.asignar_perfil(cuenta_id, datos.perfil)

@enrutador.delete("/{cuenta_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(
    cuenta_id: int, servicio: ServicioCuentas = Depends(obtener_servicio)
) -> None:
    servicio.eliminar(cuenta_id)
