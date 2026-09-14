from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel

def _instante_actual() -> datetime:
    return datetime.now(timezone.utc)

class ArticuloCategoria(SQLModel, table=True):

    __tablename__ = "articulo_categoria"

    articulo_id: int = Field(foreign_key="articulo.id", primary_key=True)
    categoria_id: int = Field(foreign_key="categoria.id", primary_key=True)

class ArticuloImagen(SQLModel, table=True):

    __tablename__ = "articulo_imagen"

    id: Optional[int] = Field(default=None, primary_key=True)
    articulo_id: int = Field(foreign_key="articulo.id", index=True)
    url_imagen: str = Field(max_length=500)
    id_cdn: str = Field(max_length=200)
    posicion: int = Field(default=0)

class ComposicionArticulo(SQLModel, table=True):

    __tablename__ = "composicion_articulo"

    articulo_id: int = Field(foreign_key="articulo.id", primary_key=True)
    componente_id: int = Field(foreign_key="componente.id", primary_key=True)
    extraible: bool = Field(default=False)
    cantidad: Decimal = Field(default=Decimal("1.000"), max_digits=10, decimal_places=3)
    unidad_medida_id: Optional[int] = Field(default=None, foreign_key="unidad_medida.id")

class Articulo(SQLModel, table=True):

    __tablename__ = "articulo"

    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str = Field(max_length=200, index=True)
    descripcion: Optional[str] = Field(default=None, max_length=1000)
    precio_unitario: Decimal = Field(max_digits=10, decimal_places=2)
    existencias: int = Field(default=0)
    disponible: bool = Field(default=True)
    es_prefabricado: bool = Field(default=False)
    unidad_venta_id: Optional[int] = Field(default=None, foreign_key="unidad_medida.id")
    eliminado_en: Optional[datetime] = Field(default=None)
    creado_en: datetime = Field(default_factory=_instante_actual)
    modificado_en: datetime = Field(default_factory=_instante_actual)
