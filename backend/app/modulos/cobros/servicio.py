from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.modulos.cobros.cliente_mp import consultar_pago, crear_preferencia
from app.modulos.cobros.esquemas import CobroSalida, PagoDirectoEntrada, PagoDirectoSalida, PreferenciaSalida
from app.nucleo.ajustes import ajustes
from app.persistencia.entidades.orden import BitacoraOrden, Cobro, Orden, PartidaOrden
from app.persistencia.sesion_trabajo import GestorTransaccion

_MAPA_ESTADOS = {
    "approved": "approved",
    "pending": "pending",
    "in_process": "pending",
    "rejected": "rejected",
    "cancelled": "cancelled",
}

class ServicioCobros:
    def __init__(self, sesion: Session, gestor: GestorTransaccion) -> None:
        self.sesion = sesion
        self.gestor = gestor

    @staticmethod
    def _a_salida(cobro: Cobro) -> CobroSalida:
        return CobroSalida(
            id=cobro.id,
            orden_id=cobro.orden_id,
            estado_cobro=cobro.estado_cobro,
            monto=cobro.monto,
            medio=cobro.medio,
            id_pago_mp=cobro.id_pago_mp,
            id_preferencia_mp=cobro.id_preferencia_mp,
        )

    def crear_preferencia(self, orden_id: int, cuenta_id: int) -> PreferenciaSalida:
        orden = self.sesion.get(Orden, orden_id)
        if orden is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada"
            )
        if orden.cuenta_id != cuenta_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puede pagar una orden ajena",
            )

        existente = self.sesion.exec(
            select(Cobro).where(Cobro.orden_id == orden_id)
        ).first()

        partidas = self.sesion.exec(
            select(PartidaOrden).where(PartidaOrden.orden_id == orden_id)
        ).all()
        items = [
            {
                "title": p.titulo_capturado,
                "quantity": p.unidades,
                "unit_price": float(p.precio_capturado),
                "currency_id": "ARS",
            }
            for p in partidas
        ]

        preferencia = crear_preferencia(items, referencia=str(orden_id))

        if existente is None:
            existente = Cobro(
                orden_id=orden_id,
                clave_idempotencia=uuid.uuid4().hex,
                monto=orden.total,
                estado_cobro="pendiente",
            )
        existente.id_preferencia_mp = preferencia["id"]
        existente.actualizado_en = datetime.now(timezone.utc)
        self.sesion.add(existente)
        self.sesion.flush()

        return PreferenciaSalida(
            id_preferencia=preferencia["id"],
            init_point=preferencia["init_point"],
            cobro_id=existente.id,
        )

    def procesar_webhook(self, id_pago: str | None) -> tuple[int | None, str | None, int | None]:
        if not id_pago:
            return None, None, None
        datos = consultar_pago(id_pago)
        referencia = datos.get("external_reference")
        estado_externo = datos.get("status", "pending")
        medio = datos.get("payment_method_id")

        cobro = None
        if referencia:
            try:
                cobro = self.sesion.exec(
                    select(Cobro).where(Cobro.orden_id == int(referencia))
                ).first()
            except (TypeError, ValueError):
                cobro = None
        if cobro is None:
            return None, None, None

        nuevo_estado = _MAPA_ESTADOS.get(estado_externo, "pending")
        cobro.id_pago_mp = str(id_pago)
        cobro.estado_cobro = nuevo_estado
        cobro.medio = medio
        cobro.actualizado_en = datetime.now(timezone.utc)
        self.sesion.add(cobro)
        self.sesion.flush()

        cuenta_id: int | None = None
        if nuevo_estado == "approved":
            orden = self.sesion.get(Orden, cobro.orden_id)
            if orden is not None and orden.estado_actual == "PENDIENTE":
                cuenta_id = orden.cuenta_id
                orden.estado_actual = "CONFIRMADO"
                orden.actualizada_en = datetime.now(timezone.utc)
                self.sesion.add(orden)
                self.sesion.add(
                    BitacoraOrden(
                        orden_id=orden.id,
                        estado_previo="PENDIENTE",
                        estado_siguiente="CONFIRMADO",
                        ejecutado_por=orden.cuenta_id,
                        comentario="Confirmado automáticamente por pago aprobado en MercadoPago",
                    )
                )
                self.sesion.flush()

        return cobro.orden_id, nuevo_estado, cuenta_id

    def pago_directo(self, datos: PagoDirectoEntrada, cuenta_id: int) -> PagoDirectoSalida:
        try:
            import mercadopago
        except ImportError as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="SDK de MercadoPago no instalado",
            ) from exc

        if not ajustes.token_mp:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="MercadoPago no configurado",
            )

        orden = self.sesion.get(Orden, datos.orden_id)
        if orden is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
        if orden.cuenta_id != cuenta_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puede pagar una orden ajena")
        if orden.estado_actual != "PENDIENTE":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La orden no está en estado PENDIENTE")

        cobro = self.sesion.exec(select(Cobro).where(Cobro.orden_id == datos.orden_id)).first()
        if cobro and cobro.estado_cobro == "approved":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La orden ya fue pagada")

        sdk = mercadopago.SDK(ajustes.token_mp)
        cuerpo_pago: dict = {
            "transaction_amount": float(orden.total),
            "token": datos.token,
            "description": f"Orden #{orden.id}",
            "installments": int(datos.cuotas),
            "payment_method_id": datos.payment_method_id,
            "payer": {"email": datos.email_pagador or ""},
            "external_reference": str(orden.id),
        }
        if datos.issuer_id:
            try:
                cuerpo_pago["issuer_id"] = int(datos.issuer_id)
            except (ValueError, TypeError):
                cuerpo_pago["issuer_id"] = datos.issuer_id
        _es_api_local = any(h in ajustes.url_api for h in ("localhost", "127.0.0.1"))
        _api_url_valida = ajustes.url_api.startswith("http") and "." in ajustes.url_api
        if not _es_api_local and _api_url_valida:
            cuerpo_pago["notification_url"] = f"{ajustes.url_api}/api/v1/cobros/webhook"

        respuesta = sdk.payment().create(cuerpo_pago)
        datos_resp = respuesta.get("response", {})
        codigo = respuesta.get("status")

        if codigo not in {200, 201}:
            causa = datos_resp.get("cause", [])
            causa_str = ", ".join(str(c) for c in causa) if causa else ""
            detalle = (
                datos_resp.get("message")
                or datos_resp.get("error")
                or "No se pudo procesar el pago"
            )
            if causa_str:
                detalle = f"{detalle} — {causa_str}"
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=detalle)

        estado_mp = datos_resp.get("status", "pending")
        id_pago = str(datos_resp.get("id", ""))

        if cobro is None:
            cobro = Cobro(
                orden_id=orden.id,
                clave_idempotencia=uuid.uuid4().hex,
                monto=orden.total,
                estado_cobro=estado_mp,
            )
        cobro.id_pago_mp = id_pago
        cobro.estado_cobro = estado_mp
        cobro.medio = datos_resp.get("payment_method_id")
        cobro.actualizado_en = datetime.now(timezone.utc)
        self.sesion.add(cobro)

        if estado_mp == "approved":
            orden.estado_actual = "CONFIRMADO"
            orden.actualizada_en = datetime.now(timezone.utc)
            self.sesion.add(orden)
            self.sesion.add(
                BitacoraOrden(
                    orden_id=orden.id,
                    estado_previo="PENDIENTE",
                    estado_siguiente="CONFIRMADO",
                    ejecutado_por=cuenta_id,
                    comentario="Confirmado automáticamente por pago aprobado con tarjeta",
                )
            )
        self.sesion.flush()

        return PagoDirectoSalida(
            id_pago_mp=id_pago,
            estado=estado_mp,
            detalle=datos_resp.get("status_detail"),
        )

    def estado_cobro(self, orden_id: int) -> CobroSalida:
        cobro = self.sesion.exec(
            select(Cobro).where(Cobro.orden_id == orden_id)
        ).first()
        if cobro is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No existe cobro para esta orden",
            )
        return self._a_salida(cobro)
