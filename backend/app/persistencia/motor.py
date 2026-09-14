from __future__ import annotations

from sqlmodel import SQLModel, create_engine

from app.nucleo.ajustes import ajustes

from app.persistencia import entidades  # noqa: F401

_argumentos_conexion = {}
if ajustes.database_url.startswith("sqlite"):
    _argumentos_conexion = {"check_same_thread": False}

motor = create_engine(
    ajustes.database_url,
    echo=False,
    connect_args=_argumentos_conexion,
)

def crear_tablas() -> None:
    SQLModel.metadata.create_all(motor)
