import { useEffect } from "react"
import { Link, useSearchParams } from "react-router-dom"
import { Clock } from "lucide-react"
import { useQueryClient } from "@tanstack/react-query"
import { clavesConsulta } from "@/lib/clavesConsulta"
import { carritoStore } from "@/almacenes/carritoStore"

export function PaginaPagoPendiente() {
  const [params] = useSearchParams()
  const cliente = useQueryClient()
  const limpiarCarrito = carritoStore((s) => s.vaciarCarrito)

  const ordenId = params.get("external_reference")

  useEffect(() => {
    limpiarCarrito()
    cliente.invalidateQueries({ queryKey: clavesConsulta.ordenes.misOrdenes() })
    if (ordenId) {
      cliente.invalidateQueries({
        queryKey: clavesConsulta.ordenes.detalle(Number(ordenId)),
      })
    }
  }, [limpiarCarrito, cliente, ordenId])

  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center gap-6 text-center">
      <div className="flex h-20 w-20 items-center justify-center rounded-full bg-yellow-100 text-yellow-500">
        <Clock className="h-10 w-10" />
      </div>
      <div className="space-y-2">
        <h1 className="text-2xl font-bold text-yellow-700">Pago pendiente</h1>
        <p className="text-gray-500 max-w-sm">
          Tu pago está en proceso. Si elegiste un medio offline (efectivo, Rapipago, etc.),
          completá el pago con el comprobante que te envió Mercado Pago.
        </p>
        <p className="text-sm text-gray-400">
          Una vez acreditado, el estado de tu pedido se actualizará automáticamente.
        </p>
      </div>
      <div className="flex gap-3">
        {ordenId && (
          <Link
            to={`/mis-ordenes/${ordenId}`}
            className="rounded-xl bg-primario-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-primario-700"
          >
            Ver mi pedido
          </Link>
        )}
        <Link
          to="/mis-ordenes"
          className="rounded-xl border border-gray-200 px-5 py-2.5 text-sm font-medium text-gray-600 hover:bg-gray-50"
        >
          Mis órdenes
        </Link>
      </div>
    </div>
  )
}
