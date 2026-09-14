import { Clock, CheckCircle2, Flame, PackageCheck, XCircle } from "lucide-react"
import { Insignia } from "@/componentes/ui/Insignia"
import type { EstadoOrden } from "@/tipos/ordenes"

const coloresPorEstado: Record<EstadoOrden, string> = {
  PENDIENTE:      "bg-yellow-100 text-yellow-800 border border-yellow-200",
  CONFIRMADO:     "bg-blue-100 text-blue-800 border border-blue-200",
  EN_PREPARACION: "bg-primario-100 text-primario-700 border border-primario-200",
  ENTREGADO:      "bg-green-100 text-green-800 border border-green-200",
  CANCELADO:      "bg-red-100 text-red-700 border border-red-200",
}

const etiquetaPorEstado: Record<EstadoOrden, string> = {
  PENDIENTE:      "Pendiente",
  CONFIRMADO:     "Confirmado",
  EN_PREPARACION: "En preparación",
  ENTREGADO:      "Entregado",
  CANCELADO:      "Cancelado",
}

const iconoPorEstado: Record<EstadoOrden, React.ReactNode> = {
  PENDIENTE:      <Clock className="h-3 w-3" />,
  CONFIRMADO:     <CheckCircle2 className="h-3 w-3" />,
  EN_PREPARACION: <Flame className="h-3 w-3" />,
  ENTREGADO:      <PackageCheck className="h-3 w-3" />,
  CANCELADO:      <XCircle className="h-3 w-3" />,
}

export function InsigniaEstado({ estado }: { estado: EstadoOrden }) {
  return (
    <Insignia className={coloresPorEstado[estado] ?? "bg-gray-100 text-gray-700"}>
      <span className="flex items-center gap-1">
        {iconoPorEstado[estado]}
        {etiquetaPorEstado[estado] ?? estado}
      </span>
    </Insignia>
  )
}
