import { Link } from "react-router-dom"
import { UtensilsCrossed } from "lucide-react"
import { FormularioIngreso } from "@/funcionalidades/sesion/FormularioIngreso"

export function PaginaIngreso() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-crema-200 via-crema-100 to-primario-50 px-4">
      
      <div className="pointer-events-none fixed -left-20 -top-20 h-72 w-72 rounded-full bg-primario-100/60 blur-3xl" />
      <div className="pointer-events-none fixed -bottom-20 -right-20 h-80 w-80 rounded-full bg-calido-200/40 blur-3xl" />

      <div className="relative w-full max-w-md">
        
        <Link to="/" className="mb-8 flex items-center justify-center gap-3">
          <span className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primario-500 text-white shadow-md">
            <UtensilsCrossed className="h-6 w-6" />
          </span>
          <span className="text-3xl font-extrabold text-gray-900">
            Food<span className="text-primario-500">Store</span>
          </span>
        </Link>

        
        <div className="rounded-3xl border border-crema-200 bg-white p-8 shadow-tarjeta-hover">
          <h1 className="mb-1 text-center text-2xl font-extrabold text-gray-900">
            ¡Bienvenido de vuelta!
          </h1>
          <p className="mb-6 text-center text-sm text-gray-500 font-semibold">
            Ingresá para hacer tu pedido
          </p>
          <FormularioIngreso />
        </div>
      </div>
    </div>
  )
}
