from __future__ import annotations

from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect, status

from app.nucleo.proteccion import JWTError, decodificar_token
from app.modulos.tiempo_real.gestor import gestor_conexiones

enrutador = APIRouter()

@enrutador.websocket("/ws/{canal}")
async def canal_tiempo_real(
    websocket: WebSocket,
    canal: str,
    token: str = Query(default=""),
) -> None:
    try:
        decodificar_token(token)
    except JWTError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    await gestor_conexiones.conectar(websocket, canal)
    await websocket.send_json({"evento": "conectado", "canal": canal})
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        gestor_conexiones.desconectar(websocket, canal)
