import {
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
} from "recharts"
import { Spinner } from "@/componentes/ui/Spinner"
import type { DistribucionEstado } from "@/tipos/admin"
import type { EstadoOrden } from "@/tipos/ordenes"

interface PropsGraficoDistribucion {
  datos: DistribucionEstado[] | undefined
  cargando: boolean
}

const colores: Record<EstadoOrden, string> = {
  PENDIENTE: "#eab308",
  CONFIRMADO: "#3b82f6",
  EN_PREPARACION: "#f97316",
  ENTREGADO: "#22c55e",
  CANCELADO: "#ef4444",
}

export function GraficoDistribucionEstados({
  datos,
  cargando,
}: PropsGraficoDistribucion) {
  if (cargando) return <Spinner />
  if (!datos || datos.length === 0)
    return <p className="py-10 text-center text-sm text-gray-400">Sin datos.</p>

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={datos}
          dataKey="cantidad"
          nameKey="estado"
          cx="50%"
          cy="50%"
          outerRadius={90}
          label={(entrada) => `${entrada.estado}`}
        >
          {datos.map((entrada) => (
            <Cell
              key={entrada.estado}
              fill={colores[entrada.estado] ?? "#94a3b8"}
            />
          ))}
        </Pie>
        <Tooltip contentStyle={{ borderRadius: 8, fontSize: 13 }} />
        <Legend wrapperStyle={{ fontSize: 12 }} />
      </PieChart>
    </ResponsiveContainer>
  )
}
