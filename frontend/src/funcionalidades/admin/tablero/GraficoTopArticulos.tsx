import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts"
import { Spinner } from "@/componentes/ui/Spinner"
import type { ArticuloDestacado } from "@/tipos/admin"

interface PropsGraficoTopArticulos {
  datos: ArticuloDestacado[] | undefined
  cargando: boolean
}

export function GraficoTopArticulos({
  datos,
  cargando,
}: PropsGraficoTopArticulos) {
  if (cargando) return <Spinner />
  if (!datos || datos.length === 0)
    return <p className="py-10 text-center text-sm text-gray-400">Sin datos.</p>

  const top = datos.slice(0, 5)

  return (
    <ResponsiveContainer width="100%" height={300}>
      <BarChart
        data={top}
        layout="vertical"
        margin={{ top: 10, right: 20, left: 20, bottom: 0 }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
        <XAxis type="number" tick={{ fontSize: 12 }} />
        <YAxis
          type="category"
          dataKey="titulo"
          width={120}
          tick={{ fontSize: 12 }}
        />
        <Tooltip contentStyle={{ borderRadius: 8, fontSize: 13 }} />
        <Bar
          dataKey="unidades_vendidas"
          name="Unidades"
          fill="#0ea5e9"
          radius={[0, 4, 4, 0]}
        />
      </BarChart>
    </ResponsiveContainer>
  )
}
