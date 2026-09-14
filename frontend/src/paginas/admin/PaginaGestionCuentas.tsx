import { useState } from "react"
import { Spinner } from "@/componentes/ui/Spinner"
import { TablaCuentas } from "@/funcionalidades/admin/cuentas/TablaCuentas"
import { useAdminCuentas } from "@/funcionalidades/admin/cuentas/hooks/useAdminCuentas"
import type { CuentaAdmin } from "@/tipos/admin"

export function PaginaGestionCuentas() {
  const { consulta, cambiarEstado, asignarPerfil, eliminar } = useAdminCuentas()
  const [idCargandoEstado, setIdCargandoEstado] = useState<number | null>(null)
  const [idCargandoPerfil, setIdCargandoPerfil] = useState<number | null>(null)

  const alternarEstado = (cuenta: CuentaAdmin) => {
    setIdCargandoEstado(cuenta.id)
    cambiarEstado.mutate(
      { id: cuenta.id, habilitado: !cuenta.habilitado },
      { onSettled: () => setIdCargandoEstado(null) },
    )
  }

  const manejarAsignarPerfil = (id: number, perfil: string) => {
    setIdCargandoPerfil(id)
    asignarPerfil.mutate(
      { id, perfil },
      { onSettled: () => setIdCargandoPerfil(null) },
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Gestión de cuentas</h1>
        {consulta.data && (
          <span className="text-sm text-gray-500">
            {consulta.data.length}{" "}
            {consulta.data.length === 1 ? "cuenta" : "cuentas"}
          </span>
        )}
      </div>

      {consulta.isLoading ? (
        <Spinner />
      ) : (
        <TablaCuentas
          cuentas={consulta.data ?? []}
          alAlternarEstado={alternarEstado}
          alAsignarPerfil={manejarAsignarPerfil}
          alEliminar={(id) => eliminar.mutate(id)}
          cargandoEstado={idCargandoEstado}
          cargandoPerfil={idCargandoPerfil}
        />
      )}
    </div>
  )
}
