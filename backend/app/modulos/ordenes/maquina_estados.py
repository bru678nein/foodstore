from __future__ import annotations

ESTADO_INICIAL = "PENDIENTE"

TRANSICIONES_VALIDAS: dict[str, list[str]] = {
    "PENDIENTE": ["CONFIRMADO", "CANCELADO"],
    "CONFIRMADO": ["EN_PREPARACION", "CANCELADO"],
    "EN_PREPARACION": ["ENTREGADO", "CANCELADO"],
    "ENTREGADO": [],
    "CANCELADO": [],
}

def validar_transicion(estado_actual: str, estado_nuevo: str) -> bool:
    return estado_nuevo in TRANSICIONES_VALIDAS.get(estado_actual, [])

def es_estado_terminal(estado: str) -> bool:
    return not TRANSICIONES_VALIDAS.get(estado, ["placeholder"])

def estados_posibles(estado_actual: str) -> list[str]:
    return list(TRANSICIONES_VALIDAS.get(estado_actual, []))
