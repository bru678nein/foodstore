import { useEffect } from "react"
import { useQueryClient } from "@tanstack/react-query"
import { Spinner } from "@/componentes/ui/Spinner"
import { TablaOrdenes } from "@/funcionalidades/admin/ordenes/TablaOrdenes"
import { useAdminOrdenes } from "@/funcionalidades/admin/ordenes/hooks/useAdminOrdenes"
import { useConexionWS } from "@/hooks/useConexionWS"
import { clavesConsulta } from "@/lib/clavesConsulta"

export function PaginaGestionOrdenes() {
  const cliente = useQueryClient()
  const { consulta, cambiarEstado } = useAdminOrdenes()
  const { ultimoEvento } = useConexionWS("ordenes")

  useEffect(() => {
    if (!ultimoEvento) return
    cliente.invalidateQueries({ queryKey: clavesConsulta.ordenes.todas() })
  }, [ultimoEvento, cliente])

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Gestión de órdenes</h1>
        {consulta.isFetching && (
          <span className="flex items-center gap-2 text-xs text-gray-400">
            <span className="h-2 w-2 animate-pulse rounded-full bg-green-400" />
            En vivo
          </span>
        )}
      </div>

      {consulta.isLoading ? (
        <Spinner />
      ) : (
        <TablaOrdenes
          ordenes={consulta.data ?? []}
          cambiandoId={cambiarEstado.isPending ? cambiarEstado.variables?.id : null}
          alCambiarEstado={(id, estado) => cambiarEstado.mutate({ id, estado })}
        />
      )}
    </div>
  )
}
