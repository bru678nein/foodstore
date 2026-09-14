from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

class PartidaEntrada(BaseModel):
    articulo_id: int
    unidades: int = Field(gt=0)
    componentes_a_excluir: list[int] = []

class CrearOrdenEntrada(BaseModel):
    domicilio_id: Optional[int] = None
    tipo_entrega: str = Field(default="DOMICILIO", max_length=20)
    forma_pago_codigo: str = Field(default="MERCADOPAGO", max_length=20)
    partidas: list[PartidaEntrada] = Field(min_length=1)
    observaciones: Optional[str] = Field(default=None, max_length=500)

class CambioEstadoEntrada(BaseModel):
    estado_nuevo: str
    comentario: Optional[str] = Field(default=None, max_length=500)

class RespuestaPartida(BaseModel):
    id: int
    articulo_id: Optional[int] = None
    titulo_capturado: str
    precio_capturado: Decimal
    unidades: int
    importe_parcial: Decimal
    componentes_excluidos: list[str] = []

class RespuestaBitacora(BaseModel):
    id: int
    estado_previo: Optional[str] = None
    estado: str
    ejecutado_por: int
    nota: Optional[str] = None
    registrada_en: datetime

class DomicilioOrden(BaseModel):
    id: int
    via: str
    altura: str
    localidad: str
    provincia: str

class CobroOrden(BaseModel):
    id: int
    estado: str
    monto: Decimal
    medio: Optional[str] = None
    preferencia_id: Optional[str] = None

class RespuestaOrden(BaseModel):
    id: int
    cuenta_id: int = 0
    estado_actual: str
    tipo_entrega: str
    forma_pago_codigo: str
    subtotal: Decimal
    descuento: Decimal
    costo_envio: Decimal
    total: Decimal
    observaciones: Optional[str] = None
    domicilio: Optional[DomicilioOrden] = None
    partidas: list[RespuestaPartida] = []
    bitacora: list[RespuestaBitacora] = []
    cobro: Optional[CobroOrden] = None
    registrada_en: datetime
