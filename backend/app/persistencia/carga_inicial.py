from __future__ import annotations

from sqlmodel import Session, select

from app.nucleo.proteccion import cifrar_clave
from app.persistencia.entidades.catalogo_ordenes import EstadoPedido, FormaPago
from app.persistencia.entidades.cuenta import Cuenta, CuentaPerfil, Perfil
from app.persistencia.entidades.unidad_medida import UnidadMedida
from app.persistencia.motor import motor

PERFILES_BASE = ["ADMINISTRADOR", "INVENTARIO", "DESPACHO", "COMPRADOR"]

CORREO_ADMIN = "admin@foodstore.com"
CLAVE_ADMIN = "Admin1234!"

ESTADOS_PEDIDO = [
    {"codigo": "PENDIENTE",    "descripcion": "Pedido creado, pago pendiente",      "orden": 1, "es_terminal": False},
    {"codigo": "CONFIRMADO",   "descripcion": "Pago procesado y confirmado",         "orden": 2, "es_terminal": False},
    {"codigo": "EN_PREPARACION", "descripcion": "En preparacion en cocina",          "orden": 3, "es_terminal": False},
    {"codigo": "ENTREGADO",    "descripcion": "Entrega confirmada",                  "orden": 4, "es_terminal": True},
    {"codigo": "CANCELADO",    "descripcion": "Pedido cancelado",                    "orden": 5, "es_terminal": True},
]

FORMAS_PAGO = [
    {"codigo": "MERCADOPAGO",   "descripcion": "MercadoPago Checkout PRO",    "habilitada": True},
    {"codigo": "MP_CARD",       "descripcion": "Tarjeta vía MercadoPago",     "habilitada": True},
    {"codigo": "EFECTIVO",      "descripcion": "Pago en efectivo",             "habilitada": True},
    {"codigo": "TARJETA",       "descripcion": "Tarjeta al recibir",           "habilitada": True},
    {"codigo": "TRANSFERENCIA", "descripcion": "Transferencia bancaria",       "habilitada": True},
]

UNIDADES_MEDIDA = [
    {"nombre": "kilogramo", "simbolo": "kg",       "tipo": "peso"},
    {"nombre": "gramo",     "simbolo": "g",         "tipo": "peso"},
    {"nombre": "litro",     "simbolo": "L",         "tipo": "volumen"},
    {"nombre": "mililitro", "simbolo": "ml",        "tipo": "volumen"},
    {"nombre": "unidad",    "simbolo": "ud",        "tipo": "contable"},
    {"nombre": "porcion",   "simbolo": "porciones", "tipo": "contable"},
]

def ejecutar_carga_inicial(sesion: Session | None = None) -> None:
    propia = sesion is None
    sesion = sesion or Session(motor)
    try:
        nombres_perfiles: dict[str, Perfil] = {}
        for nombre in PERFILES_BASE:
            existente = sesion.exec(select(Perfil).where(Perfil.nombre == nombre)).first()
            if existente is None:
                existente = Perfil(nombre=nombre)
                sesion.add(existente)
                sesion.flush()
            nombres_perfiles[nombre] = existente

        for ep in ESTADOS_PEDIDO:
            if not sesion.exec(select(EstadoPedido).where(EstadoPedido.codigo == ep["codigo"])).first():
                sesion.add(EstadoPedido(**ep))

        for fp in FORMAS_PAGO:
            if not sesion.exec(select(FormaPago).where(FormaPago.codigo == fp["codigo"])).first():
                sesion.add(FormaPago(**fp))

        for um in UNIDADES_MEDIDA:
            if not sesion.exec(select(UnidadMedida).where(UnidadMedida.simbolo == um["simbolo"])).first():
                sesion.add(UnidadMedida(**um))

        admin = sesion.exec(select(Cuenta).where(Cuenta.correo == CORREO_ADMIN)).first()
        if admin is None:
            admin = Cuenta(
                correo=CORREO_ADMIN,
                clave_hash=cifrar_clave(CLAVE_ADMIN),
                nombre_completo="Administrador General",
                habilitado=True,
            )
            sesion.add(admin)
            sesion.flush()
            sesion.add(
                CuentaPerfil(
                    cuenta_id=admin.id,
                    perfil_id=nombres_perfiles["ADMINISTRADOR"].id,
                )
            )

        sesion.commit()
    finally:
        if propia:
            sesion.close()
