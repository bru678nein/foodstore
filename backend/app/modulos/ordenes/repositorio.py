from __future__ import annotations

from typing import Optional

from sqlmodel import select

from app.persistencia.base_repositorio import BaseRepositorio
from app.persistencia.entidades.articulo import Articulo, ComposicionArticulo
from app.persistencia.entidades.componente import Componente
from app.persistencia.entidades.domicilio import Domicilio
from app.persistencia.entidades.orden import (
    BitacoraOrden,
    Cobro,
    Orden,
    PartidaOrden,
)

class RepositorioOrdenes(BaseRepositorio[Orden]):

    def buscar_articulo(self, articulo_id: int) -> Optional[Articulo]:
        consulta = select(Articulo).where(
            Articulo.id == articulo_id, Articulo.eliminado_en.is_(None)
        )
        return self.sesion.exec(consulta).first()

    def buscar_domicilio(self, domicilio_id: int, cuenta_id: int) -> Optional[Domicilio]:
        consulta = select(Domicilio).where(
            Domicilio.id == domicilio_id,
            Domicilio.cuenta_id == cuenta_id,
            Domicilio.eliminado_en.is_(None),
        )
        return self.sesion.exec(consulta).first()

    def buscar_domicilio_por_id(self, domicilio_id: int | None) -> Optional[Domicilio]:
        if domicilio_id is None:
            return None
        return self.sesion.get(Domicilio, domicilio_id)

    def guardar_orden(self, orden: Orden) -> Orden:
        return self.guardar(orden)

    def buscar_orden(self, orden_id: int) -> Optional[Orden]:
        return self.sesion.get(Orden, orden_id)

    def listar_todas(self) -> list[Orden]:
        consulta = select(Orden).order_by(Orden.registrada_en.desc())
        return list(self.sesion.exec(consulta).all())

    def listar_por_cuenta(self, cuenta_id: int) -> list[Orden]:
        consulta = (
            select(Orden)
            .where(Orden.cuenta_id == cuenta_id)
            .order_by(Orden.registrada_en.desc())
        )
        return list(self.sesion.exec(consulta).all())

    def agregar_partida(self, partida: PartidaOrden) -> PartidaOrden:
        return self.guardar(partida)

    def partidas_de(self, orden_id: int) -> list[PartidaOrden]:
        consulta = select(PartidaOrden).where(PartidaOrden.orden_id == orden_id)
        return list(self.sesion.exec(consulta).all())

    def agregar_bitacora(self, registro: BitacoraOrden) -> BitacoraOrden:
        return self.guardar(registro)

    def bitacora_de(self, orden_id: int) -> list[BitacoraOrden]:
        consulta = (
            select(BitacoraOrden)
            .where(BitacoraOrden.orden_id == orden_id)
            .order_by(BitacoraOrden.registrado_en)
        )
        return list(self.sesion.exec(consulta).all())

    def cobro_de(self, orden_id: int) -> Optional[Cobro]:
        consulta = select(Cobro).where(Cobro.orden_id == orden_id)
        return self.sesion.exec(consulta).first()

    def guardar_articulo(self, articulo: Articulo) -> None:
        self.guardar(articulo)

    def composiciones_de(self, articulo_id: int) -> list[ComposicionArticulo]:
        consulta = select(ComposicionArticulo).where(ComposicionArticulo.articulo_id == articulo_id)
        return list(self.sesion.exec(consulta).all())

    def buscar_componente(self, componente_id: int) -> Optional[Componente]:
        return self.sesion.get(Componente, componente_id)

    def guardar_componente(self, componente: Componente) -> None:
        self.guardar(componente)
