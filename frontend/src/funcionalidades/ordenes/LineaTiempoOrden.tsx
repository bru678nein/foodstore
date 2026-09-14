import { InsigniaEstado } from "@/componentes/comunes/InsigniaEstado"
import { formatearFecha } from "@/lib/formato"
import type { EntradaBitacora } from "@/tipos/ordenes"

export function LineaTiempoOrden({ bitacora }: { bitacora: EntradaBitacora[] }) {
  if (!bitacora || bitacora.length === 0) {
    return <p className="text-sm text-gray-400">Sin historial registrado.</p>
  }

  return (
    <ol className="relative space-y-5 border-l border-gray-200 pl-6">
      {bitacora.map((entrada, indice) => (
        <li key={indice} className="relative">
          <span className="absolute -left-[1.65rem] top-1 flex h-3 w-3 items-center justify-center">
            <span className="h-3 w-3 rounded-full bg-primario-500 ring-4 ring-primario-100" />
          </span>
          <div className="flex flex-wrap items-center gap-2">
            <InsigniaEstado estado={entrada.estado} />
            <span className="text-xs text-gray-400">
              {formatearFecha(entrada.registrada_en)}
            </span>
          </div>
          {entrada.nota && (
            <p className="mt-1 text-sm text-gray-600">{entrada.nota}</p>
          )}
        </li>
      ))}
    </ol>
  )
}
