from __future__ import annotations

import json
from datetime import datetime, timezone
from decimal import Decimal

from fastapi import HTTPException, status

from app.modulos.ordenes.esquemas import (
    CobroOrden,
    CrearOrdenEntrada,
    DomicilioOrden,
    RespuestaBitacora,
    RespuestaOrden,
    RespuestaPartida,
)
from app.modulos.ordenes.maquina_estados import (
    ESTADO_INICIAL,
    validar_transicion,
)
from app.modulos.ordenes.repositorio import RepositorioOrdenes
from app.persistencia.entidades.articulo import ComposicionArticulo
from app.persistencia.entidades.componente import Componente
from app.persistencia.entidades.orden import (
    BitacoraOrden,
    Orden,
    PartidaOrden,
    COSTO_ENVIO_DEFAULT,
)
from app.persistencia.sesion_trabajo import GestorTransaccion

ESTADOS_REPONEN_STOCK = {"PENDIENTE", "CONFIRMADO"}

class ServicioOrdenes:
    def __init__(self, repositorio: RepositorioOrdenes, gestor: GestorTransaccion) -> None:
        self.repositorio = repositorio
        self.gestor = gestor

    def _a_respuesta(self, orden: Orden) -> RespuestaOrden:
        partidas = []
        for p in self.repositorio.partidas_de(orden.id):
            excluidos = json.loads(p.componentes_excluidos) if p.componentes_excluidos else []
            partidas.append(
                RespuestaPartida(
                    id=p.id,
                    articulo_id=p.articulo_id,
                    titulo_capturado=p.titulo_capturado,
                    precio_capturado=p.precio_capturado,
                    unidades=p.unidades,
                    importe_parcial=p.subtotal_snap,
                    componentes_excluidos=excluidos,
                )
            )
        bitacora = [
            RespuestaBitacora(
                id=b.id,
                estado_previo=b.estado_previo,
                estado=b.estado_siguiente,
                ejecutado_por=b.ejecutado_por,
                nota=b.comentario,
                registrada_en=b.registrado_en,
            )
            for b in self.repositorio.bitacora_de(orden.id)
        ]
        domicilio = self.repositorio.buscar_domicilio_por_id(orden.domicilio_id)
        domicilio_dto = (
            DomicilioOrden(
                id=domicilio.id,
                via=domicilio.via,
                altura=domicilio.altura,
                localidad=domicilio.localidad,
                provincia=domicilio.provincia,
            )
            if domicilio
            else None
        )
        cobro = self.repositorio.cobro_de(orden.id)
        cobro_dto = (
            CobroOrden(
                id=cobro.id,
                estado=cobro.estado_cobro,
                monto=cobro.monto,
                medio=cobro.medio,
                preferencia_id=cobro.id_preferencia_mp,
            )
            if cobro
            else None
        )
        return RespuestaOrden(
            id=orden.id,
            cuenta_id=orden.cuenta_id,
            estado_actual=orden.estado_actual,
            tipo_entrega=orden.tipo_entrega,
            forma_pago_codigo=orden.forma_pago_codigo,
            subtotal=orden.subtotal,
            descuento=orden.descuento,
            costo_envio=orden.costo_envio,
            total=orden.total,
            observaciones=orden.observaciones,
            domicilio=domicilio_dto,
            partidas=partidas,
            bitacora=bitacora,
            cobro=cobro_dto,
            registrada_en=orden.registrada_en,
        )

    def _obtener(self, orden_id: int) -> Orden:
        orden = self.repositorio.buscar_orden(orden_id)
        if orden is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Orden no encontrada",
            )
        return orden

    def _nombres_componentes(self, ids: list[int]) -> list[str]:
        nombres = []
        for cid in ids:
            comp = self.repositorio.sesion.get(Componente, cid)
            if comp is not None:
                nombres.append(comp.denominacion)
        return nombres

    def crear_orden(self, cuenta_id: int, datos: CrearOrdenEntrada) -> RespuestaOrden:
        tipo = datos.tipo_entrega.upper()
        if tipo not in ("DOMICILIO", "LOCAL"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="tipo_entrega debe ser DOMICILIO o LOCAL",
            )

        domicilio = None
        if tipo == "DOMICILIO":
            if not datos.domicilio_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Se requiere domicilio_id para envío a domicilio",
                )
            domicilio = self.repositorio.buscar_domicilio(datos.domicilio_id, cuenta_id)
            if domicilio is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El domicilio indicado no pertenece a la cuenta",
                )

        forma_pago = datos.forma_pago_codigo.upper()
        if forma_pago == "EFECTIVO" and tipo != "LOCAL":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El pago en efectivo solo está disponible para retiro en local",
            )

        costo_envio = Decimal("0.00") if tipo == "LOCAL" else COSTO_ENVIO_DEFAULT

        orden = Orden(
            cuenta_id=cuenta_id,
            domicilio_id=domicilio.id if domicilio else None,
            tipo_entrega=tipo,
            estado_actual=ESTADO_INICIAL,
            forma_pago_codigo=datos.forma_pago_codigo,
            subtotal=Decimal("0.00"),
            descuento=Decimal("0.00"),
            costo_envio=costo_envio,
            total=Decimal("0.00"),
            observaciones=datos.observaciones,
        )
        self.repositorio.guardar_orden(orden)

        subtotal = Decimal("0.00")
        for linea in datos.partidas:
            articulo = self.repositorio.buscar_articulo(linea.articulo_id)
            if articulo is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Articulo {linea.articulo_id} inexistente",
                )
            if not articulo.disponible:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"El articulo '{articulo.titulo}' no esta disponible",
                )
            if articulo.existencias < linea.unidades:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Existencias insuficientes para '{articulo.titulo}'",
                )

            ids_excluidos = set(linea.componentes_a_excluir)
            composiciones = self.repositorio.composiciones_de(articulo.id)
            ops_componentes: list[tuple[Componente, Decimal]] = []
            for comp_rel in composiciones:
                if comp_rel.componente_id in ids_excluidos:
                    continue
                componente = self.repositorio.buscar_componente(comp_rel.componente_id)
                if componente is None:
                    continue
                total_necesario = comp_rel.cantidad * linea.unidades
                if Decimal(componente.existencias) < total_necesario:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=(
                            f"Stock insuficiente de '{componente.denominacion}': "
                            f"se necesitan {total_necesario} y hay {componente.existencias}"
                        ),
                    )
                ops_componentes.append((componente, total_necesario))

            subtotal_linea = articulo.precio_unitario * linea.unidades
            subtotal += subtotal_linea
            articulo.existencias -= linea.unidades
            self.repositorio.guardar_articulo(articulo)
            for componente, total in ops_componentes:
                componente.existencias -= int(total)
                self.repositorio.guardar_componente(componente)

            excluidos = self._nombres_componentes(linea.componentes_a_excluir)
            self.repositorio.agregar_partida(
                PartidaOrden(
                    orden_id=orden.id,
                    articulo_id=articulo.id,
                    titulo_capturado=articulo.titulo,
                    precio_capturado=articulo.precio_unitario,
                    unidades=linea.unidades,
                    subtotal_snap=subtotal_linea,
                    componentes_excluidos=json.dumps(excluidos) if excluidos else None,
                )
            )

        orden.subtotal = subtotal
        orden.total = subtotal - orden.descuento + orden.costo_envio
        orden.actualizada_en = datetime.now(timezone.utc)
        self.repositorio.guardar_orden(orden)

        self.repositorio.agregar_bitacora(
            BitacoraOrden(
                orden_id=orden.id,
                estado_previo=None,
                estado_siguiente=ESTADO_INICIAL,
                ejecutado_por=cuenta_id,
                comentario="Orden registrada",
            )
        )
        return self._a_respuesta(orden)

    def listar_todas(self) -> list[RespuestaOrden]:
        return [self._a_respuesta(o) for o in self.repositorio.listar_todas()]

    def listar_mias(self, cuenta_id: int) -> list[RespuestaOrden]:
        return [self._a_respuesta(o) for o in self.repositorio.listar_por_cuenta(cuenta_id)]

    def detalle(self, orden_id: int, cuenta_id: int, es_gestor: bool) -> RespuestaOrden:
        orden = self._obtener(orden_id)
        if not es_gestor and orden.cuenta_id != cuenta_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puede acceder a esta orden",
            )
        return self._a_respuesta(orden)

    def historial(self, orden_id: int, cuenta_id: int, es_gestor: bool) -> list[RespuestaBitacora]:
        orden = self._obtener(orden_id)
        if not es_gestor and orden.cuenta_id != cuenta_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puede acceder a esta orden",
            )
        return [
            RespuestaBitacora(
                id=b.id,
                estado_previo=b.estado_previo,
                estado=b.estado_siguiente,
                ejecutado_por=b.ejecutado_por,
                nota=b.comentario,
                registrada_en=b.registrado_en,
            )
            for b in self.repositorio.bitacora_de(orden_id)
        ]

    def _reponer_stock(self, orden: Orden) -> None:
        for p in self.repositorio.partidas_de(orden.id):
            if p.articulo_id is None:
                continue
            articulo = self.repositorio.buscar_articulo(p.articulo_id)
            if articulo is not None:
                articulo.existencias += p.unidades
                self.repositorio.guardar_articulo(articulo)
            excluidos_nombres = set(json.loads(p.componentes_excluidos) if p.componentes_excluidos else [])
            for comp_rel in self.repositorio.composiciones_de(p.articulo_id):
                componente = self.repositorio.buscar_componente(comp_rel.componente_id)
                if componente is None or componente.denominacion in excluidos_nombres:
                    continue
                componente.existencias += int(comp_rel.cantidad * p.unidades)
                self.repositorio.guardar_componente(componente)

    def cambiar_estado(
        self, orden_id: int, estado_nuevo: str, ejecutor_id: int, comentario: str | None
    ) -> RespuestaOrden:
        orden = self._obtener(orden_id)
        estado_previo = orden.estado_actual
        if not validar_transicion(estado_previo, estado_nuevo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Transicion invalida: {estado_previo} -> {estado_nuevo}",
            )
        if estado_nuevo == "CANCELADO" and estado_previo in ESTADOS_REPONEN_STOCK:
            self._reponer_stock(orden)

        orden.estado_actual = estado_nuevo
        orden.actualizada_en = datetime.now(timezone.utc)
        self.repositorio.guardar_orden(orden)
        self.repositorio.agregar_bitacora(
            BitacoraOrden(
                orden_id=orden.id,
                estado_previo=estado_previo,
                estado_siguiente=estado_nuevo,
                ejecutado_por=ejecutor_id,
                comentario=comentario,
            )
        )
        return self._a_respuesta(orden)

    def cancelar_por_comprador(self, orden_id: int, cuenta_id: int) -> RespuestaOrden:
        orden = self._obtener(orden_id)
        if orden.cuenta_id != cuenta_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No puede cancelar una orden ajena",
            )
        if orden.estado_actual != "PENDIENTE":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Solo se pueden cancelar ordenes en estado PENDIENTE",
            )
        return self.cambiar_estado(
            orden_id, "CANCELADO", cuenta_id, "Cancelada por el comprador"
        )
