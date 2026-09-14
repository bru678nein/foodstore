from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.modulos.domicilios.esquemas import DomicilioEntrada, DomicilioSalida
from app.modulos.domicilios.repositorio import RepositorioDomicilios
from app.persistencia.entidades.domicilio import Domicilio
from app.persistencia.sesion_trabajo import GestorTransaccion

class ServicioDomicilios:
    def __init__(self, repositorio: RepositorioDomicilios, gestor: GestorTransaccion) -> None:
        self.repositorio = repositorio
        self.gestor = gestor

    @staticmethod
    def _a_salida(dom: Domicilio) -> DomicilioSalida:
        return DomicilioSalida(
            id=dom.id,
            via=dom.via,
            altura=dom.altura,
            localidad=dom.localidad,
            provincia=dom.provincia,
            codigo_postal=dom.codigo_postal,
            es_predeterminado=dom.es_predeterminado,
        )

    def _obtener(self, domicilio_id: int, cuenta_id: int) -> Domicilio:
        dom = self.repositorio.buscar(domicilio_id, cuenta_id)
        if dom is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Domicilio no encontrado",
            )
        return dom

    def listar(self, cuenta_id: int) -> list[DomicilioSalida]:
        return [self._a_salida(d) for d in self.repositorio.listar_por_cuenta(cuenta_id)]

    def crear(self, cuenta_id: int, datos: DomicilioEntrada) -> DomicilioSalida:
        if datos.es_predeterminado:
            self.repositorio.quitar_predeterminado(cuenta_id)
        dom = Domicilio(cuenta_id=cuenta_id, **datos.model_dump())
        self.repositorio.guardar(dom)
        return self._a_salida(dom)

    def actualizar(
        self, domicilio_id: int, cuenta_id: int, datos: DomicilioEntrada
    ) -> DomicilioSalida:
        dom = self._obtener(domicilio_id, cuenta_id)
        if datos.es_predeterminado and not dom.es_predeterminado:
            self.repositorio.quitar_predeterminado(cuenta_id)
        for campo, valor in datos.model_dump().items():
            setattr(dom, campo, valor)
        self.repositorio.guardar(dom)
        return self._a_salida(dom)

    def eliminar(self, domicilio_id: int, cuenta_id: int) -> None:
        dom = self._obtener(domicilio_id, cuenta_id)
        dom.eliminado_en = datetime.now(timezone.utc)
        self.repositorio.guardar(dom)

    def marcar_predeterminado(self, domicilio_id: int, cuenta_id: int) -> DomicilioSalida:
        dom = self._obtener(domicilio_id, cuenta_id)
        self.repositorio.quitar_predeterminado(cuenta_id)
        dom.es_predeterminado = True
        self.repositorio.guardar(dom)
        return self._a_salida(dom)
