export interface ElementoCarrito {
  articuloId: number
  titulo: string
  precioUnitario: number
  cantidad: number
  imagenUrl: string | null
  componentesAExcluir: number[]
}
