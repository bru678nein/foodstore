from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.modulos.componentes.esquemas import ComponenteEntrada, ComponenteSalida
from app.modulos.componentes.repositorio import RepositorioComponentes
from app.persistencia.entidades.componente import Componente
from app.persistencia.sesion_trabajo import GestorTransaccion

class ServicioComponentes:
    def __init__(self, repositorio: RepositorioComponentes, gestor: GestorTransaccion) -> None:
        self.repositorio = repositorio
        self.gestor = gestor

    @staticmethod
    def _a_salida(c: Componente) -> ComponenteSalida:
        return ComponenteSalida(
            id=c.id,
            denominacion=c.denominacion,
            existencias=c.existencias,
            precio_unitario=c.precio_unitario,
            unidad=c.unidad,
            genera_alergia=c.genera_alergia,
        )

    def _obtener(self, componente_id: int) -> Componente:
        c = self.repositorio.buscar(componente_id)
        if c is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Componente no encontrado",
            )
        return c

    def listar(self) -> list[ComponenteSalida]:
        return [self._a_salida(c) for c in self.repositorio.listar()]

    def crear(self, datos: ComponenteEntrada) -> ComponenteSalida:
        componente = Componente(**datos.model_dump())
        self.repositorio.guardar(componente)
        return self._a_salida(componente)

    def actualizar(self, componente_id: int, datos: ComponenteEntrada) -> ComponenteSalida:
        componente = self._obtener(componente_id)
        for campo, valor in datos.model_dump().items():
            setattr(componente, campo, valor)
        self.repositorio.guardar(componente)
        return self._a_salida(componente)

    def eliminar(self, componente_id: int) -> None:
        componente = self._obtener(componente_id)
        componente.eliminado_en = datetime.now(timezone.utc)
        self.repositorio.guardar(componente)
