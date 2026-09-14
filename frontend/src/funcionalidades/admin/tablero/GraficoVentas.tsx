import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts"
import { Spinner } from "@/componentes/ui/Spinner"
import { formatearMoneda } from "@/lib/formato"
import type { PuntoVenta } from "@/tipos/admin"

interface PropsGraficoVentas {
  datos: PuntoVenta[] | undefined
  cargando: boolean
}

export function GraficoVentas({ datos, cargando }: PropsGraficoVentas) {
  if (cargando) return <Spinner />
  if (!datos || datos.length === 0)
    return <p className="py-10 text-center text-sm text-gray-400">Sin datos.</p>

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={datos} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
        <XAxis dataKey="etiqueta" tick={{ fontSize: 12 }} />
        <YAxis tick={{ fontSize: 12 }} />
        <Tooltip
          formatter={(valor: number) => formatearMoneda(valor)}
          contentStyle={{ borderRadius: 8, fontSize: 13 }}
        />
        <Line
          type="monotone"
          dataKey="total"
          name="Ventas"
          stroke="#f97316"
          strokeWidth={2.5}
          dot={{ r: 3 }}
          activeDot={{ r: 5 }}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}
