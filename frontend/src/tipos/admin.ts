import type { EstadoOrden } from "./ordenes"

export interface CuentaAdmin {
  id: number
  correo: string
  nombre_completo: string
  habilitado: boolean
  perfiles: string[]
  creado_en?: string
}

export const PERFILES_DISPONIBLES = [
  "ADMINISTRADOR",
  "INVENTARIO",
  "DESPACHO",
  "COMPRADOR",
] as const

export type PerfilDisponible = (typeof PERFILES_DISPONIBLES)[number]

export interface ResumenMetricas {
  ventas_hoy: number
  ventas_mes: number
  ticket_promedio: number
  ordenes_activas: number
}

export interface PuntoVenta {
  etiqueta: string
  total: number
}

export interface ArticuloDestacado {
  articulo_id: number
  titulo: string
  unidades_vendidas: number
  total: number
}

export interface DistribucionEstado {
  estado: EstadoOrden
  cantidad: number
}

export interface IngresoPorMedio {
  medio: string
  total: number
}

export type PeriodoMetricas = "dia" | "semana" | "mes"
