import { Link } from "react-router-dom"
import { FormularioPerfil } from "@/funcionalidades/perfil/FormularioPerfil"

export function PaginaPerfil() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Mi perfil</h1>
      <FormularioPerfil />
      <div className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
        <div className="flex items-center justify-between">
          <h2 className="font-semibold">Domicilios</h2>
          <Link
            to="/domicilios"
            className="text-sm font-medium text-primario-600 hover:underline"
          >
            Administrar →
          </Link>
        </div>
        <p className="mt-1 text-sm text-gray-500">
          Gestioná tus direcciones de entrega.
        </p>
      </div>
    </div>
  )
}
