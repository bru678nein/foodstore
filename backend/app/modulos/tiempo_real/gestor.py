from __future__ import annotations

from typing import Any, Iterable

from fastapi import WebSocket

class GestorConexiones:

    def __init__(self) -> None:
        self.canales: dict[str, set[WebSocket]] = {}

    async def conectar(self, ws: WebSocket, canal: str) -> None:
        self.canales.setdefault(canal, set()).add(ws)

    def desconectar(self, ws: WebSocket, canal: str) -> None:
        suscriptores = self.canales.get(canal)
        if suscriptores is None:
            return
        suscriptores.discard(ws)
        if not suscriptores:
            self.canales.pop(canal, None)

    async def difundir(self, canal: str, mensaje: dict[str, Any]) -> None:
        muertos: list[WebSocket] = []
        for ws in list(self.canales.get(canal, set())):
            try:
                await ws.send_json(mensaje)
            except Exception:
                muertos.append(ws)
        for ws in muertos:
            self.desconectar(ws, canal)

    async def difundir_multiples(
        self, canales: Iterable[str], mensaje: dict[str, Any]
    ) -> None:
        for canal in canales:
            await self.difundir(canal, mensaje)

gestor_conexiones = GestorConexiones()
