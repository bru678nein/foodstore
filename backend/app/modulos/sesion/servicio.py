from __future__ import annotations

from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status

from app.nucleo.ajustes import ajustes
from app.nucleo.proteccion import (
    cifrar_clave,
    generar_token_acceso,
    generar_token_renovacion,
    verificar_clave,
)
from app.modulos.sesion.esquemas import (
    CuentaBasica,
    InicioSesionEntrada,
    RegistroEntrada,
    RespuestaAcceso,
    RespuestaToken,
)
from app.modulos.sesion.repositorio import RepositorioSesion
from app.persistencia.entidades.cuenta import Cuenta, TokenRenovacion
from app.persistencia.sesion_trabajo import GestorTransaccion

PERFIL_POR_DEFECTO = "COMPRADOR"

class ServicioSesion:

    def __init__(self, repositorio: RepositorioSesion, gestor: GestorTransaccion) -> None:
        self.repositorio = repositorio
        self.gestor = gestor

    def cuenta_a_respuesta(self, cuenta: Cuenta) -> CuentaBasica:
        return CuentaBasica(
            id=cuenta.id,
            correo=cuenta.correo,
            nombre_completo=cuenta.nombre_completo,
            perfiles=self.repositorio.consultar_perfiles(cuenta.id),
        )

    def consultar_perfiles_cuenta(self, cuenta_id: int) -> list[str]:
        return self.repositorio.consultar_perfiles(cuenta_id)

    def _emitir_tokens(self, cuenta: Cuenta) -> RespuestaToken:
        perfiles = self.repositorio.consultar_perfiles(cuenta.id)
        token_acceso = generar_token_acceso(
            {"sub": str(cuenta.id), "correo": cuenta.correo, "perfiles": perfiles}
        )
        valor_renovacion = generar_token_renovacion()
        vence = datetime.now(timezone.utc) + timedelta(days=ajustes.dias_renovacion)
        self.repositorio.guardar_token(
            TokenRenovacion(
                valor=valor_renovacion, cuenta_id=cuenta.id, vence_en=vence
            )
        )
        return RespuestaToken(
            token_acceso=token_acceso,
            token_renovacion=valor_renovacion,
            cuenta=CuentaBasica(
                id=cuenta.id,
                correo=cuenta.correo,
                nombre_completo=cuenta.nombre_completo,
                perfiles=perfiles,
            ),
        )

    def registrar_cuenta(self, datos: RegistroEntrada) -> Cuenta:
        if self.repositorio.buscar_cuenta_por_correo(datos.correo) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El correo ya se encuentra registrado",
            )
        cuenta = Cuenta(
            correo=datos.correo,
            clave_hash=cifrar_clave(datos.contrasena),
            nombre_completo=datos.nombre_completo,
        )
        self.repositorio.crear_cuenta(cuenta)

        perfil = self.repositorio.buscar_perfil_por_nombre(PERFIL_POR_DEFECTO)
        if perfil is not None:
            self.repositorio.asignar_perfil(cuenta.id, perfil)
        return cuenta

    def validar_credenciales(self, datos: InicioSesionEntrada) -> Cuenta:
        cuenta = self.repositorio.buscar_cuenta_por_correo(datos.correo)
        if cuenta is None or not verificar_clave(datos.contrasena, cuenta.clave_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Correo o clave incorrectos",
            )
        if not cuenta.habilitado:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="La cuenta se encuentra deshabilitada",
            )
        return cuenta

    def iniciar_sesion(self, datos: InicioSesionEntrada) -> RespuestaToken:
        cuenta = self.validar_credenciales(datos)
        return self._emitir_tokens(cuenta)

    def renovar_token(self, valor: str) -> RespuestaAcceso:
        token = self.repositorio.buscar_token(valor)
        if token is None or not self.repositorio.token_vigente(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token de renovacion invalido o vencido",
            )
        cuenta = self.repositorio.buscar_cuenta_por_id(token.cuenta_id)
        if cuenta is None or not cuenta.habilitado:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="La cuenta asociada no esta disponible",
            )
        perfiles = self.repositorio.consultar_perfiles(cuenta.id)
        nuevo_acceso = generar_token_acceso(
            {"sub": str(cuenta.id), "correo": cuenta.correo, "perfiles": perfiles}
        )
        return RespuestaAcceso(token_acceso=nuevo_acceso)

    def cerrar_sesion(self, valor: str) -> None:
        token = self.repositorio.buscar_token(valor)
        if token is not None:
            self.repositorio.revocar_token(token)
