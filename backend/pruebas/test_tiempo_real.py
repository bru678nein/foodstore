"""Pruebas del modulo de tiempo real (WebSockets)."""
from __future__ import annotations

import pytest

from app.modulos.tiempo_real.gestor import GestorConexiones
from pruebas.conftest import CLAVE_ADMIN, CORREO_ADMIN, PREFIJO


class _SocketFalso:
    """Doble de prueba que registra los mensajes difundidos."""

    def __init__(self) -> None:
        self.recibidos: list[dict] = []
        self.cerrado = False

    async def send_json(self, mensaje: dict) -> None:
        self.recibidos.append(mensaje)


def test_conexion_websocket(cliente):
    inicio = cliente.post(
        f"{PREFIJO}/sesion/iniciar",
        json={"correo": CORREO_ADMIN, "clave": CLAVE_ADMIN},
    ).json()
    token = inicio["token_acceso"]
    with cliente.websocket_connect(f"/ws/ordenes?token={token}") as ws:
        bienvenida = ws.receive_json()
        assert bienvenida["evento"] == "conectado"
        assert bienvenida["canal"] == "ordenes"


def test_conexion_websocket_sin_token_se_rechaza(cliente):
    from starlette.websockets import WebSocketDisconnect

    with pytest.raises(WebSocketDisconnect):
        with cliente.websocket_connect("/ws/ordenes?token=invalido") as ws:
            ws.receive_json()


@pytest.mark.asyncio
async def test_desconexion_limpia():
    gestor = GestorConexiones()
    socket = _SocketFalso()
    await gestor.conectar(socket, "ordenes")
    assert "ordenes" in gestor.canales
    gestor.desconectar(socket, "ordenes")
    assert "ordenes" not in gestor.canales


@pytest.mark.asyncio
async def test_broadcast_cambio_estado_orden():
    gestor = GestorConexiones()
    socket_a = _SocketFalso()
    socket_b = _SocketFalso()
    await gestor.conectar(socket_a, "ordenes")
    await gestor.conectar(socket_b, "ordenes")

    mensaje = {"evento": "orden_actualizada", "orden_id": 1, "estado": "CONFIRMADO"}
    await gestor.difundir("ordenes", mensaje)

    assert socket_a.recibidos == [mensaje]
    assert socket_b.recibidos == [mensaje]


@pytest.mark.asyncio
async def test_difundir_multiples_canales():
    gestor = GestorConexiones()
    socket_ordenes = _SocketFalso()
    socket_cuenta = _SocketFalso()
    await gestor.conectar(socket_ordenes, "ordenes")
    await gestor.conectar(socket_cuenta, "cuenta:7")

    mensaje = {"evento": "orden_creada", "orden_id": 9}
    await gestor.difundir_multiples(["ordenes", "cuenta:7"], mensaje)

    assert socket_ordenes.recibidos == [mensaje]
    assert socket_cuenta.recibidos == [mensaje]


@pytest.mark.asyncio
async def test_reconexion_automatica():
    """Un socket que se desconecta puede reconectarse y recibir mensajes nuevos."""
    gestor = GestorConexiones()
    socket = _SocketFalso()

    await gestor.conectar(socket, "ordenes")
    await gestor.difundir("ordenes", {"evento": "ping"})
    assert len(socket.recibidos) == 1

    # simula desconexión
    gestor.desconectar(socket, "ordenes")
    assert "ordenes" not in gestor.canales

    # reconexión
    await gestor.conectar(socket, "ordenes")
    assert "ordenes" in gestor.canales
    await gestor.difundir("ordenes", {"evento": "pago_aprobado", "orden_id": 1})
    assert len(socket.recibidos) == 2
    assert socket.recibidos[-1]["evento"] == "pago_aprobado"
