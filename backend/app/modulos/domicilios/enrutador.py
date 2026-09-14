from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.nucleo.dependencias import obtener_cuenta_activa
from app.modulos.domicilios.esquemas import DomicilioEntrada, DomicilioSalida
from app.modulos.domicilios.repositorio import RepositorioDomicilios
from app.modulos.domicilios.servicio import ServicioDomicilios
from app.persistencia.entidades.cuenta import Cuenta
from app.persistencia.sesion_trabajo import GestorTransaccion, obtener_gestor

enrutador = APIRouter(prefix="/domicilios", tags=["domicilios"])

def obtener_servicio(
    gestor: GestorTransaccion = Depends(obtener_gestor),
) -> ServicioDomicilios:
    return ServicioDomicilios(RepositorioDomicilios(gestor.sesion), gestor)

@enrutador.get("", response_model=list[DomicilioSalida])
def listar(
    cuenta: Cuenta = Depends(obtener_cuenta_activa),
    servicio: ServicioDomicilios = Depends(obtener_servicio),
) -> list[DomicilioSalida]:
    return servicio.listar(cuenta.id)

@enrutador.post("", response_model=DomicilioSalida, status_code=status.HTTP_201_CREATED)
def crear(
    datos: DomicilioEntrada,
    cuenta: Cuenta = Depends(obtener_cuenta_activa),
    servicio: ServicioDomicilios = Depends(obtener_servicio),
) -> DomicilioSalida:
    return servicio.crear(cuenta.id, datos)

@enrutador.put("/{domicilio_id}", response_model=DomicilioSalida)
def actualizar(
    domicilio_id: int,
    datos: DomicilioEntrada,
    cuenta: Cuenta = Depends(obtener_cuenta_activa),
    servicio: ServicioDomicilios = Depends(obtener_servicio),
) -> DomicilioSalida:
    return servicio.actualizar(domicilio_id, cuenta.id, datos)

@enrutador.delete("/{domicilio_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(
    domicilio_id: int,
    cuenta: Cuenta = Depends(obtener_cuenta_activa),
    servicio: ServicioDomicilios = Depends(obtener_servicio),
) -> None:
    servicio.eliminar(domicilio_id, cuenta.id)

@enrutador.patch("/{domicilio_id}/predeterminado", response_model=DomicilioSalida)
def marcar_predeterminado(
    domicilio_id: int,
    cuenta: Cuenta = Depends(obtener_cuenta_activa),
    servicio: ServicioDomicilios = Depends(obtener_servicio),
) -> DomicilioSalida:
    return servicio.marcar_predeterminado(domicilio_id, cuenta.id)
