import type { EstadoOrden } from "@/tipos/ordenes"

const SIGUIENTE: Partial<Record<EstadoOrden, EstadoOrden>> = {
  PENDIENTE:      "CONFIRMADO",
  CONFIRMADO:     "EN_PREPARACION",
  EN_PREPARACION: "ENTREGADO",
}

const ETIQUETA_BOTON: Partial<Record<EstadoOrden, string>> = {
  PENDIENTE:      "Confirmar",
  CONFIRMADO:     "En preparación",
  EN_PREPARACION: "Entregar",
}

const PUEDE_CANCELAR: EstadoOrden[] = ["PENDIENTE", "CONFIRMADO"]

interface PropsControlEstadoOrden {
  estado: EstadoOrden
  deshabilitado?: boolean
  alCambiar: (estado: EstadoOrden) => void
}

export function ControlEstadoOrden({
  estado,
  deshabilitado,
  alCambiar,
}: PropsControlEstadoOrden) {
  const siguiente = SIGUIENTE[estado]
  const etiqueta = ETIQUETA_BOTON[estado]
  const puedeCancelar = PUEDE_CANCELAR.includes(estado)

  if (!siguiente) return <span className="text-xs text-gray-300">—</span>

  return (
    <div className="flex items-center gap-3">
      <button
        type="button"
        disabled={deshabilitado}
        onClick={() => alCambiar(siguiente)}
        className="rounded-lg bg-primario-500 px-3 py-1.5 text-xs font-medium text-white hover:bg-primario-600 disabled:opacity-50"
      >
        {etiqueta} →
      </button>
      {puedeCancelar && (
        <button
          type="button"
          disabled={deshabilitado}
          onClick={() => alCambiar("CANCELADO")}
          className="text-xs text-red-400 hover:text-red-600 disabled:opacity-40"
        >
          Cancelar
        </button>
      )}
    </div>
  )
}
