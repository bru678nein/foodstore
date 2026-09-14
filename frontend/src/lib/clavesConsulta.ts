import type { ParametrosArticulos } from "@/tipos/catalogo"
import type { PeriodoMetricas } from "@/tipos/admin"

export const clavesConsulta = {
  sesion: {
    miCuenta: () => ["sesion", "mi-cuenta"] as const,
  },
  articulos: {
    todos: () => ["articulos"] as const,
    lista: (params: ParametrosArticulos) =>
      ["articulos", "lista", params] as const,
    detalle: (id: number) => ["articulos", id] as const,
  },
  categorias: {
    lista: () => ["categorias", "lista"] as const,
  },
  componentes: {
    lista: () => ["componentes", "lista"] as const,
  },
  ordenes: {
    misOrdenes: () => ["ordenes", "mis-ordenes"] as const,
    detalle: (id: number) => ["ordenes", id] as const,
    todas: () => ["ordenes", "todas"] as const,
  },
  domicilios: {
    lista: () => ["domicilios", "lista"] as const,
  },
  cobros: {
    estado: (ordenId: number) => ["cobros", ordenId] as const,
  },
  metricas: {
    resumen: () => ["metricas", "resumen"] as const,
    ventas: (p: PeriodoMetricas) => ["metricas", "ventas", p] as const,
    destacados: () => ["metricas", "destacados"] as const,
    distribucion: () => ["metricas", "distribucion"] as const,
    ingresos: () => ["metricas", "ingresos"] as const,
  },
  admin: {
    cuentas: () => ["admin", "cuentas"] as const,
  },
}
