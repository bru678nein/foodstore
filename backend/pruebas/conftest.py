"""Configuracion y fixtures compartidas para la bateria de pruebas.

Se fuerza una base SQLite aislada en archivo temporal antes de importar la
aplicacion, de modo que el motor real apunte a la base de pruebas y no a
PostgreSQL.
"""
from __future__ import annotations

import os
import tempfile

import pytest

_DESCRIPTOR, _RUTA_DB = tempfile.mkstemp(suffix=".db")
os.close(_DESCRIPTOR)
_RUTA_NORMALIZADA = _RUTA_DB.replace("\\", "/")

os.environ["DATABASE_URL"] = f"sqlite:///{_RUTA_NORMALIZADA}"
os.environ["CLAVE_SECRETA"] = "clave-de-pruebas-suuuper-secreta-0123456789"
os.environ["MINUTOS_ACCESO"] = "30"

from fastapi.testclient import TestClient  # noqa: E402
from sqlmodel import SQLModel  # noqa: E402

from app.nucleo.limitador import limitador  # noqa: E402
from app.persistencia.carga_inicial import (  # noqa: E402
    CLAVE_ADMIN,
    CORREO_ADMIN,
    ejecutar_carga_inicial,
)
from app.persistencia.motor import motor  # noqa: E402
from app.principal import aplicacion  # noqa: E402

PREFIJO = "/api/v1"

# El limitador se desactiva para no interferir con las pruebas.
limitador.enabled = False


@pytest.fixture()
def cliente():
    """Entrega un TestClient sobre una base recreada por cada prueba."""
    SQLModel.metadata.drop_all(motor)
    SQLModel.metadata.create_all(motor)
    ejecutar_carga_inicial()
    with TestClient(aplicacion) as instancia:
        yield instancia


def _token(cliente: TestClient, correo: str, clave: str) -> str:
    respuesta = cliente.post(
        f"{PREFIJO}/sesion/iniciar", json={"correo": correo, "clave": clave}
    )
    assert respuesta.status_code == 200, respuesta.text
    return respuesta.json()["token_acceso"]


@pytest.fixture()
def token_admin(cliente: TestClient) -> str:
    return _token(cliente, CORREO_ADMIN, CLAVE_ADMIN)


@pytest.fixture()
def cabecera_admin(token_admin: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token_admin}"}


@pytest.fixture()
def token_comprador(cliente: TestClient) -> str:
    cliente.post(
        f"{PREFIJO}/sesion/registrar",
        json={
            "correo": "comprador@foodstore.com",
            "clave": "Comprador1234!",
            "nombre_completo": "Comprador de Prueba",
        },
    )
    return _token(cliente, "comprador@foodstore.com", "Comprador1234!")


@pytest.fixture()
def cabecera_comprador(token_comprador: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token_comprador}"}
