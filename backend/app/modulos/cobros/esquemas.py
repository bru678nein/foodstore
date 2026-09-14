from __future__ import annotations

from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel

class PreferenciaEntrada(BaseModel):
    orden_id: int

class PreferenciaSalida(BaseModel):
    id_preferencia: str
    init_point: str
    cobro_id: int

class CobroSalida(BaseModel):
    id: int
    orden_id: int
    estado_cobro: str
    monto: Decimal
    medio: Optional[str] = None
    id_pago_mp: Optional[str] = None
    id_preferencia_mp: Optional[str] = None

class PagoDirectoEntrada(BaseModel):
    orden_id: int
    token: str
    payment_method_id: str
    cuotas: int = 1
    issuer_id: Optional[str] = None
    email_pagador: Optional[str] = None

class PagoDirectoSalida(BaseModel):
    id_pago_mp: str
    estado: str
    detalle: Optional[str] = None

class WebhookEntrada(BaseModel):
    type: Optional[str] = None
    action: Optional[str] = None
    data: Optional[dict[str, Any]] = None
