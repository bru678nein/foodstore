import { useEffect, useState } from "react"
import { useQueryClient } from "@tanstack/react-query"
import { TrendingUp, Calendar, Receipt, Flame } from "lucide-react"
import { TarjetaKpi } from "@/funcionalidades/admin/tablero/TarjetaKpi"
import { GraficoVentas } from "@/funcionalidades/admin/tablero/GraficoVentas"
import { GraficoTopArticulos } from "@/funcionalidades/admin/tablero/GraficoTopArticulos"
import { GraficoDistribucionEstados } from "@/funcionalidades/admin/tablero/GraficoDistribucionEstados"
import { GraficoIngresosPorMedio } from "@/funcionalidades/admin/tablero/GraficoIngresosPorMedio"
import {
  useArticulosDestacados,
  useDistribucionEstados,
  useIngresosPorMedio,
  useResumenMetricas,
  useVentas,
} from "@/funcionalidades/admin/tablero/hooks/useMetricas"
import { useConexionWS } from "@/hooks/useConexionWS"
import { Spinner } from "@/componentes/ui/Spinner"
import { formatearMoneda } from "@/lib/formato"
import type { PeriodoMetricas } from "@/tipos/admin"

const PERIODOS: { valor: PeriodoMetricas; etiqueta: string }[] = [
  { valor: "dia", etiqueta: "Día" },
  { valor: "semana", etiqueta: "Semana" },
  { valor: "mes", etiqueta: "Mes" },
]

export function PaginaTablero() {
  const cliente = useQueryClient()
  const [periodo, setPeriodo] = useState<PeriodoMetricas>("semana")
  const resumen = useResumenMetricas()
  const ventas = useVentas(periodo)
  const destacados = useArticulosDestacados()
  const distribucion = useDistribucionEstados()
  const ingresos = useIngresosPorMedio()
  const { ultimoEvento } = useConexionWS("admin")

    useEffect(() => {
    if (!ultimoEvento) return
    cliente.invalidateQueries({ queryKey: ["metricas"] })
    cliente.invalidateQueries({ queryKey: ["ordenes", "todas"] })
  }, [ultimoEvento, cliente])

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Tablero</h1>

      {resumen.isLoading ? (
        <Spinner />
      ) : (
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <TarjetaKpi
            titulo="Ventas hoy"
            valor={formatearMoneda(resumen.data?.ventas_hoy ?? 0)}
            icono={<TrendingUp className="h-5 w-5" />}
          />
          <TarjetaKpi
            titulo="Ventas del mes"
            valor={formatearMoneda(resumen.data?.ventas_mes ?? 0)}
            icono={<Calendar className="h-5 w-5" />}
            color="bg-secundario-500/10 text-secundario-600"
          />
          <TarjetaKpi
            titulo="Ticket promedio"
            valor={formatearMoneda(resumen.data?.ticket_promedio ?? 0)}
            icono={<Receipt className="h-5 w-5" />}
            color="bg-green-50 text-green-600"
          />
          <TarjetaKpi
            titulo="Órdenes activas"
            valor={String(resumen.data?.ordenes_activas ?? 0)}
            icono={<Flame className="h-5 w-5" />}
            color="bg-yellow-50 text-yellow-600"
          />
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="font-semibold">Evolución de ventas</h2>
            <div className="flex gap-1">
              {PERIODOS.map((p) => (
                <button
                  key={p.valor}
                  onClick={() => setPeriodo(p.valor)}
                  className={`rounded-md px-2.5 py-1 text-xs font-medium ${
                    periodo === p.valor
                      ? "bg-primario-500 text-white"
                      : "bg-gray-100 text-gray-600"
                  }`}
                >
                  {p.etiqueta}
                </button>
              ))}
            </div>
          </div>
          <GraficoVentas datos={ventas.data} cargando={ventas.isLoading} />
        </div>

        <div className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
          <h2 className="mb-4 font-semibold">Distribución de estados</h2>
          <GraficoDistribucionEstados
            datos={distribucion.data}
            cargando={distribucion.isLoading}
          />
        </div>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <div className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
          <h2 className="mb-4 font-semibold">Top 5 artículos vendidos</h2>
          <GraficoTopArticulos
            datos={destacados.data}
            cargando={destacados.isLoading}
          />
        </div>

        <div className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
          <h2 className="mb-4 font-semibold">Ingresos por forma de pago</h2>
          <GraficoIngresosPorMedio
            datos={ingresos.data}
            cargando={ingresos.isLoading}
          />
        </div>
      </div>
    </div>
  )
}
