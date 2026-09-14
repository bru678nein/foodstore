import { useEffect, useMemo, useState } from "react"
import { Flame } from "lucide-react"
import { BarraBusqueda } from "@/funcionalidades/catalogo/BarraBusqueda"
import { FiltroPorCategoria } from "@/funcionalidades/catalogo/FiltroPorCategoria"
import { GrillaArticulos } from "@/funcionalidades/catalogo/GrillaArticulos"
import { useConsultaArticulos } from "@/funcionalidades/catalogo/hooks/useConsultaArticulos"
import { Paginacion } from "@/componentes/ui/Paginacion"
import { useDebounce } from "@/hooks/useDebounce"

export function PaginaCatalogo() {
  const [busqueda, setBusqueda] = useState("")
  const [categoria, setCategoria] = useState<number | undefined>(undefined)
  const [pagina, setPagina] = useState(1)
  const busquedaDebounced = useDebounce(busqueda, 400)

  useEffect(() => {
    setPagina(1)
  }, [busquedaDebounced, categoria])

  const params = useMemo(
    () => ({ q: busquedaDebounced, categoria, pagina, porPagina: 12 }),
    [busquedaDebounced, categoria, pagina],
  )

  const { data, isLoading, isFetching } = useConsultaArticulos(params)

  return (
    <div className="space-y-6">
      
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-primario-500 via-primario-600 to-calido-500 p-8 text-white shadow-tarjeta-hover">
        <div className="pointer-events-none absolute -right-8 -top-8 h-40 w-40 rounded-full bg-white/10" />
        <div className="pointer-events-none absolute -bottom-12 -right-4 h-52 w-52 rounded-full bg-white/5" />
        <div className="pointer-events-none absolute left-1/2 top-0 h-24 w-24 -translate-x-1/2 rounded-full bg-white/5" />

        <div className="relative">
          <p className="mb-1 flex items-center gap-1.5 text-sm font-bold uppercase tracking-widest text-primario-100">
            <Flame className="h-3.5 w-3.5" /> Lo mejor de hoy
          </p>
          <h1 className="text-3xl font-extrabold leading-tight sm:text-4xl">
            ¡Tu comida favorita,
            <br />
            en minutos!
          </h1>
          <p className="mt-3 font-semibold text-primario-100">
            Explorá el catálogo y armá tu pedido. Rápido, fácil y rico.
          </p>
        </div>
      </div>

      
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
        <FiltroPorCategoria categoriaActiva={categoria} alSeleccionar={setCategoria} />
        <div className="w-full lg:w-72">
          <BarraBusqueda valor={busqueda} alCambiar={setBusqueda} />
        </div>
      </div>

      <GrillaArticulos
        articulos={data?.items ?? []}
        cargando={isLoading || (isFetching && !data)}
      />

      <Paginacion
        paginaActual={data?.pagina ?? pagina}
        totalPaginas={data?.total_paginas ?? 1}
        alCambiar={setPagina}
      />
    </div>
  )
}
