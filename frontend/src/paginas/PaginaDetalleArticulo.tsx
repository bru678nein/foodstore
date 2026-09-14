import { useState } from "react"
import { Link, useParams } from "react-router-dom"
import { UtensilsCrossed } from "lucide-react"
import { Boton } from "@/componentes/ui/Boton"
import { Insignia } from "@/componentes/ui/Insignia"
import { Spinner } from "@/componentes/ui/Spinner"
import { useConsultaArticulo } from "@/funcionalidades/catalogo/hooks/useConsultaArticulo"
import { carritoStore } from "@/almacenes/carritoStore"
import { formatearMoneda } from "@/lib/formato"

export function PaginaDetalleArticulo() {
  const { id } = useParams<{ id: string }>()
  const articuloId = Number(id)
  const { data: articulo, isLoading, isError } = useConsultaArticulo(articuloId)
  const agregarElemento = carritoStore((s) => s.agregarElemento)
  const abrirCarrito = carritoStore((s) => s.alternarCarrito)

  const [imagenActiva, setImagenActiva] = useState(0)
  const [excluidos, setExcluidos] = useState<number[]>([])
  const [cantidad, setCantidad] = useState(1)

  if (isLoading) return <Spinner texto="Cargando artículo..." />
  if (isError || !articulo)
    return (
      <div className="py-16 text-center">
        <p className="text-gray-500">No se pudo cargar el artículo.</p>
        <Link to="/" className="mt-3 inline-block text-primario-600">
          ← Volver al catálogo
        </Link>
      </div>
    )

  const sinStock = articulo.existencias <= 0 || !articulo.disponible
  const imagenes =
    articulo.galeria.length > 0
      ? articulo.galeria.map((g) => g.url)
      : articulo.imagen_principal
        ? [articulo.imagen_principal]
        : []

  const alternarExcluido = (compId: number) =>
    setExcluidos((prev) =>
      prev.includes(compId)
        ? prev.filter((x) => x !== compId)
        : [...prev, compId],
    )

  const manejarAgregar = () => {
    for (let i = 0; i < cantidad; i++) {
      agregarElemento({
        articuloId: articulo.id,
        titulo: articulo.titulo,
        precioUnitario: articulo.precio_unitario,
        imagenUrl: articulo.imagen_principal,
        componentesAExcluir: excluidos,
      })
    }
    abrirCarrito()
  }

  return (
    <div className="space-y-6">
      <Link to="/" className="text-sm text-gray-500 hover:text-primario-600">
        ← Volver al catálogo
      </Link>

      <div className="grid gap-8 lg:grid-cols-2">
        
        <div>
          <div className="aspect-square overflow-hidden rounded-2xl bg-gray-100">
            {imagenes[imagenActiva] ? (
              <img
                src={imagenes[imagenActiva]}
                alt={articulo.titulo}
                className="h-full w-full object-cover"
              />
            ) : (
              <div className="flex h-full w-full items-center justify-center text-gray-200">
                <UtensilsCrossed className="h-16 w-16" />
              </div>
            )}
          </div>
          {imagenes.length > 1 && (
            <div className="mt-3 flex gap-2">
              {imagenes.map((url, indice) => (
                <button
                  key={indice}
                  onClick={() => setImagenActiva(indice)}
                  className={`h-16 w-16 overflow-hidden rounded-lg border-2 ${
                    indice === imagenActiva
                      ? "border-primario-500"
                      : "border-transparent"
                  }`}
                >
                  <img src={url} alt="" className="h-full w-full object-cover" />
                </button>
              ))}
            </div>
          )}
        </div>

        
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold text-gray-900">
              {articulo.titulo}
            </h1>
            {sinStock && (
              <Insignia className="bg-red-100 text-red-700">Sin stock</Insignia>
            )}
          </div>
          {articulo.categorias.length > 0 && (
            <p className="mt-1 text-sm text-gray-400">
              {articulo.categorias.map((c) => c.nombre).join(" · ")}
            </p>
          )}
          <p className="mt-4 text-3xl font-bold text-primario-600">
            {formatearMoneda(articulo.precio_unitario)}
          </p>
          <p className="mt-4 leading-relaxed text-gray-600">
            {articulo.descripcion}
          </p>

          {articulo.composicion.length > 0 && (
            <div className="mt-6">
              <h2 className="mb-2 font-semibold text-gray-900">Ingredientes</h2>
              <div className="space-y-2">
                {articulo.composicion.map((comp) => (
                  <label
                    key={comp.id}
                    className={`flex items-center justify-between rounded-lg border px-3 py-2 ${
                      comp.extraible ? "cursor-pointer hover:bg-gray-50" : ""
                    }`}
                  >
                    <span className="text-sm text-gray-700">
                      {comp.denominacion}
                    </span>
                    {comp.extraible ? (
                      <input
                        type="checkbox"
                        checked={!excluidos.includes(comp.id)}
                        onChange={() => alternarExcluido(comp.id)}
                        className="h-4 w-4 accent-primario-500"
                      />
                    ) : (
                      <span className="text-xs text-gray-400">fijo</span>
                    )}
                  </label>
                ))}
              </div>
            </div>
          )}

          <div className="mt-6 flex items-center gap-4">
            <div className="flex items-center gap-2">
              <button
                onClick={() => setCantidad((c) => Math.max(1, c - 1))}
                className="flex h-9 w-9 items-center justify-center rounded-lg border border-gray-300"
              >
                −
              </button>
              <span className="w-8 text-center font-medium">{cantidad}</span>
              <button
                onClick={() => setCantidad((c) => c + 1)}
                className="flex h-9 w-9 items-center justify-center rounded-lg border border-gray-300"
              >
                +
              </button>
            </div>
            <Boton
              tamano="lg"
              disabled={sinStock}
              onClick={manejarAgregar}
              className="flex-1"
            >
              Agregar al carrito
            </Boton>
          </div>
        </div>
      </div>
    </div>
  )
}
