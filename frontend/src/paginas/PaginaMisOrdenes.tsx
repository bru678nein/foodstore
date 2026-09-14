import { useEffect } from "react"
import { Link } from "react-router-dom"
import { Package } from "lucide-react"
import { useQueryClient } from "@tanstack/react-query"
import { Spinner } from "@/componentes/ui/Spinner"
import { TarjetaOrden } from "@/funcionalidades/ordenes/TarjetaOrden"
import { useMisOrdenes } from "@/funcionalidades/ordenes/hooks/useMisOrdenes"
import { useConexionWS } from "@/hooks/useConexionWS"
import { sesionStore } from "@/almacenes/sesionStore"
import { clavesConsulta } from "@/lib/clavesConsulta"

export function PaginaMisOrdenes() {
  const { data: ordenes, isLoading, isError } = useMisOrdenes()
  const cliente = useQueryClient()
  const cuentaId = sesionStore((s) => s.cuenta?.id)
  const { ultimoEvento } = useConexionWS(cuentaId ? `cuenta:${cuentaId}` : null)

  useEffect(() => {
    if (!ultimoEvento) return
    cliente.invalidateQueries({ queryKey: clavesConsulta.ordenes.misOrdenes() })
  }, [ultimoEvento, cliente])

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Mis órdenes</h1>

      {isLoading && <Spinner texto="Cargando órdenes..." />}
      {isError && (
        <p className="rounded-lg bg-red-50 px-4 py-3 text-error">
          No se pudieron cargar tus órdenes.
        </p>
      )}

      {ordenes && ordenes.length === 0 && (
        <div className="flex flex-col items-center gap-3 py-16 text-center">
          <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-crema-100 text-primario-300">
            <Package className="h-8 w-8" />
          </div>
          <p className="text-lg font-bold text-gray-700">Todavía no hiciste pedidos</p>
          <Link to="/" className="font-semibold text-primario-600 hover:underline">
            Ver catálogo
          </Link>
        </div>
      )}

      {ordenes && ordenes.length > 0 && (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {ordenes.map((orden) => (
            <TarjetaOrden key={orden.id} orden={orden} />
          ))}
        </div>
      )}
    </div>
  )
}
