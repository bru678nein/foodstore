"""Pruebas del modulo de metricas."""
from __future__ import annotations

from decimal import Decimal

from pruebas.conftest import PREFIJO


def _preparar(cliente, cabecera_admin, cabecera_comprador, precio="100.00", existencias=100):
    articulo = cliente.post(
        f"{PREFIJO}/articulos",
        headers=cabecera_admin,
        json={
            "titulo": "Pizza Napolitana",
            "precio_unitario": precio,
            "existencias": existencias,
            "disponible": True,
            "categorias": [],
            "composicion": [],
        },
    ).json()["id"]
    domicilio = cliente.post(
        f"{PREFIJO}/domicilios",
        headers=cabecera_comprador,
        json={
            "via": "Calle Falsa",
            "altura": "123",
            "localidad": "Capital",
            "provincia": "Cordoba",
        },
    ).json()["id"]
    return articulo, domicilio


def _crear_orden(cliente, cabecera_comprador, articulo, domicilio, unidades):
    return cliente.post(
        f"{PREFIJO}/ordenes",
        headers=cabecera_comprador,
        json={
            "domicilio_id": domicilio,
            "partidas": [{"articulo_id": articulo, "unidades": unidades}],
        },
    ).json()


def test_kpis_ventas_hoy(cliente, cabecera_admin, cabecera_comprador):
    articulo, domicilio = _preparar(cliente, cabecera_admin, cabecera_comprador)
    _crear_orden(cliente, cabecera_comprador, articulo, domicilio, 2)
    # total = subtotal(200) + costo_envio(50) = 250
    resumen = cliente.get(f"{PREFIJO}/metricas/resumen", headers=cabecera_admin).json()
    assert Decimal(resumen["ventas_hoy"]) == Decimal("250.00")


def test_kpis_ventas_mes(cliente, cabecera_admin, cabecera_comprador):
    articulo, domicilio = _preparar(cliente, cabecera_admin, cabecera_comprador)
    _crear_orden(cliente, cabecera_comprador, articulo, domicilio, 3)
    # total = subtotal(300) + costo_envio(50) = 350
    resumen = cliente.get(f"{PREFIJO}/metricas/resumen", headers=cabecera_admin).json()
    assert Decimal(resumen["ventas_mes"]) == Decimal("350.00")


def test_kpis_ticket_promedio(cliente, cabecera_admin, cabecera_comprador):
    articulo, domicilio = _preparar(cliente, cabecera_admin, cabecera_comprador)
    _crear_orden(cliente, cabecera_comprador, articulo, domicilio, 2)  # total 250
    _crear_orden(cliente, cabecera_comprador, articulo, domicilio, 1)  # total 150
    # promedio = (250 + 150) / 2 = 200
    resumen = cliente.get(f"{PREFIJO}/metricas/resumen", headers=cabecera_admin).json()
    assert Decimal(resumen["ticket_promedio"]) == Decimal("200.00")


def test_excluir_ordenes_canceladas_de_ingresos(cliente, cabecera_admin, cabecera_comprador):
    articulo, domicilio = _preparar(cliente, cabecera_admin, cabecera_comprador)
    _crear_orden(cliente, cabecera_comprador, articulo, domicilio, 2)  # 250 vigente
    cancelada = _crear_orden(cliente, cabecera_comprador, articulo, domicilio, 5)  # 550
    cliente.post(
        f"{PREFIJO}/ordenes/{cancelada['id']}/cancelar", headers=cabecera_comprador
    )
    resumen = cliente.get(f"{PREFIJO}/metricas/resumen", headers=cabecera_admin).json()
    assert Decimal(resumen["ventas_hoy"]) == Decimal("250.00")


def test_articulos_destacados(cliente, cabecera_admin, cabecera_comprador):
    articulo, domicilio = _preparar(cliente, cabecera_admin, cabecera_comprador)
    _crear_orden(cliente, cabecera_comprador, articulo, domicilio, 4)
    destacados = cliente.get(
        f"{PREFIJO}/metricas/articulos-destacados", headers=cabecera_admin
    ).json()
    assert destacados
    assert destacados[0]["articulo_id"] == articulo
    assert destacados[0]["unidades_vendidas"] == 4
