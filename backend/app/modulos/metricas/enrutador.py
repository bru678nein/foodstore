from __future__ import annotations

from fastapi import APIRouter, Depends, Query

from app.nucleo.dependencias import requerir_perfil
from app.modulos.metricas.esquemas import (
    ArticuloDestacado,
    ConteoEstado,
    IngresoPorMedio,
    PuntoVenta,
    ResumenMetricas,
)
from app.modulos.metricas.servicio import ServicioMetricas
from app.persistencia.sesion_trabajo import GestorTransaccion, obtener_gestor

enrutador = APIRouter(
    prefix="/metricas",
    tags=["metricas"],
    dependencies=[Depends(requerir_perfil("ADMINISTRADOR"))],
)

def obtener_servicio(
    gestor: GestorTransaccion = Depends(obtener_gestor),
) -> ServicioMetricas:
    return ServicioMetricas(gestor.sesion)

@enrutador.get("/resumen", response_model=ResumenMetricas)
def resumen(servicio: ServicioMetricas = Depends(obtener_servicio)) -> ResumenMetricas:
    return servicio.resumen()

@enrutador.get("/ventas", response_model=list[PuntoVenta])
def ventas(
    periodo: str = Query(default="dia", pattern="^(dia|semana|mes)$"),
    servicio: ServicioMetricas = Depends(obtener_servicio),
) -> list[PuntoVenta]:
    return servicio.ventas_por_periodo(periodo)

@enrutador.get("/articulos-destacados", response_model=list[ArticuloDestacado])
def articulos_destacados(
    servicio: ServicioMetricas = Depends(obtener_servicio),
) -> list[ArticuloDestacado]:
    return servicio.articulos_destacados()

@enrutador.get("/distribucion-estados", response_model=list[ConteoEstado])
def distribucion_estados(
    servicio: ServicioMetricas = Depends(obtener_servicio),
) -> list[ConteoEstado]:
    return servicio.distribucion_estados()

@enrutador.get("/ingresos-por-medio", response_model=list[IngresoPorMedio])
def ingresos_por_medio(
    servicio: ServicioMetricas = Depends(obtener_servicio),
) -> list[IngresoPorMedio]:
    return servicio.ingresos_por_medio()
