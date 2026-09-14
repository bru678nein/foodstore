import { UtensilsCrossed } from "lucide-react"
import { TarjetaArticulo } from "./TarjetaArticulo"
import { Spinner } from "@/componentes/ui/Spinner"
import type { ArticuloLista } from "@/tipos/catalogo"

interface PropsGrillaArticulos {
  articulos: ArticuloLista[]
  cargando: boolean
}

export function GrillaArticulos({ articulos, cargando }: PropsGrillaArticulos) {
  if (cargando) {
    return <Spinner texto="Cargando artículos..." />
  }

  if (articulos.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center gap-3 py-16 text-center">
        <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-crema-100 text-primario-300">
          <UtensilsCrossed className="h-8 w-8" />
        </div>
        <p className="text-lg font-bold text-gray-700">No encontramos artículos</p>
        <p className="text-sm text-gray-400">Probá con otra búsqueda o filtro.</p>
      </div>
    )
  }

  return (
    <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
      {articulos.map((articulo) => (
        <TarjetaArticulo key={articulo.id} articulo={articulo} />
      ))}
    </div>
  )
}
