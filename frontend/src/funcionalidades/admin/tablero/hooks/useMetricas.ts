import { useQuery } from "@tanstack/react-query"
import {
  obtenerArticulosDestacados,
  obtenerDistribucionEstados,
  obtenerIngresosPorMedio,
  obtenerResumen,
  obtenerVentas,
} from "@/api/endpoints/metricas"
import { clavesConsulta } from "@/lib/clavesConsulta"
import type { PeriodoMetricas } from "@/tipos/admin"

export function useResumenMetricas() {
  return useQuery({
    queryKey: clavesConsulta.metricas.resumen(),
    queryFn: obtenerResumen,
  })
}

export function useVentas(periodo: PeriodoMetricas) {
  return useQuery({
    queryKey: clavesConsulta.metricas.ventas(periodo),
    queryFn: () => obtenerVentas(periodo),
  })
}

export function useArticulosDestacados() {
  return useQuery({
    queryKey: clavesConsulta.metricas.destacados(),
    queryFn: obtenerArticulosDestacados,
  })
}

export function useDistribucionEstados() {
  return useQuery({
    queryKey: clavesConsulta.metricas.distribucion(),
    queryFn: obtenerDistribucionEstados,
  })
}

export function useIngresosPorMedio() {
  return useQuery({
    queryKey: clavesConsulta.metricas.ingresos(),
    queryFn: obtenerIngresosPorMedio,
  })
}
