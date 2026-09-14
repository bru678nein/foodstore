import { Insignia } from "@/componentes/ui/Insignia"
import { Spinner } from "@/componentes/ui/Spinner"
import type { Domicilio } from "@/tipos/ordenes"

interface PropsListaDomicilios {
  domicilios: Domicilio[] | undefined
  cargando: boolean
  seleccionableId?: number | null
  alSeleccionar?: (id: number) => void
  alPredeterminar?: (id: number) => void
  alEditar?: (domicilio: Domicilio) => void
  alEliminar?: (id: number) => void
}

export function ListaDomicilios({
  domicilios,
  cargando,
  seleccionableId,
  alSeleccionar,
  alPredeterminar,
  alEditar,
  alEliminar,
}: PropsListaDomicilios) {
  if (cargando) return <Spinner texto="Cargando domicilios..." />

  if (!domicilios || domicilios.length === 0) {
    return (
      <p className="rounded-lg border border-dashed border-gray-200 p-6 text-center text-sm text-gray-400">
        No tenés domicilios cargados todavía.
      </p>
    )
  }

  return (
    <div className="space-y-3">
      {domicilios.map((dom) => {
        const seleccionado = seleccionableId === dom.id
        return (
          <div
            key={dom.id}
            onClick={() => alSeleccionar?.(dom.id)}
            className={`rounded-xl border p-4 transition ${
              alSeleccionar ? "cursor-pointer" : ""
            } ${
              seleccionado
                ? "border-primario-500 ring-1 ring-primario-500"
                : "border-gray-100 hover:border-gray-200"
            }`}
          >
            <div className="flex items-start justify-between gap-2">
              <div>
                <p className="font-medium text-gray-900">
                  {dom.via} {dom.altura}
                </p>
                <p className="text-sm text-gray-500">
                  {dom.localidad}, {dom.provincia}
                  {dom.codigo_postal ? ` · ${dom.codigo_postal}` : ""}
                </p>
              </div>
              {dom.es_predeterminado && (
                <Insignia className="bg-primario-100 text-primario-700">
                  Predeterminado
                </Insignia>
              )}
            </div>

            {(alPredeterminar || alEditar || alEliminar) && (
              <div className="mt-3 flex gap-3 text-xs">
                {alPredeterminar && !dom.es_predeterminado && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      alPredeterminar(dom.id)
                    }}
                    className="text-secundario-600 hover:underline"
                  >
                    Marcar predeterminado
                  </button>
                )}
                {alEditar && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      alEditar(dom)
                    }}
                    className="text-gray-500 hover:underline"
                  >
                    Editar
                  </button>
                )}
                {alEliminar && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      alEliminar(dom.id)
                    }}
                    className="text-error hover:underline"
                  >
                    Eliminar
                  </button>
                )}
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}
