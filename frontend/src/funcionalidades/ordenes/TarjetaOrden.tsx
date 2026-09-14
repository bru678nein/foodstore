import { Link } from "react-router-dom"
import { InsigniaEstado } from "@/componentes/comunes/InsigniaEstado"
import { formatearFecha, formatearMoneda } from "@/lib/formato"
import type { RespuestaOrden } from "@/tipos/ordenes"

export function TarjetaOrden({ orden }: { orden: RespuestaOrden }) {
  return (
    <Link
      to={`/mis-ordenes/${orden.id}`}
      className="block rounded-xl border border-gray-100 bg-white p-5 shadow-sm transition hover:shadow-md"
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="font-semibold text-gray-900">Orden #{orden.id}</p>
          <p className="text-sm text-gray-400">
            {formatearFecha(orden.registrada_en)}
          </p>
        </div>
        <InsigniaEstado estado={orden.estado_actual} />
      </div>
      <div className="mt-4 flex items-center justify-between">
        <span className="text-sm text-gray-500">
          {orden.partidas.length} artículo(s)
        </span>
        <span className="text-lg font-bold text-primario-600">
          {formatearMoneda(orden.total)}
        </span>
      </div>
    </Link>
  )
}
