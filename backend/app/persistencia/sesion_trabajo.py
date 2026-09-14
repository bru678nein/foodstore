from __future__ import annotations

from types import TracebackType
from typing import Any, Generator

from sqlmodel import Session

from app.persistencia.motor import motor

class GestorTransaccion:

    def __init__(self, sesion: Session) -> None:
        self.sesion = sesion
        self._confirmado = False

    def __enter__(self) -> "GestorTransaccion":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type is None:
            self.confirmar()
        else:
            self.revertir()

    def confirmar(self) -> None:
        self.sesion.commit()
        self._confirmado = True

    def revertir(self) -> None:
        self.sesion.rollback()

    def sincronizar(self) -> None:
        self.sesion.flush()

    def actualizar(self, instancia: Any) -> None:
        self.sesion.refresh(instancia)

def obtener_gestor() -> Generator[GestorTransaccion, None, None]:
    with Session(motor) as sesion:
        gestor = GestorTransaccion(sesion)
        try:
            yield gestor
            gestor.confirmar()
        except Exception:
            gestor.revertir()
            raise
