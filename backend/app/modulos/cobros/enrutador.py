from __future__ import annotations

import hashlib
import hmac

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.nucleo.ajustes import ajustes
from app.nucleo.dependencias import obtener_cuenta_activa, requerir_perfil
from app.modulos.cobros.esquemas import (
    CobroSalida,
    PagoDirectoEntrada,
    PagoDirectoSalida,
    PreferenciaEntrada,
    PreferenciaSalida,
)
from app.modulos.cobros.servicio import ServicioCobros
from app.modulos.tiempo_real.gestor import gestor_conexiones
from app.persistencia.entidades.cuenta import Cuenta
from app.persistencia.sesion_trabajo import GestorTransaccion, obtener_gestor

enrutador = APIRouter(prefix="/cobros", tags=["cobros"])

def _verificar_firma_mp(request: Request) -> None:
    secreto = ajustes.secreto_webhook_mp
    if not secreto:
        return

    header = request.headers.get("x-signature", "")
    if not header:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Firma ausente")

    partes = dict(p.split("=", 1) for p in header.split(",") if "=" in p)
    ts = partes.get("ts", "")
    firma_recibida = partes.get("v1", "")

    data_id = request.query_params.get("data.id", "").lower()
    request_id = request.headers.get("x-request-id", "")

    partes_manifest: list[str] = []
    if data_id:
        partes_manifest.append(f"id:{data_id}")
    if request_id:
        partes_manifest.append(f"request-id:{request_id}")
    partes_manifest.append(f"ts:{ts}")
    mensaje = ";".join(partes_manifest) + ";"

    firma_esperada = hmac.new(secreto.encode(), mensaje.encode(), hashlib.sha256).hexdigest()

    if not hmac.compare_digest(firma_esperada, firma_recibida):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Firma invalida")

def obtener_servicio(
    gestor: GestorTransaccion = Depends(obtener_gestor),
) -> ServicioCobros:
    return ServicioCobros(gestor.sesion, gestor)

@enrutador.post(
    "/preferencia", response_model=PreferenciaSalida, status_code=status.HTTP_201_CREATED
)
def crear_preferencia(
    datos: PreferenciaEntrada,
    cuenta: Cuenta = Depends(requerir_perfil("COMPRADOR", "ADMINISTRADOR")),
    servicio: ServicioCobros = Depends(obtener_servicio),
) -> PreferenciaSalida:
    return servicio.crear_preferencia(datos.orden_id, cuenta.id)

@enrutador.post(
    "/pago-directo", response_model=PagoDirectoSalida, status_code=status.HTTP_201_CREATED
)
def pago_directo(
    datos: PagoDirectoEntrada,
    cuenta: Cuenta = Depends(requerir_perfil("COMPRADOR", "ADMINISTRADOR")),
    servicio: ServicioCobros = Depends(obtener_servicio),
) -> PagoDirectoSalida:
    return servicio.pago_directo(datos, cuenta.id)

@enrutador.post("/webhook", status_code=status.HTTP_200_OK)
async def webhook(
    request: Request,
    gestor: GestorTransaccion = Depends(obtener_gestor),
    servicio: ServicioCobros = Depends(obtener_servicio),
) -> dict[str, str]:
    cuerpo = {}
    try:
        cuerpo = await request.json()
    except Exception:
        cuerpo = {}
    parametros = dict(request.query_params)

    id_pago = None
    if isinstance(cuerpo, dict):
        datos = cuerpo.get("data") or {}
        id_pago = datos.get("id") if isinstance(datos, dict) else None
    id_pago = id_pago or parametros.get("data.id") or parametros.get("id")

    _verificar_firma_mp(request)

    with gestor:
        orden_id, nuevo_estado, cuenta_id = servicio.procesar_webhook(id_pago)

    if orden_id is not None and nuevo_estado == "approved":
        evento = {"evento": "pago_aprobado", "orden_id": orden_id, "estado": "CONFIRMADO"}
        canales: set[str] = {"ordenes", f"orden:{orden_id}"}
        if cuenta_id:
            canales.add(f"cuenta:{cuenta_id}")
        await gestor_conexiones.difundir_multiples(canales, evento)

    return {"estado": "recibido"}

@enrutador.get("/{orden_id}", response_model=CobroSalida)
def estado_cobro(
    orden_id: int,
    cuenta: Cuenta = Depends(obtener_cuenta_activa),
    servicio: ServicioCobros = Depends(obtener_servicio),
) -> CobroSalida:
    return servicio.estado_cobro(orden_id)
