import { Link, useParams } from "react-router-dom"
import { DetalleOrden } from "@/funcionalidades/ordenes/DetalleOrden"

export function PaginaDetalleOrden() {
  const { id } = useParams<{ id: string }>()
  const ordenId = Number(id)

  return (
    <div className="space-y-4">
      <Link
        to="/mis-ordenes"
        className="text-sm text-gray-500 hover:text-primario-600"
      >
        ← Volver a mis órdenes
      </Link>
      <DetalleOrden ordenId={ordenId} />
    </div>
  )
}
