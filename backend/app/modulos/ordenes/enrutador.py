from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.nucleo.dependencias import (
    obtener_cuenta_activa,
    perfiles_de_cuenta,
    requerir_perfil,
)
from app.modulos.ordenes.esquemas import (
    CambioEstadoEntrada,
    CrearOrdenEntrada,
    RespuestaBitacora,
    RespuestaOrden,
)
from app.modulos.ordenes.repositorio import RepositorioOrdenes
from app.modulos.ordenes.servicio import ServicioOrdenes
from app.modulos.tiempo_real.gestor import gestor_conexiones
from app.persistencia.entidades.cuenta import Cuenta
from app.persistencia.sesion_trabajo import GestorTransaccion, obtener_gestor

enrutador = APIRouter(prefix="/ordenes", tags=["ordenes"])

_PERFILES_GESTORES = {"ADMINISTRADOR", "DESPACHO"}

def obtener_servicio(
    gestor: GestorTransaccion = Depends(obtener_gestor),
) -> ServicioOrdenes:
    return ServicioOrdenes(RepositorioOrdenes(gestor.sesion), gestor)

async def _difundir_orden(orden: RespuestaOrden, evento: str) -> None:
    mensaje = {
        "evento": evento,
        "orden_id": orden.id,
        "estado": orden.estado_actual,
        "total": str(orden.total),
    }
    canales = {"ordenes", f"orden:{orden.id}", f"cuenta:{orden.cuenta_id}"}
    await gestor_conexiones.difundir_multiples(canales, mensaje)

@enrutador.post(
    "", response_model=RespuestaOrden, status_code=status.HTTP_201_CREATED
)
async def crear(
    datos: CrearOrdenEntrada,
    cuenta: Cuenta = Depends(requerir_perfil("COMPRADOR", "ADMINISTRADOR")),
    gestor: GestorTransaccion = Depends(obtener_gestor),
    servicio: ServicioOrdenes = Depends(obtener_servicio),
) -> RespuestaOrden:
    with gestor:
        orden = servicio.crear_orden(cuenta.id, datos)
    await _difundir_orden(orden, "orden_creada")
    return orden

@enrutador.get("/mis-ordenes", response_model=list[RespuestaOrden])
def mis_ordenes(
    cuenta: Cuenta = Depends(requerir_perfil("COMPRADOR", "ADMINISTRADOR")),
    servicio: ServicioOrdenes = Depends(obtener_servicio),
) -> list[RespuestaOrden]:
    return servicio.listar_mias(cuenta.id)

@enrutador.get(
    "", response_model=list[RespuestaOrden],
    dependencies=[Depends(requerir_perfil("ADMINISTRADOR", "DESPACHO"))],
)
def listar(
    servicio: ServicioOrdenes = Depends(obtener_servicio),
) -> list[RespuestaOrden]:
    return servicio.listar_todas()

@enrutador.get("/{orden_id}", response_model=RespuestaOrden)
def detalle(
    orden_id: int,
    cuenta: Cuenta = Depends(obtener_cuenta_activa),
    gestor: GestorTransaccion = Depends(obtener_gestor),
    servicio: ServicioOrdenes = Depends(obtener_servicio),
) -> RespuestaOrden:
    perfiles = set(perfiles_de_cuenta(gestor, cuenta.id))
    es_gestor = bool(perfiles.intersection(_PERFILES_GESTORES))
    return servicio.detalle(orden_id, cuenta.id, es_gestor)

@enrutador.get("/{orden_id}/historial", response_model=list[RespuestaBitacora])
def historial(
    orden_id: int,
    cuenta: Cuenta = Depends(obtener_cuenta_activa),
    gestor: GestorTransaccion = Depends(obtener_gestor),
    servicio: ServicioOrdenes = Depends(obtener_servicio),
) -> list[RespuestaBitacora]:
    perfiles = set(perfiles_de_cuenta(gestor, cuenta.id))
    es_gestor = bool(perfiles.intersection(_PERFILES_GESTORES))
    return servicio.historial(orden_id, cuenta.id, es_gestor)

@enrutador.patch("/{orden_id}/estado", response_model=RespuestaOrden)
async def cambiar_estado(
    orden_id: int,
    datos: CambioEstadoEntrada,
    cuenta: Cuenta = Depends(requerir_perfil("ADMINISTRADOR", "DESPACHO")),
    gestor: GestorTransaccion = Depends(obtener_gestor),
    servicio: ServicioOrdenes = Depends(obtener_servicio),
) -> RespuestaOrden:
    with gestor:
        orden = servicio.cambiar_estado(
            orden_id, datos.estado_nuevo, cuenta.id, datos.comentario
        )
    await _difundir_orden(orden, "orden_actualizada")
    return orden

@enrutador.post("/{orden_id}/cancelar", response_model=RespuestaOrden)
async def cancelar(
    orden_id: int,
    cuenta: Cuenta = Depends(requerir_perfil("COMPRADOR", "ADMINISTRADOR")),
    gestor: GestorTransaccion = Depends(obtener_gestor),
    servicio: ServicioOrdenes = Depends(obtener_servicio),
) -> RespuestaOrden:
    with gestor:
        orden = servicio.cancelar_por_comprador(orden_id, cuenta.id)
    await _difundir_orden(orden, "orden_cancelada")
    return orden
