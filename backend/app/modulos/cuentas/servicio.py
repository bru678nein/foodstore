from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.modulos.cuentas.esquemas import CuentaDetalle
from app.modulos.cuentas.repositorio import RepositorioCuentas
from app.persistencia.entidades.cuenta import Cuenta
from app.persistencia.sesion_trabajo import GestorTransaccion

class ServicioCuentas:
    def __init__(self, repositorio: RepositorioCuentas, gestor: GestorTransaccion) -> None:
        self.repositorio = repositorio
        self.gestor = gestor

    def _a_detalle(self, cuenta: Cuenta) -> CuentaDetalle:
        return CuentaDetalle(
            id=cuenta.id,
            correo=cuenta.correo,
            nombre_completo=cuenta.nombre_completo,
            habilitado=cuenta.habilitado,
            perfiles=self.repositorio.consultar_perfiles(cuenta.id),
            creado_en=cuenta.creado_en,
        )

    def _obtener(self, cuenta_id: int) -> Cuenta:
        cuenta = self.repositorio.buscar_por_id(cuenta_id)
        if cuenta is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cuenta no encontrada",
            )
        return cuenta

    def listar(self) -> list[CuentaDetalle]:
        return [self._a_detalle(c) for c in self.repositorio.listar_todas()]

    def detalle(self, cuenta_id: int) -> CuentaDetalle:
        return self._a_detalle(self._obtener(cuenta_id))

    def cambiar_estado(self, cuenta_id: int, habilitado: bool) -> CuentaDetalle:
        cuenta = self._obtener(cuenta_id)
        cuenta.habilitado = habilitado
        cuenta.modificado_en = datetime.now(timezone.utc)
        self.repositorio.guardar(cuenta)
        return self._a_detalle(cuenta)

    def asignar_perfil(self, cuenta_id: int, nombre_perfil: str) -> CuentaDetalle:
        cuenta = self._obtener(cuenta_id)
        perfil = self.repositorio.buscar_perfil_por_nombre(nombre_perfil)
        if perfil is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Perfil inexistente",
            )
        self.repositorio.reemplazar_perfiles(cuenta_id, perfil)
        return self._a_detalle(cuenta)

    def eliminar(self, cuenta_id: int) -> None:
        cuenta = self._obtener(cuenta_id)
        cuenta.eliminado_en = datetime.now(timezone.utc)
        cuenta.habilitado = False
        self.repositorio.guardar(cuenta)
