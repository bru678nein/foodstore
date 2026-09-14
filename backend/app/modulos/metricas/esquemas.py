from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel

class ResumenMetricas(BaseModel):
    ventas_hoy: Decimal
    ventas_mes: Decimal
    ticket_promedio: Decimal
    ordenes_activas: int

class PuntoVenta(BaseModel):
    etiqueta: str
    total: Decimal
    cantidad: int

class ArticuloDestacado(BaseModel):
    articulo_id: int | None = None
    titulo: str
    unidades_vendidas: int

class ConteoEstado(BaseModel):
    estado: str
    cantidad: int

class IngresoPorMedio(BaseModel):
    medio: str
    total: Decimal
