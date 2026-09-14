import { useNavigate } from "react-router-dom"
import { ShoppingCart } from "lucide-react"
import { Boton } from "@/componentes/ui/Boton"
import { ElementoCarrito } from "@/funcionalidades/carrito/ElementoCarrito"
import { ResumenCarrito } from "@/funcionalidades/carrito/ResumenCarrito"
import { useAccionesCarrito } from "@/funcionalidades/carrito/hooks/useAccionesCarrito"
import { sesionStore } from "@/almacenes/sesionStore"

export function PaginaCarrito() {
  const navigate = useNavigate()
  const { elementos, total, cantidadTotal, vaciarCarrito } =
    useAccionesCarrito()
  const estaAutenticado = sesionStore((s) => s.estaAutenticado)

  const procederAlPago = () => {
    navigate(estaAutenticado ? "/pago" : "/ingresar")
  }

  if (elementos.length === 0) {
    return (
      <div className="flex flex-col items-center gap-3 py-20 text-center">
        <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-crema-100 text-primario-300">
          <ShoppingCart className="h-8 w-8" />
        </div>
        <h1 className="text-xl font-bold text-gray-700">Tu carrito está vacío</h1>
        <p className="text-gray-500">Agregá algunos productos del catálogo.</p>
        <Boton onClick={() => navigate("/")}>Ver catálogo</Boton>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Tu carrito</h1>
      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-2">
          <div className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
            <div className="divide-y divide-gray-100">
              {elementos.map((e) => (
                <ElementoCarrito key={e.articuloId} elemento={e} />
              ))}
            </div>
            <button
              onClick={vaciarCarrito}
              className="mt-4 text-sm text-gray-400 hover:text-error"
            >
              Vaciar carrito
            </button>
          </div>
        </div>
        <div>
          <ResumenCarrito total={total} cantidad={cantidadTotal}>
            <Boton className="w-full" onClick={procederAlPago}>
              Proceder al pago
            </Boton>
          </ResumenCarrito>
        </div>
      </div>
    </div>
  )
}
