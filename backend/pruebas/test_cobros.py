"""Pruebas del modulo de cobros: preferencias MP, webhook y estado."""
from __future__ import annotations

from unittest.mock import patch

from fastapi.testclient import TestClient

from pruebas.conftest import PREFIJO


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _crear_articulo(cliente: TestClient, cabecera_admin: dict) -> int:
    resp = cliente.post(
        f"{PREFIJO}/articulos",
        headers=cabecera_admin,
        json={
            "titulo": "Milanesa Napolitana",
            "descripcion": "Clásica.",
            "precio_unitario": "1500.00",
            "existencias": 50,
            "disponible": True,
            "categorias": [],
            "composicion": [],
        },
    )
    assert resp.status_code == 201, resp.text
    return resp.json()["id"]


def _crear_domicilio(cliente: TestClient, cabecera_comprador: dict) -> int:
    resp = cliente.post(
        f"{PREFIJO}/domicilios",
        headers=cabecera_comprador,
        json={
            "via": "Calle Test",
            "altura": "100",
            "localidad": "Ciudad",
            "provincia": "Buenos Aires",
            "codigo_postal": "1000",
            "es_predeterminado": True,
        },
    )
    assert resp.status_code == 201, resp.text
    return resp.json()["id"]


def _crear_orden(
    cliente: TestClient, cabecera_comprador: dict, articulo_id: int, domicilio_id: int
) -> dict:
    resp = cliente.post(
        f"{PREFIJO}/ordenes",
        headers=cabecera_comprador,
        json={
            "domicilio_id": domicilio_id,
            "partidas": [{"articulo_id": articulo_id, "unidades": 1}],
        },
    )
    assert resp.status_code == 201, resp.text
    return resp.json()


def _crear_preferencia(
    cliente: TestClient, cabecera_comprador: dict, orden_id: int
) -> dict:
    resp = cliente.post(
        f"{PREFIJO}/cobros/preferencia",
        headers=cabecera_comprador,
        json={"orden_id": orden_id},
    )
    return resp


# ---------------------------------------------------------------------------
# Tests: POST /cobros/preferencia
# ---------------------------------------------------------------------------

def test_crear_preferencia_exitosa(cliente, cabecera_admin, cabecera_comprador):
    articulo_id = _crear_articulo(cliente, cabecera_admin)
    domicilio_id = _crear_domicilio(cliente, cabecera_comprador)
    orden = _crear_orden(cliente, cabecera_comprador, articulo_id, domicilio_id)

    resp = _crear_preferencia(cliente, cabecera_comprador, orden["id"])
    assert resp.status_code == 201, resp.text
    cuerpo = resp.json()
    assert "id_preferencia" in cuerpo
    assert "init_point" in cuerpo
    assert "cobro_id" in cuerpo
    assert cuerpo["id_preferencia"].startswith("sim-pref-")


def test_crear_preferencia_orden_inexistente(cliente, cabecera_comprador):
    resp = _crear_preferencia(cliente, cabecera_comprador, 99999)
    assert resp.status_code == 404


def test_crear_preferencia_orden_ajena(cliente, cabecera_admin, cabecera_comprador):
    # Crear segundo comprador
    cliente.post(
        f"{PREFIJO}/sesion/registrar",
        json={
            "correo": "otro@foodstore.com",
            "clave": "Otro1234567!",
            "nombre_completo": "Otro Comprador",
        },
    )
    resp_login = cliente.post(
        f"{PREFIJO}/sesion/iniciar",
        json={"correo": "otro@foodstore.com", "clave": "Otro1234567!"},
    )
    cabecera_otro = {"Authorization": f"Bearer {resp_login.json()['token_acceso']}"}

    articulo_id = _crear_articulo(cliente, cabecera_admin)
    domicilio_id = _crear_domicilio(cliente, cabecera_comprador)
    orden = _crear_orden(cliente, cabecera_comprador, articulo_id, domicilio_id)

    # El "otro" intenta pagar una orden que no es suya
    resp = _crear_preferencia(cliente, cabecera_otro, orden["id"])
    assert resp.status_code == 403


def test_crear_preferencia_idempotente(cliente, cabecera_admin, cabecera_comprador):
    """Segunda llamada actualiza el cobro existente en vez de crear uno nuevo."""
    articulo_id = _crear_articulo(cliente, cabecera_admin)
    domicilio_id = _crear_domicilio(cliente, cabecera_comprador)
    orden = _crear_orden(cliente, cabecera_comprador, articulo_id, domicilio_id)

    resp1 = _crear_preferencia(cliente, cabecera_comprador, orden["id"])
    resp2 = _crear_preferencia(cliente, cabecera_comprador, orden["id"])

    assert resp1.status_code == 201
    assert resp2.status_code == 201
    # El cobro_id debe ser el mismo (mismo registro, no duplicado)
    assert resp1.json()["cobro_id"] == resp2.json()["cobro_id"]


def test_crear_preferencia_requiere_perfil_comprador(cliente, cabecera_admin):
    resp = cliente.post(
        f"{PREFIJO}/cobros/preferencia",
        headers=cabecera_admin,
        json={"orden_id": 1},
    )
    assert resp.status_code == 403


# ---------------------------------------------------------------------------
# Tests: POST /cobros/webhook
# ---------------------------------------------------------------------------

def test_webhook_acepta_body_json(cliente, cabecera_admin, cabecera_comprador):
    articulo_id = _crear_articulo(cliente, cabecera_admin)
    domicilio_id = _crear_domicilio(cliente, cabecera_comprador)
    orden = _crear_orden(cliente, cabecera_comprador, articulo_id, domicilio_id)
    _crear_preferencia(cliente, cabecera_comprador, orden["id"])

    resp = cliente.post(
        f"{PREFIJO}/cobros/webhook",
        json={"data": {"id": "pago-simulado-001"}},
    )
    assert resp.status_code == 200
    assert resp.json()["estado"] == "recibido"


def test_webhook_acepta_query_param(cliente, cabecera_admin, cabecera_comprador):
    articulo_id = _crear_articulo(cliente, cabecera_admin)
    domicilio_id = _crear_domicilio(cliente, cabecera_comprador)
    orden = _crear_orden(cliente, cabecera_comprador, articulo_id, domicilio_id)
    _crear_preferencia(cliente, cabecera_comprador, orden["id"])

    resp = cliente.post(
        f"{PREFIJO}/cobros/webhook?data.id=pago-simulado-002",
    )
    assert resp.status_code == 200


def test_webhook_sin_id_no_falla(cliente):
    """Webhook sin payload no debe lanzar excepcion."""
    resp = cliente.post(f"{PREFIJO}/cobros/webhook", json={})
    assert resp.status_code == 200


def test_webhook_actualiza_estado_cobro(cliente, cabecera_admin, cabecera_comprador):
    """El webhook actualiza el estado del cobro cuando recibe un pago aprobado."""
    articulo_id = _crear_articulo(cliente, cabecera_admin)
    domicilio_id = _crear_domicilio(cliente, cabecera_comprador)
    orden = _crear_orden(cliente, cabecera_comprador, articulo_id, domicilio_id)
    _crear_preferencia(cliente, cabecera_comprador, orden["id"])

    # Mockear consultar_pago para que devuelva un pago aprobado con referencia a la orden
    datos_pago_mock = {
        "id": "pago-approved-001",
        "status": "approved",
        "payment_method_id": "visa",
        "external_reference": str(orden["id"]),
    }
    with patch(
        "app.modulos.cobros.servicio.consultar_pago", return_value=datos_pago_mock
    ):
        cliente.post(
            f"{PREFIJO}/cobros/webhook",
            json={"data": {"id": "pago-approved-001"}},
        )

    resp_estado = cliente.get(
        f"{PREFIJO}/cobros/{orden['id']}",
        headers=cabecera_comprador,
    )
    assert resp_estado.status_code == 200
    cuerpo = resp_estado.json()
    assert cuerpo["estado_cobro"] == "approved"
    assert cuerpo["medio"] == "visa"


# ---------------------------------------------------------------------------
# Tests: GET /cobros/{orden_id}
# ---------------------------------------------------------------------------

def test_estado_cobro_sin_cobro_devuelve_404(cliente, cabecera_comprador):
    resp = cliente.get(f"{PREFIJO}/cobros/99999", headers=cabecera_comprador)
    assert resp.status_code == 404


def test_estado_cobro_despues_de_preferencia(cliente, cabecera_admin, cabecera_comprador):
    articulo_id = _crear_articulo(cliente, cabecera_admin)
    domicilio_id = _crear_domicilio(cliente, cabecera_comprador)
    orden = _crear_orden(cliente, cabecera_comprador, articulo_id, domicilio_id)
    pref = _crear_preferencia(cliente, cabecera_comprador, orden["id"])

    resp = cliente.get(
        f"{PREFIJO}/cobros/{orden['id']}",
        headers=cabecera_comprador,
    )
    assert resp.status_code == 200
    cuerpo = resp.json()
    assert cuerpo["orden_id"] == orden["id"]
    assert cuerpo["estado_cobro"] == "pendiente"
    assert cuerpo["id_preferencia_mp"] is not None
    assert cuerpo["id"] == pref.json()["cobro_id"]


def test_estado_cobro_requiere_autenticacion(cliente):
    resp = cliente.get(f"{PREFIJO}/cobros/1")
    assert resp.status_code == 401
