from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

from app.nucleo.ajustes import ajustes
from app.nucleo.limitador import limitador
from app.persistencia.carga_inicial import ejecutar_carga_inicial
from app.persistencia.motor import crear_tablas

from app.modulos.sesion.enrutador import enrutador as enrutador_sesion
from app.modulos.cuentas.enrutador import enrutador as enrutador_cuentas
from app.modulos.domicilios.enrutador import enrutador as enrutador_domicilios
from app.modulos.categorias.enrutador import enrutador as enrutador_categorias
from app.modulos.componentes.enrutador import enrutador as enrutador_componentes
from app.modulos.articulos.enrutador import enrutador as enrutador_articulos
from app.modulos.ordenes.enrutador import enrutador as enrutador_ordenes
from app.modulos.cobros.enrutador import enrutador as enrutador_cobros
from app.modulos.archivos.enrutador import enrutador as enrutador_archivos
from app.modulos.metricas.enrutador import enrutador as enrutador_metricas
from app.modulos.tiempo_real.enrutador import enrutador as enrutador_tiempo_real

@asynccontextmanager
async def ciclo_vida(_: FastAPI):
    crear_tablas()
    ejecutar_carga_inicial()
    yield

def crear_aplicacion() -> FastAPI:
    aplicacion = FastAPI(
        title=ajustes.nombre_app,
        version=ajustes.version,
        debug=ajustes.debug,
        lifespan=ciclo_vida,
    )

    aplicacion.state.limiter = limitador
    aplicacion.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    aplicacion.add_middleware(SlowAPIMiddleware)

    aplicacion.add_middleware(
        CORSMiddleware,
        allow_origins=ajustes.origenes_lista,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    prefijo = ajustes.prefijo_api
    aplicacion.include_router(enrutador_sesion, prefix=prefijo)
    aplicacion.include_router(enrutador_cuentas, prefix=prefijo)
    aplicacion.include_router(enrutador_domicilios, prefix=prefijo)
    aplicacion.include_router(enrutador_categorias, prefix=prefijo)
    aplicacion.include_router(enrutador_componentes, prefix=prefijo)
    aplicacion.include_router(enrutador_articulos, prefix=prefijo)
    aplicacion.include_router(enrutador_ordenes, prefix=prefijo)
    aplicacion.include_router(enrutador_cobros, prefix=prefijo)
    aplicacion.include_router(enrutador_archivos, prefix=prefijo)
    aplicacion.include_router(enrutador_metricas, prefix=prefijo)
    aplicacion.include_router(enrutador_tiempo_real)

    @aplicacion.get("/", tags=["sistema"])
    def raiz() -> dict[str, str]:
        return {
            "aplicacion": ajustes.nombre_app,
            "version": ajustes.version,
            "documentacion": "/docs",
        }

    @aplicacion.get("/estado", tags=["sistema"])
    def estado() -> dict[str, str]:
        return {"estado": "operativo"}

    return aplicacion

aplicacion = crear_aplicacion()
