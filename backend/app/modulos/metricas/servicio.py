from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal

from sqlmodel import Session, select

from app.modulos.metricas.esquemas import (
    ArticuloDestacado,
    ConteoEstado,
    IngresoPorMedio,
    PuntoVenta,
    ResumenMetricas,
)
from app.persistencia.entidades.orden import (
    Cobro,
    Orden,
    PartidaOrden,
)

ESTADOS_TERMINALES = {"ENTREGADO", "CANCELADO"}
ESTADO_ANULADO = "CANCELADO"

def _a_utc(valor: datetime) -> datetime:
    return valor if valor.tzinfo else valor.replace(tzinfo=timezone.utc)

class ServicioMetricas:
    def __init__(self, sesion: Session) -> None:
        self.sesion = sesion

    def _ordenes_validas(self) -> list[Orden]:
        consulta = select(Orden).where(Orden.estado_actual != ESTADO_ANULADO)
        return list(self.sesion.exec(consulta).all())

    def resumen(self) -> ResumenMetricas:
        ordenes = self._ordenes_validas()
        ahora = datetime.now(timezone.utc)
        hoy = ahora.date()

        ventas_hoy = Decimal("0.00")
        ventas_mes = Decimal("0.00")
        total_general = Decimal("0.00")
        for orden in ordenes:
            fecha = _a_utc(orden.registrada_en)
            total_general += orden.total
            if fecha.date() == hoy:
                ventas_hoy += orden.total
            if fecha.year == ahora.year and fecha.month == ahora.month:
                ventas_mes += orden.total

        cantidad = len(ordenes)
        ticket = (total_general / cantidad) if cantidad else Decimal("0.00")
        ticket = ticket.quantize(Decimal("0.01"))

        activas = self.sesion.exec(
            select(Orden).where(Orden.estado_actual.notin_(ESTADOS_TERMINALES))
        ).all()

        return ResumenMetricas(
            ventas_hoy=ventas_hoy,
            ventas_mes=ventas_mes,
            ticket_promedio=ticket,
            ordenes_activas=len(list(activas)),
        )

    def ventas_por_periodo(self, periodo: str) -> list[PuntoVenta]:
        ordenes = self._ordenes_validas()
        agrupado: dict[str, list] = defaultdict(lambda: [Decimal("0.00"), 0])
        for orden in ordenes:
            fecha = _a_utc(orden.registrada_en)
            if periodo == "mes":
                clave = fecha.strftime("%Y-%m")
            elif periodo == "semana":
                iso = fecha.isocalendar()
                clave = f"{iso[0]}-S{iso[1]:02d}"
            else:
                clave = fecha.strftime("%Y-%m-%d")
            agrupado[clave][0] += orden.total
            agrupado[clave][1] += 1
        return [
            PuntoVenta(etiqueta=clave, total=valores[0], cantidad=valores[1])
            for clave, valores in sorted(agrupado.items())
        ]

    def articulos_destacados(self, limite: int = 10) -> list[ArticuloDestacado]:
        ids_anuladas = {
            o.id
            for o in self.sesion.exec(
                select(Orden).where(Orden.estado_actual == ESTADO_ANULADO)
            ).all()
        }
        partidas = self.sesion.exec(select(PartidaOrden)).all()
        acumulado: dict[tuple, int] = defaultdict(int)
        for p in partidas:
            if p.orden_id in ids_anuladas:
                continue
            acumulado[(p.articulo_id, p.titulo_capturado)] += p.unidades
        ordenados = sorted(acumulado.items(), key=lambda x: x[1], reverse=True)
        return [
            ArticuloDestacado(
                articulo_id=clave[0], titulo=clave[1], unidades_vendidas=unidades
            )
            for clave, unidades in ordenados[:limite]
        ]

    def distribucion_estados(self) -> list[ConteoEstado]:
        conteo: dict[str, int] = defaultdict(int)
        for orden in self.sesion.exec(select(Orden)).all():
            conteo[orden.estado_actual] += 1
        return [
            ConteoEstado(estado=estado, cantidad=cantidad)
            for estado, cantidad in sorted(conteo.items())
        ]

    def ingresos_por_medio(self) -> list[IngresoPorMedio]:
        cobros = self.sesion.exec(
            select(Cobro).where(Cobro.estado_cobro == "approved")
        ).all()
        acumulado: dict[str, Decimal] = defaultdict(lambda: Decimal("0.00"))
        for cobro in cobros:
            acumulado[cobro.medio or "desconocido"] += cobro.monto
        return [
            IngresoPorMedio(medio=medio, total=total)
            for medio, total in sorted(acumulado.items())
        ]
