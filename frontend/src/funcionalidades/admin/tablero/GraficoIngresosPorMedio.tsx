import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts"
import { Spinner } from "@/componentes/ui/Spinner"
import { formatearMoneda } from "@/lib/formato"
import type { IngresoPorMedio } from "@/tipos/admin"

interface Props {
  datos: IngresoPorMedio[] | undefined
  cargando: boolean
}

const COLORES = ["#6366f1", "#22c55e", "#f59e0b", "#ef4444", "#3b82f6"]

export function GraficoIngresosPorMedio({ datos, cargando }: Props) {
  if (cargando) return <Spinner />
  if (!datos || datos.length === 0)
    return (
      <p className="py-10 text-center text-sm text-gray-400">
        Sin cobros aprobados aún.
      </p>
    )

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart data={datos} margin={{ top: 5, right: 16, left: 8, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
        <XAxis dataKey="medio" tick={{ fontSize: 12 }} />
        <YAxis
          tickFormatter={(v) => formatearMoneda(v)}
          tick={{ fontSize: 11 }}
          width={80}
        />
        <Tooltip
          formatter={(value: number) => [formatearMoneda(value), "Ingresos"]}
          contentStyle={{ borderRadius: 8, fontSize: 13 }}
        />
        <Bar dataKey="total" radius={[4, 4, 0, 0]}>
          {datos.map((entry, i) => (
            <Cell key={entry.medio} fill={COLORES[i % COLORES.length]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
