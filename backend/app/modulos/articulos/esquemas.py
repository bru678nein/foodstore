from __future__ import annotations

import math
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

class ComposicionEntrada(BaseModel):
    componente_id: int
    extraible: bool = False
    cantidad_gramos: int = 0

class ArticuloEntrada(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    descripcion: Optional[str] = Field(default=None, max_length=1000)
    precio_unitario: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    existencias: int = Field(default=0, ge=0)
    disponible: bool = True
    es_prefabricado: bool = False
    categorias: list[int] = []
    composicion: list[ComposicionEntrada] = []

class ExistenciasEntrada(BaseModel):
    existencias: int = Field(ge=0)

class CategoriaBasica(BaseModel):
    id: int
    nombre: str

class ImagenGaleria(BaseModel):
    id: int
    url: str
    orden: int = 0

class ComposicionItem(BaseModel):
    id: int
    denominacion: str
    extraible: bool
    cantidad_gramos: int = 0

class ArticuloListaSalida(BaseModel):
    id: int
    titulo: str
    precio_unitario: Decimal
    existencias: int
    disponible: bool
    es_prefabricado: bool = False
    categorias: list[CategoriaBasica] = []
    imagen_principal: Optional[str] = None

class ArticuloDetalleSalida(ArticuloListaSalida):
    descripcion: Optional[str] = None
    galeria: list[ImagenGaleria] = []
    composicion: list[ComposicionItem] = []

class PaginaArticulos(BaseModel):
    total: int
    pagina: int
    por_pagina: int
    total_paginas: int
    items: list[ArticuloListaSalida]

    @classmethod
    def construir(cls, total: int, pagina: int, por_pagina: int, items: list[ArticuloListaSalida]) -> "PaginaArticulos":
        total_paginas = max(1, math.ceil(total / por_pagina)) if por_pagina > 0 else 1
        return cls(total=total, pagina=pagina, por_pagina=por_pagina, total_paginas=total_paginas, items=items)
