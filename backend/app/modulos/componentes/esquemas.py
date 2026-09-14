from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, Field

from app.persistencia.entidades.componente import UnidadMedida



class ComponenteEntrada(BaseModel):
    denominacion: str = Field(min_length=1, max_length=100)
    existencias: int = Field(default=0, ge=0)
    precio_unitario: Decimal = Field(default=Decimal("0.00"), ge=0)
    unidad: UnidadMedida = UnidadMedida.G
    genera_alergia: bool = False

class ComponenteSalida(BaseModel):
    id: int
    denominacion: str
    existencias: int
    precio_unitario: Decimal
    unidad: UnidadMedida
    genera_alergia: bool
