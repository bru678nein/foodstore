import { clienteHttp } from "../clienteHttp"
import type {
  ArticuloDestacado,
  DistribucionEstado,
  IngresoPorMedio,
  PeriodoMetricas,
  PuntoVenta,
  ResumenMetricas,
} from "@/tipos/admin"

export async function obtenerResumen(): Promise<ResumenMetricas> {
  const { data } = await clienteHttp.get<ResumenMetricas>("/metricas/resumen")
  return data
}

export async function obtenerVentas(
  periodo: PeriodoMetricas,
): Promise<PuntoVenta[]> {
  const { data } = await clienteHttp.get<PuntoVenta[]>("/metricas/ventas", {
    params: { periodo },
  })
  return data
}

export async function obtenerArticulosDestacados(): Promise<
  ArticuloDestacado[]
> {
  const { data } = await clienteHttp.get<ArticuloDestacado[]>(
    "/metricas/articulos-destacados",
  )
  return data
}

export async function obtenerDistribucionEstados(): Promise<
  DistribucionEstado[]
> {
  const { data } = await clienteHttp.get<DistribucionEstado[]>(
    "/metricas/distribucion-estados",
  )
  return data
}

export async function obtenerIngresosPorMedio(): Promise<IngresoPorMedio[]> {
  const { data } = await clienteHttp.get<IngresoPorMedio[]>(
    "/metricas/ingresos-por-medio",
  )
  return data
}
