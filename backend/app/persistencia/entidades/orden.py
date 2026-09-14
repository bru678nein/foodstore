from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel

COSTO_ENVIO_DEFAULT = Decimal("50.00")

def _instante_actual() -> datetime:
    return datetime.now(timezone.utc)

class Orden(SQLModel, table=True):

    __tablename__ = "orden"

    id: Optional[int] = Field(default=None, primary_key=True)
    cuenta_id: int = Field(foreign_key="cuenta.id", index=True)
    domicilio_id: Optional[int] = Field(default=None, foreign_key="domicilio.id")
    tipo_entrega: str = Field(default="DOMICILIO", max_length=20)
    estado_actual: str = Field(default="PENDIENTE", max_length=30, index=True)
    forma_pago_codigo: str = Field(default="MERCADOPAGO", max_length=20)
    subtotal: Decimal = Field(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    descuento: Decimal = Field(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    costo_envio: Decimal = Field(max_digits=10, decimal_places=2, default=COSTO_ENVIO_DEFAULT)
    total: Decimal = Field(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    observaciones: Optional[str] = Field(default=None, max_length=500)
    registrada_en: datetime = Field(default_factory=_instante_actual, index=True)
    actualizada_en: datetime = Field(default_factory=_instante_actual)

class PartidaOrden(SQLModel, table=True):

    __tablename__ = "partida_orden"

    id: Optional[int] = Field(default=None, primary_key=True)
    orden_id: int = Field(foreign_key="orden.id", index=True)
    articulo_id: Optional[int] = Field(default=None, foreign_key="articulo.id")
    titulo_capturado: str = Field(max_length=200)
    precio_capturado: Decimal = Field(max_digits=10, decimal_places=2)
    unidades: int = Field(default=1)
    subtotal_snap: Decimal = Field(max_digits=10, decimal_places=2)
    componentes_excluidos: Optional[str] = Field(default=None, max_length=1000)

class BitacoraOrden(SQLModel, table=True):

    __tablename__ = "bitacora_orden"

    id: Optional[int] = Field(default=None, primary_key=True)
    orden_id: int = Field(foreign_key="orden.id", index=True)
    estado_previo: Optional[str] = Field(default=None, max_length=30)
    estado_siguiente: str = Field(max_length=30)
    ejecutado_por: int = Field(foreign_key="cuenta.id")
    comentario: Optional[str] = Field(default=None, max_length=500)
    registrado_en: datetime = Field(default_factory=_instante_actual)

class Cobro(SQLModel, table=True):

    __tablename__ = "cobro"

    id: Optional[int] = Field(default=None, primary_key=True)
    orden_id: int = Field(foreign_key="orden.id", unique=True, index=True)
    id_pago_mp: Optional[str] = Field(default=None, max_length=100, unique=True)
    id_preferencia_mp: Optional[str] = Field(default=None, max_length=100)
    clave_idempotencia: str = Field(max_length=100, unique=True)
    monto: Decimal = Field(max_digits=10, decimal_places=2)
    medio: Optional[str] = Field(default=None, max_length=50)
    estado_cobro: str = Field(default="pendiente", max_length=30)
    mp_status_detail: Optional[str] = Field(default=None, max_length=100)
    transaction_amount: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    payment_method_id: Optional[str] = Field(default=None, max_length=50)
    iniciado_en: datetime = Field(default_factory=_instante_actual)
    actualizado_en: datetime = Field(default_factory=_instante_actual)
