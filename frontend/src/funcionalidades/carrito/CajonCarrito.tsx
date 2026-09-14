import { ShoppingCart, UtensilsCrossed, X } from "lucide-react"
import { useNavigate } from "react-router-dom"
import { carritoStore } from "@/almacenes/carritoStore"
import { Boton } from "@/componentes/ui/Boton"
import { ElementoCarrito } from "./ElementoCarrito"
import { formatearMoneda } from "@/lib/formato"

export function CajonCarrito() {
  const navigate = useNavigate()
  const estaAbierto = carritoStore((s) => s.estaAbierto)
  const elementos = carritoStore((s) => s.elementos)
  const cerrarCarrito = carritoStore((s) => s.cerrarCarrito)
  const vaciarCarrito = carritoStore((s) => s.vaciarCarrito)
  const total = carritoStore((s) =>
    s.elementos.reduce((t, e) => t + e.precioUnitario * e.cantidad, 0),
  )

  const irAlCarrito = () => {
    cerrarCarrito()
    navigate("/carrito")
  }

  return (
    <>
      
      <div
        className={`fixed inset-0 z-40 bg-black/30 backdrop-blur-sm transition-opacity ${
          estaAbierto ? "opacity-100" : "pointer-events-none opacity-0"
        }`}
        onClick={cerrarCarrito}
      />

      
      <aside
        className={`fixed right-0 top-0 z-50 flex h-full w-full max-w-md flex-col bg-white shadow-2xl transition-transform duration-300 ${
          estaAbierto ? "translate-x-0" : "translate-x-full"
        }`}
      >
        
        <div className="flex items-center justify-between border-b border-crema-200 bg-crema-50 px-6 py-4">
          <div className="flex items-center gap-2">
            <ShoppingCart className="h-5 w-5 text-primario-500" />
            <h2 className="text-lg font-extrabold text-gray-900">Tu carrito</h2>
          </div>
          <button
            onClick={cerrarCarrito}
            className="flex h-8 w-8 items-center justify-center rounded-full text-gray-400 hover:bg-crema-200 hover:text-gray-600 transition-colors"
            aria-label="Cerrar carrito"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        
        <div className="flex-1 overflow-y-auto px-5 py-2">
          {elementos.length === 0 ? (
            <div className="flex h-full flex-col items-center justify-center gap-3 text-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-crema-100 text-primario-300">
                <UtensilsCrossed className="h-8 w-8" />
              </div>
              <p className="font-bold text-gray-700">Tu carrito está vacío</p>
              <p className="text-sm font-semibold text-gray-400">
                Agregá algo rico del catálogo
              </p>
            </div>
          ) : (
            <div className="divide-y divide-crema-100">
              {elementos.map((e) => (
                <ElementoCarrito key={e.articuloId} elemento={e} compacto />
              ))}
            </div>
          )}
        </div>

        
        {elementos.length > 0 && (
          <div className="space-y-3 border-t border-crema-200 bg-crema-50 px-5 py-4">
            <div className="flex justify-between text-base font-extrabold text-gray-900">
              <span>Total</span>
              <span className="text-primario-500">{formatearMoneda(total)}</span>
            </div>
            <Boton className="w-full" tamano="lg" onClick={irAlCarrito}>
              Ir al carrito
            </Boton>
            <button
              onClick={vaciarCarrito}
              className="w-full text-center text-sm font-semibold text-gray-400 hover:text-error transition-colors"
            >
              Vaciar carrito
            </button>
          </div>
        )}
      </aside>
    </>
  )
}
