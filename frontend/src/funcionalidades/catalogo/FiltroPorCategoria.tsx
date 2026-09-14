import { useConsultaCategorias } from "./hooks/useConsultaCategorias"
import type { CategoriaSalida } from "@/tipos/catalogo"

function aplanar(cats: CategoriaSalida[]): CategoriaSalida[] {
  return cats.flatMap((c) => [c, ...aplanar(c.hijos)])
}

interface PropsFiltroPorCategoria {
  categoriaActiva: number | undefined
  alSeleccionar: (categoriaId: number | undefined) => void
}

export function FiltroPorCategoria({
  categoriaActiva,
  alSeleccionar,
}: PropsFiltroPorCategoria) {
  const { data: categorias, isLoading } = useConsultaCategorias()

  const claseChip = (activo: boolean) =>
    `rounded-full px-3 py-1.5 text-sm font-medium transition ${
      activo
        ? "bg-primario-500 text-white"
        : "bg-white text-gray-600 ring-1 ring-gray-200 hover:bg-gray-50"
    }`

  const todas = aplanar(categorias ?? [])

  return (
    <div className="flex flex-wrap gap-2">
      <button
        className={claseChip(categoriaActiva === undefined)}
        onClick={() => alSeleccionar(undefined)}
      >
        Todos
      </button>
      {isLoading && (
        <span className="px-3 py-1.5 text-sm text-gray-400">Cargando...</span>
      )}
      {todas.map((categoria) => (
        <button
          key={categoria.id}
          className={claseChip(categoriaActiva === categoria.id)}
          onClick={() => alSeleccionar(categoria.id)}
        >
          {categoria.nombre}
        </button>
      ))}
    </div>
  )
}
