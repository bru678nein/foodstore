"""Pruebas del modulo de sesion."""
from __future__ import annotations

from fastapi.testclient import TestClient

from pruebas.conftest import CLAVE_ADMIN, CORREO_ADMIN, PREFIJO


def _registrar(cliente: TestClient, correo: str, clave: str = "Secreto1234!"):
    return cliente.post(
        f"{PREFIJO}/sesion/registrar",
        json={"correo": correo, "clave": clave, "nombre_completo": "Usuario Test"},
    )


def test_registro_exitoso(cliente: TestClient):
    respuesta = _registrar(cliente, "nuevo@foodstore.com")
    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["cuenta"]["correo"] == "nuevo@foodstore.com"
    assert "COMPRADOR" in cuerpo["cuenta"]["perfiles"]
    assert "token_acceso" in cuerpo
    assert "token_renovacion" in cuerpo


def test_registro_correo_duplicado(cliente: TestClient):
    _registrar(cliente, "duplicado@foodstore.com")
    repetido = _registrar(cliente, "duplicado@foodstore.com")
    assert repetido.status_code == 409


def test_inicio_sesion_correcto(cliente: TestClient):
    respuesta = cliente.post(
        f"{PREFIJO}/sesion/iniciar",
        json={"correo": CORREO_ADMIN, "clave": CLAVE_ADMIN},
    )
    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert cuerpo["token_acceso"]
    assert cuerpo["token_renovacion"]
    assert "ADMINISTRADOR" in cuerpo["cuenta"]["perfiles"]


def test_inicio_sesion_credenciales_incorrectas(cliente: TestClient):
    respuesta = cliente.post(
        f"{PREFIJO}/sesion/iniciar",
        json={"correo": CORREO_ADMIN, "clave": "claveerronea"},
    )
    assert respuesta.status_code == 401


def test_inicio_sesion_cuenta_deshabilitada(cliente: TestClient, cabecera_admin):
    _registrar(cliente, "bloqueado@foodstore.com")
    # El admin localiza la cuenta y la deshabilita.
    listado = cliente.get(f"{PREFIJO}/cuentas", headers=cabecera_admin).json()
    objetivo = next(c for c in listado if c["correo"] == "bloqueado@foodstore.com")
    cliente.patch(
        f"{PREFIJO}/cuentas/{objetivo['id']}/estado",
        headers=cabecera_admin,
        json={"habilitado": False},
    )
    respuesta = cliente.post(
        f"{PREFIJO}/sesion/iniciar",
        json={"correo": "bloqueado@foodstore.com", "clave": "Secreto1234!"},
    )
    assert respuesta.status_code == 403


def test_renovar_token_valido(cliente: TestClient):
    inicio = cliente.post(
        f"{PREFIJO}/sesion/iniciar",
        json={"correo": CORREO_ADMIN, "clave": CLAVE_ADMIN},
    ).json()
    respuesta = cliente.post(
        f"{PREFIJO}/sesion/renovar",
        json={"token_renovacion": inicio["token_renovacion"]},
    )
    assert respuesta.status_code == 200
    assert respuesta.json()["token_acceso"]


def test_renovar_token_revocado(cliente: TestClient):
    inicio = cliente.post(
        f"{PREFIJO}/sesion/iniciar",
        json={"correo": CORREO_ADMIN, "clave": CLAVE_ADMIN},
    ).json()
    cliente.post(
        f"{PREFIJO}/sesion/cerrar",
        json={"token_renovacion": inicio["token_renovacion"]},
    )
    respuesta = cliente.post(
        f"{PREFIJO}/sesion/renovar",
        json={"token_renovacion": inicio["token_renovacion"]},
    )
    assert respuesta.status_code == 401


def test_cerrar_sesion(cliente: TestClient):
    inicio = cliente.post(
        f"{PREFIJO}/sesion/iniciar",
        json={"correo": CORREO_ADMIN, "clave": CLAVE_ADMIN},
    ).json()
    respuesta = cliente.post(
        f"{PREFIJO}/sesion/cerrar",
        json={"token_renovacion": inicio["token_renovacion"]},
    )
    assert respuesta.status_code == 204
