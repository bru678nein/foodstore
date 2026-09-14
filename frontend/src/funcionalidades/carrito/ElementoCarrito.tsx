import { UtensilsCrossed, X } from "lucide-react"
import { formatearMoneda } from "@/lib/formato"
import { carritoStore } from "@/almacenes/carritoStore"
import type { ElementoCarrito as TipoElemento } from "@/tipos/carrito"

interface PropsElementoCarrito {
  elemento: TipoElemento
  compacto?: boolean
}

export function ElementoCarrito({
  elemento,
  compacto = false,
}: PropsElementoCarrito) {
  const cambiarCantidad = carritoStore((s) => s.cambiarCantidad)
  const quitarElemento = carritoStore((s) => s.quitarElemento)

  return (
    <div className="flex gap-3 py-3">
      <div className="h-16 w-16 shrink-0 overflow-hidden rounded-lg bg-gray-100">
        {elemento.imagenUrl ? (
          <img
            src={elemento.imagenUrl}
            alt={elemento.titulo}
            className="h-full w-full object-cover"
          />
        ) : (
          <div className="flex h-full w-full items-center justify-center text-gray-200">
            <UtensilsCrossed className="h-6 w-6" />
          </div>
        )}
      </div>

      <div className="flex flex-1 flex-col">
        <div className="flex items-start justify-between gap-2">
          <p className="text-sm font-medium text-gray-900">{elemento.titulo}</p>
          <button
            onClick={() => quitarElemento(elemento.articuloId)}
            className="text-gray-400 hover:text-error"
            aria-label="Quitar"
          >
            <X className="h-3.5 w-3.5" />
          </button>
        </div>

        {elemento.componentesAExcluir.length > 0 && (
          <p className="text-xs text-gray-400">
            Sin: {elemento.componentesAExcluir.length} ingrediente(s)
          </p>
        )}

        <div className="mt-auto flex items-center justify-between pt-1">
          <div className="flex items-center gap-1.5">
            <button
              onClick={() =>
                cambiarCantidad(elemento.articuloId, elemento.cantidad - 1)
              }
              className="flex h-7 w-7 items-center justify-center rounded-md border border-gray-200 text-gray-600 hover:bg-gray-50"
            >
              −
            </button>
            <span className="w-6 text-center text-sm font-medium">
              {elemento.cantidad}
            </span>
            <button
              onClick={() =>
                cambiarCantidad(elemento.articuloId, elemento.cantidad + 1)
              }
              className="flex h-7 w-7 items-center justify-center rounded-md border border-gray-200 text-gray-600 hover:bg-gray-50"
            >
              +
            </button>
          </div>
          <span className={`font-semibold ${compacto ? "text-sm" : ""}`}>
            {formatearMoneda(elemento.precioUnitario * elemento.cantidad)}
          </span>
        </div>
      </div>
    </div>
  )
}
