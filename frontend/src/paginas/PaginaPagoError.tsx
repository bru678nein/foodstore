import { Link, useSearchParams } from "react-router-dom"

export function PaginaPagoError() {
  const [params] = useSearchParams()
  const ordenId = params.get("external_reference")

  return (
    <div className="flex min-h-[60vh] flex-col items-center justify-center gap-6 text-center">
      <div className="flex h-20 w-20 items-center justify-center rounded-full bg-red-100 text-4xl">
        ✕
      </div>
      <div className="space-y-2">
        <h1 className="text-2xl font-bold text-red-700">Pago rechazado</h1>
        <p className="text-gray-500">
          No se pudo procesar tu pago. Podés intentarlo de nuevo o elegir otro medio de pago.
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
