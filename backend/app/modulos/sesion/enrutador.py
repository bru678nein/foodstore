from __future__ import annotations

from fastapi import APIRouter, Depends, Request, status

from app.nucleo.dependencias import obtener_cuenta_activa
from app.nucleo.limitador import limitador
from app.modulos.sesion.esquemas import (
    CerrarEntrada,
    CuentaBasica,
    InicioSesionEntrada,
    RegistroEntrada,
    RenovarEntrada,
    RespuestaAcceso,
    RespuestaToken,
)
from app.modulos.sesion.repositorio import RepositorioSesion
from app.modulos.sesion.servicio import ServicioSesion
from app.persistencia.entidades.cuenta import Cuenta
from app.persistencia.sesion_trabajo import GestorTransaccion, obtener_gestor

enrutador = APIRouter(prefix="/sesion", tags=["sesion"])

def obtener_servicio(
    gestor: GestorTransaccion = Depends(obtener_gestor),
) -> ServicioSesion:
    return ServicioSesion(RepositorioSesion(gestor.sesion), gestor)

@enrutador.post(
    "/registrar", response_model=RespuestaToken, status_code=status.HTTP_201_CREATED
)
@limitador.limit("5/15minutes")
def registrar(
    request: Request,
    datos: RegistroEntrada,
    servicio: ServicioSesion = Depends(obtener_servicio),
) -> RespuestaToken:
    cuenta = servicio.registrar_cuenta(datos)
    return servicio._emitir_tokens(cuenta)

@enrutador.post("/iniciar", response_model=RespuestaToken)
@limitador.limit("5/15minutes")
def iniciar(
    request: Request,
    datos: InicioSesionEntrada,
    servicio: ServicioSesion = Depends(obtener_servicio),
) -> RespuestaToken:
    return servicio.iniciar_sesion(datos)

@enrutador.post("/renovar", response_model=RespuestaAcceso)
def renovar(
    datos: RenovarEntrada,
    servicio: ServicioSesion = Depends(obtener_servicio),
) -> RespuestaAcceso:
    return servicio.renovar_token(datos.token_renovacion)

@enrutador.post("/cerrar", status_code=status.HTTP_204_NO_CONTENT)
def cerrar(
    datos: CerrarEntrada,
    servicio: ServicioSesion = Depends(obtener_servicio),
) -> None:
    servicio.cerrar_sesion(datos.token_renovacion)

@enrutador.get("/mi-cuenta", response_model=CuentaBasica)
def mi_cuenta(
    cuenta: Cuenta = Depends(obtener_cuenta_activa),
    servicio: ServicioSesion = Depends(obtener_servicio),
) -> CuentaBasica:
    return servicio.cuenta_a_respuesta(cuenta)
