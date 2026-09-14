interface PropsPaginacion {
  paginaActual: number
  totalPaginas: number
  alCambiar: (pagina: number) => void
}

export function Paginacion({ paginaActual, totalPaginas, alCambiar }: PropsPaginacion) {
  if (totalPaginas <= 1) return null

  const irA = (p: number) => {
    if (p >= 1 && p <= totalPaginas && p !== paginaActual) alCambiar(p)
  }

  return (
    <nav className="flex items-center justify-center gap-3 py-6">
      <button
        onClick={() => irA(paginaActual - 1)}
        disabled={paginaActual <= 1}
        className="rounded-xl border-2 border-crema-300 bg-white px-4 py-2 text-sm font-bold text-gray-700 transition-all hover:border-primario-300 hover:bg-primario-50 disabled:opacity-40"
      >
        ← Anterior
      </button>
      <span className="rounded-xl bg-primario-500 px-4 py-2 text-sm font-bold text-white shadow-sm">
        {paginaActual} / {totalPaginas}
      </span>
      <button
        onClick={() => irA(paginaActual + 1)}
        disabled={paginaActual >= totalPaginas}
        className="rounded-xl border-2 border-crema-300 bg-white px-4 py-2 text-sm font-bold text-gray-700 transition-all hover:border-primario-300 hover:bg-primario-50 disabled:opacity-40"
      >
        Siguiente →
      </button>
    </nav>
  )
}
