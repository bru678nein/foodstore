"""Pruebas del modulo de ordenes y su maquina de estados."""
from __future__ import annotations

from fastapi.testclient import TestClient

from pruebas.conftest import PREFIJO


def _crear_articulo(cliente, cabecera_admin, existencias=50, disponible=True, precio="100.00"):
    respuesta = cliente.post(
        f"{PREFIJO}/articulos",
        headers=cabecera_admin,
        json={
            "titulo": "Hamburguesa Clasica",
            "descripcion": "Doble carne",
            "precio_unitario": precio,
            "existencias": existencias,
            "disponible": disponible,
            "categorias": [],
            "composicion": [],
        },
    )
    assert respuesta.status_code == 201, respuesta.text
    return respuesta.json()["id"]


def _crear_domicilio(cliente, cabecera_comprador):
    respuesta = cliente.post(
        f"{PREFIJO}/domicilios",
        headers=cabecera_comprador,
        json={
            "via": "Av. Siempre Viva",
            "altura": "742",
            "localidad": "Springfield",
            "provincia": "Buenos Aires",
            "codigo_postal": "1000",
            "es_predeterminado": True,
        },
    )
    assert respuesta.status_code == 201, respuesta.text
    return respuesta.json()["id"]


def _crear_orden(cliente, cabecera_comprador, articulo_id, domicilio_id, unidades=2):
    return cliente.post(
        f"{PREFIJO}/ordenes",
        headers=cabecera_comprador,
        json={
            "domicilio_id": domicilio_id,
            "partidas": [{"articulo_id": articulo_id, "unidades": unidades}],
            "observaciones": "Sin cebolla",
        },
    )


def test_crear_orden_exitosa(cliente: TestClient, cabecera_admin, cabecera_comprador):
    articulo_id = _crear_articulo(cliente, cabecera_admin)
    domicilio_id = _crear_domicilio(cliente, cabecera_comprador)
    respuesta = _crear_orden(cliente, cabecera_comprador, articulo_id, domicilio_id)
    assert respuesta.status_code == 201, respuesta.text
    cuerpo = respuesta.json()
    assert cuerpo["estado_actual"] == "PENDIENTE"
    assert cuerpo["subtotal"] == "200.00"
    assert cuerpo["costo_envio"] == "50.00"
    assert cuerpo["total"] == "250.00"
    assert len(cuerpo["partidas"]) == 1
    assert len(cuerpo["bitacora"]) == 1


def test_crear_orden_stock_insuficiente(cliente, cabecera_admin, cabecera_comprador):
    articulo_id = _crear_articulo(cliente, cabecera_admin, existencias=1)
    domicilio_id = _crear_domicilio(cliente, cabecera_comprador)
    respuesta = _crear_orden(cliente, cabecera_comprador, articulo_id, domicilio_id, unidades=5)
    assert respuesta.status_code == 409


def test_crear_orden_articulo_no_disponible(cliente, cabecera_admin, cabecera_comprador):
    articulo_id = _crear_articulo(cliente, cabecera_admin, disponible=False)
    domicilio_id = _crear_domicilio(cliente, cabecera_comprador)
    respuesta = _crear_orden(cliente, cabecera_comprador, articulo_id, domicilio_id)
    assert respuesta.status_code == 409


def test_transicion_pendiente_a_confirmado(cliente, cabecera_admin, cabecera_comprador):
    articulo_id = _crear_articulo(cliente, cabecera_admin)
    domicilio_id = _crear_domicilio(cliente, cabecera_comprador)
    orden = _crear_orden(cliente, cabecera_comprador, articulo_id, domicilio_id).json()
    respuesta = cliente.patch(
        f"{PREFIJO}/ordenes/{orden['id']}/estado",
        headers=cabecera_admin,
        json={"estado_nuevo": "CONFIRMADO"},
    )
    assert respuesta.status_code == 200
    assert respuesta.json()["estado_actual"] == "CONFIRMADO"


def test_transicion_pendiente_a_cancelado(cliente, cabecera_admin, cabecera_comprador):
    articulo_id = _crear_articulo(cliente, cabecera_admin)
    domicilio_id = _crear_domicilio(cliente, cabecera_comprador)
    orden = _crear_orden(cliente, cabecera_comprador, articulo_id, domicilio_id).json()
    respuesta = cliente.patch(
        f"{PREFIJO}/ordenes/{orden['id']}/estado",
        headers=cabecera_admin,
        json={"estado_nuevo": "CANCELADO"},
    )
    assert respuesta.status_code == 200
    assert respuesta.json()["estado_actual"] == "CANCELADO"


def test_transicion_invalida_entregado_a_pendiente(cliente, cabecera_admin, cabecera_comprador):
    articulo_id = _crear_articulo(cliente, cabecera_admin)
    domicilio_id = _crear_domicilio(cliente, cabecera_comprador)
    orden = _crear_orden(cliente, cabecera_comprador, articulo_id, domicilio_id).json()
    oid = orden["id"]
    for estado in ["CONFIRMADO", "EN_PREPARACION", "ENTREGADO"]:
        cliente.patch(
            f"{PREFIJO}/ordenes/{oid}/estado",
            headers=cabecera_admin,
            json={"estado_nuevo": estado},
        )
    respuesta = cliente.patch(
        f"{PREFIJO}/ordenes/{oid}/estado",
        headers=cabecera_admin,
        json={"estado_nuevo": "PENDIENTE"},
    )
    assert respuesta.status_code == 409


def test_cancelar_orden_comprador_solo_pendiente(cliente, cabecera_admin, cabecera_comprador):
    articulo_id = _crear_articulo(cliente, cabecera_admin)
    domicilio_id = _crear_domicilio(cliente, cabecera_comprador)
    orden = _crear_orden(cliente, cabecera_comprador, articulo_id, domicilio_id).json()
    respuesta = cliente.post(
        f"{PREFIJO}/ordenes/{orden['id']}/cancelar", headers=cabecera_comprador
    )
    assert respuesta.status_code == 200
    assert respuesta.json()["estado_actual"] == "CANCELADO"


def test_historial_orden(cliente, cabecera_admin, cabecera_comprador):
    articulo_id = _crear_articulo(cliente, cabecera_admin)
    domicilio_id = _crear_domicilio(cliente, cabecera_comprador)
    orden = _crear_orden(cliente, cabecera_comprador, articulo_id, domicilio_id).json()
    cliente.patch(
        f"{PREFIJO}/ordenes/{orden['id']}/estado",
        headers=cabecera_admin,
        json={"estado_nuevo": "CONFIRMADO"},
    )
    respuesta = cliente.get(
        f"{PREFIJO}/ordenes/{orden['id']}/historial", headers=cabecera_admin
    )
    assert respuesta.status_code == 200
    historial = respuesta.json()
    assert len(historial) == 2
    assert historial[0]["estado_siguiente"] == "PENDIENTE"
    assert historial[1]["estado_siguiente"] == "CONFIRMADO"


def test_transicion_en_preparacion_a_cancelado(cliente, cabecera_admin, cabecera_comprador):
    articulo_id = _crear_articulo(cliente, cabecera_admin)
    domicilio_id = _crear_domicilio(cliente, cabecera_comprador)
    orden = _crear_orden(cliente, cabecera_comprador, articulo_id, domicilio_id).json()
    oid = orden["id"]
    for estado in ["CONFIRMADO", "EN_PREPARACION"]:
        cliente.patch(
            f"{PREFIJO}/ordenes/{oid}/estado",
            headers=cabecera_admin,
            json={"estado_nuevo": estado},
        )
    respuesta = cliente.patch(
        f"{PREFIJO}/ordenes/{oid}/estado",
        headers=cabecera_admin,
        json={"estado_nuevo": "CANCELADO"},
    )
    assert respuesta.status_code == 200
    assert respuesta.json()["estado_actual"] == "CANCELADO"


def test_cancelar_orden_ya_confirmada_falla(cliente, cabecera_admin, cabecera_comprador):
    articulo_id = _crear_articulo(cliente, cabecera_admin)
    domicilio_id = _crear_domicilio(cliente, cabecera_comprador)
    orden = _crear_orden(cliente, cabecera_comprador, articulo_id, domicilio_id).json()
    cliente.patch(
        f"{PREFIJO}/ordenes/{orden['id']}/estado",
        headers=cabecera_admin,
        json={"estado_nuevo": "CONFIRMADO"},
    )
    respuesta = cliente.post(
        f"{PREFIJO}/ordenes/{orden['id']}/cancelar", headers=cabecera_comprador
    )
    assert respuesta.status_code == 409
