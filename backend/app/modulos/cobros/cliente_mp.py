from __future__ import annotations

import uuid
from typing import Any

from app.nucleo.ajustes import ajustes

def _sdk_disponible() -> bool:
    if not ajustes.token_mp:
        return False
    try:
        import mercadopago  # noqa: F401
    except ImportError:
        return False
    return True

def crear_preferencia(items: list[dict[str, Any]], referencia: str) -> dict[str, Any]:
    if not _sdk_disponible():
        identificador = f"sim-pref-{uuid.uuid4().hex[:12]}"
        return {
            "id": identificador,
            "init_point": f"https://simulado.local/checkout/{identificador}",
            "simulado": True,
        }

    import mercadopago

    cliente = mercadopago.SDK(ajustes.token_mp)

    _es_local = any(h in ajustes.url_frontend for h in ("localhost", "127.0.0.1"))

    cuerpo: dict[str, Any] = {
        "items": items,
        "external_reference": referencia,
    }
    if not _es_local:
        cuerpo["back_urls"] = {
            "success": f"{ajustes.url_frontend}/pago/exito",
            "failure": f"{ajustes.url_frontend}/pago/error",
            "pending": f"{ajustes.url_frontend}/pago/pendiente",
        }
        cuerpo["auto_return"] = "approved"
    _es_api_local = any(h in ajustes.url_api for h in ("localhost", "127.0.0.1"))
    _api_url_valida = ajustes.url_api.startswith("http") and "." in ajustes.url_api
    if not _es_api_local and _api_url_valida:
        cuerpo["notification_url"] = f"{ajustes.url_api}/api/v1/cobros/webhook"
    respuesta = cliente.preference().create(cuerpo)
    codigo = respuesta.get("status")
    datos = respuesta.get("response", {})
    if codigo not in {200, 201} or not datos.get("id"):
        from fastapi import HTTPException, status as http_status
        detalle = datos.get("message") or datos.get("error") or "Error al crear preferencia en MercadoPago"
        raise HTTPException(status_code=http_status.HTTP_502_BAD_GATEWAY, detail=detalle)
    return {
        "id": datos.get("id"),
        "init_point": datos.get("init_point"),
        "simulado": False,
    }

def consultar_pago(id_pago: str) -> dict[str, Any]:
    if not _sdk_disponible():
        return {"id": id_pago, "status": "approved", "payment_method_id": "simulado"}

    import mercadopago

    cliente = mercadopago.SDK(ajustes.token_mp)
    respuesta = cliente.payment().get(id_pago)
    return respuesta.get("response", {})
