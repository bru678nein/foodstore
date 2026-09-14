import { useEffect } from "react"
import { useNavigate, useSearchParams } from "react-router-dom"
import { useQueryClient } from "@tanstack/react-query"
import { CheckCircle } from "lucide-react"
import { clavesConsulta } from "@/lib/clavesConsulta"
import { carritoStore } from "@/almacenes/carritoStore"
import { useDetalleOrden } from "@/funcionalidades/ordenes/hooks/useDetalleOrden"

const SEGUNDOS_REDIRECCION = 4

export function PaginaPagoExito() {
  const [params] = useSearchParams()
  const navigate = useNavigate()
  const cliente = useQueryClient()
  const limpiarCarrito = carritoStore((s) => s.vaciarCarrito)

  const ordenId = params.get("external_reference")
  const paymentId = params.get("payment_id")
  const ordenIdNum = Number(ordenId)

  const { data: orden } = useDetalleOrden(ordenIdNum)

  useEffect(() => {
    limpiarCarrito()
    cliente.invalidateQueries({ queryKey: clavesConsulta.ordenes.misOrdenes() })
    if (ordenId) {
      cliente.invalidateQueries({ queryKey: clavesConsulta.ordenes.detalle(ordenIdNum) })
    }
  }, [limpiarCarrito, cliente, ordenId, ordenIdNum])

  useEffect(() => {
    if (!ordenId) return
    const timer = setTimeout(() => {
      navigate(`/mis-ordenes/${ordenId}`, { replace: true })
    }, SEGUNDOS_REDIRECCION * 1000)
    return () => clearTimeout(timer)
  }, [ordenId, navigate])

  const descripcionItems = orden?.partidas
    .map((p) => `${p.unidades > 1 ? `${p.unidades}× ` : ""}${p.titulo_capturado}`)
    .join(", ")

  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center gap-6 text-center px-4">
      <div className="flex h-20 w-20 items-center justify-center rounded-full bg-green-100">
        <CheckCircle className="h-10 w-10 text-green-600" />
      </div>

      <div className="space-y-3 max-w-md">
        <h1 className="text-2xl font-bold text-green-700">¡Muchas gracias!</h1>

        <p className="text-gray-700">
          {paymentId ? (
            <>
              Tu pago con id{" "}
              <span className="font-semibold font-mono text-sm bg-gray-100 px-1.5 py-0.5 rounded">
                {paymentId}
              </span>
              {descripcionItems && (
                <> de <span className="font-semibold">{descripcionItems}</span></>
              )}{" "}
              fue completado.
            </>
          ) : descripcionItems ? (
            <>
              Tu pedido de <span className="font-semibold">{descripcionItems}</span> fue confirmado.
            </>
          ) : (
            "Tu pedido fue confirmado y está siendo procesado."
          )}
        </p>

        {ordenId && (
          <p className="text-xs text-gray-400">
            Redirigiendo al seguimiento en {SEGUNDOS_REDIRECCION} segundos...
          </p>
        )}
      </div>

      {ordenId && (
        <button
          onClick={() => navigate(`/mis-ordenes/${ordenId}`, { replace: true })}
          className="rounded-xl bg-primario-600 px-6 py-2.5 text-sm font-medium text-white hover:bg-primario-700 transition-colors"
        >
          Ver mi pedido →
        </button>
      )}
    </div>
  )
}
