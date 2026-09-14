import { Search } from "lucide-react"

interface PropsBarraBusqueda {
  valor: string
  alCambiar: (valor: string) => void
}

export function BarraBusqueda({ valor, alCambiar }: PropsBarraBusqueda) {
  return (
    <div className="relative">
      <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
      <input
        type="search"
        placeholder="Buscar artículos..."
        value={valor}
        onChange={(e) => alCambiar(e.target.value)}
        className="w-full rounded-lg border border-gray-300 py-2 pl-10 pr-3 text-sm shadow-sm focus:border-primario-500 focus:outline-none focus:ring-2 focus:ring-primario-500"
      />
    </div>
  )
}
