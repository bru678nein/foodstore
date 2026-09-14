import { ControlEstadoOrden } from "./ControlEstadoOrden"
import { formatearMoneda } from "@/lib/formato"
import type { EstadoOrden, RespuestaOrden } from "@/tipos/ordenes"

const COLUMNAS: { estado: EstadoOrden; label: string; color: string }[] = [
  { estado: "PENDIENTE",      label: "Pendiente",      color: "border-yellow-300 bg-yellow-50" },
  { estado: "CONFIRMADO",     label: "Confirmado",     color: "border-blue-300 bg-blue-50" },
  { estado: "EN_PREPARACION", label: "En preparación", color: "border-orange-300 bg-orange-50" },
  { estado: "ENTREGADO",      label: "Entregado",      color: "border-green-300 bg-green-50" },
  { estado: "CANCELADO",      label: "Cancelado",      color: "border-red-200 bg-red-50" },
]

interface PropsTablaOrdenes {
  ordenes: RespuestaOrden[]
  alCambiarEstado: (id: number, estado: EstadoOrden) => void
  cambiandoId?: number | null
}

function TarjetaOrden({
  orden,
  cambiandoId,
  alCambiarEstado,
}: {
  orden: RespuestaOrden
  cambiandoId?: number | null
  alCambiarEstado: (id: number, estado: EstadoOrden) => void
}) {
  return (
    <div className="rounded-lg border border-gray-200 bg-white p-3 shadow-sm space-y-2">
      <div className="flex items-center justify-between">
        <span className="font-semibold text-sm">#{orden.id}</span>
        <span className="text-xs text-gray-400">
          {new Date(orden.registrada_en).toLocaleTimeString("es-AR", {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </span>
      </div>

      <ul className="space-y-0.5">
        {orden.partidas.map((p) => (
          <li key={p.id} className="text-xs text-gray-600">
            {p.unidades}× {p.titulo_capturado}
          </li>
        ))}
      </ul>

      <div className="flex items-center justify-between pt-1 border-t border-gray-100">
        <span className="text-xs font-medium text-gray-700">
          {formatearMoneda(orden.total)}
        </span>
        <ControlEstadoOrden
          estado={orden.estado_actual}
          deshabilitado={cambiandoId === orden.id}
          alCambiar={(estado) => alCambiarEstado(orden.id, estado)}
        />
      </div>
    </div>
  )
}

export function TablaOrdenes({ ordenes, alCambiarEstado, cambiandoId }: PropsTablaOrdenes) {
  const porEstado = (estado: EstadoOrden) =>
    ordenes
      .filter((o) => o.estado_actual === estado)
      .sort((a, b) => new Date(b.registrada_en).getTime() - new Date(a.registrada_en).getTime())

  return (
    <div className="grid grid-cols-5 gap-3 min-h-[60vh]">
      {COLUMNAS.map(({ estado, label, color }) => {
        const items = porEstado(estado)
        return (
          <div key={estado} className="flex flex-col gap-2">
            <div className={`rounded-lg border-2 px-3 py-2 ${color}`}>
              <span className="text-xs font-semibold uppercase tracking-wide text-gray-600">
                {label}
              </span>
              <span className="ml-2 rounded-full bg-white px-1.5 py-0.5 text-xs font-bold text-gray-500">
                {items.length}
              </span>
            </div>

            <div className="flex flex-col gap-2">
              {items.length === 0 ? (
                <p className="rounded-lg border border-dashed border-gray-200 p-4 text-center text-xs text-gray-300">
                  Sin órdenes
                </p>
              ) : (
                items.map((orden) => (
                  <TarjetaOrden
                    key={orden.id}
                    orden={orden}
                    cambiandoId={cambiandoId}
                    alCambiarEstado={alCambiarEstado}
                  />
                ))
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
}
