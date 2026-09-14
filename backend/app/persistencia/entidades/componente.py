from __future__ import annotations

import enum
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel, Column
import sqlalchemy as sa


class UnidadMedida(str, enum.Enum):
    ML = "ml"
    L = "l"
    G = "g"
    KG = "kg"

class Componente(SQLModel, table=True):

    __tablename__ = "componente"

    id: Optional[int] = Field(default=None, primary_key=True)
    denominacion: str = Field(max_length=100, index=True)
    existencias: int = Field(default=0)
    precio_unitario: Decimal = Field(default=Decimal("0.00"), decimal_places=2, max_digits=10)
    unidad: UnidadMedida = Field(
        default=UnidadMedida.G,
        sa_column=Column(sa.String(2), nullable=False, server_default="g"),
    )
    genera_alergia: bool = Field(default=False)
    eliminado_en: Optional[datetime] = Field(default=None)
