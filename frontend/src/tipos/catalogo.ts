export interface CategoriaBasica {
  id: number
  nombre: string
}

export interface CategoriaSalida {
  id: number
  nombre: string
  descripcion?: string | null
  imagen_url?: string | null
  padre_id?: number | null
  hijos: CategoriaSalida[]
}

export interface ImagenArticulo {
  id: number
  url: string
  orden?: number
}

export interface ComposicionItem {
  id: number
  denominacion: string
  extraible: boolean
  cantidad_gramos: number
}

export interface ArticuloLista {
  id: number
  titulo: string
  precio_unitario: number | string
  existencias: number
  disponible: boolean
  es_prefabricado: boolean
  categorias: CategoriaBasica[]
  imagen_principal: string | null
}

export interface ArticuloDetalle extends ArticuloLista {
  descripcion: string
  galeria: ImagenArticulo[]
  composicion: ComposicionItem[]
}

export interface RespuestaPaginada<T> {
  items: T[]
  total: number
  pagina: number
  por_pagina: number
  total_paginas: number
}

export interface ParametrosArticulos {
  categoria?: number
  disponible?: boolean
  q?: string
  pagina?: number
  porPagina?: number
}

export type UnidadMedida = "ml" | "l" | "g" | "kg"

export interface Componente {
  id: number
  denominacion: string
  existencias: number
  precio_unitario: number
  unidad: UnidadMedida
  genera_alergia: boolean
}

export interface EntradaArticulo {
  titulo: string
  descripcion: string
  precio_unitario: number
  existencias: number
  disponible: boolean
  es_prefabricado: boolean
  categorias: number[]
  composicion?: { componente_id: number; extraible: boolean; cantidad_gramos: number }[]
}

export interface EntradaCategoria {
  nombre: string
  padre_id?: number | null
}

export interface EntradaComponente {
  denominacion: string
  existencias?: number
  precio_unitario?: number
  unidad?: UnidadMedida
  genera_alergia?: boolean
}
