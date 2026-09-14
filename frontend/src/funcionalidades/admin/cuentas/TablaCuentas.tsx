import { useState } from "react"
import { Boton } from "@/componentes/ui/Boton"
import { Insignia } from "@/componentes/ui/Insignia"
import { PERFILES_DISPONIBLES } from "@/tipos/admin"
import type { CuentaAdmin } from "@/tipos/admin"

interface Props {
  cuentas: CuentaAdmin[]
  alAlternarEstado: (cuenta: CuentaAdmin) => void
  alAsignarPerfil: (id: number, perfil: string) => void
  alEliminar: (id: number) => void
  cargandoEstado?: number | null
  cargandoPerfil?: number | null
}

const COLOR_PERFIL: Record<string, string> = {
  ADMINISTRADOR: "bg-red-100 text-red-700",
  INVENTARIO: "bg-blue-100 text-blue-700",
  DESPACHO: "bg-orange-100 text-orange-700",
  COMPRADOR: "bg-green-100 text-green-700",
}

export function TablaCuentas({
  cuentas,
  alAlternarEstado,
  alAsignarPerfil,
  alEliminar,
  cargandoEstado,
  cargandoPerfil,
}: Props) {
  const [selectorAbierto, setSelectorAbierto] = useState<number | null>(null)

  if (cuentas.length === 0) {
    return (
      <p className="rounded-lg border border-dashed border-gray-200 p-8 text-center text-sm text-gray-400">
        No hay cuentas registradas.
      </p>
    )
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-gray-100 bg-white shadow-sm">
      <table className="min-w-full divide-y divide-gray-100 text-sm">
        <thead className="bg-gray-50 text-left text-xs uppercase tracking-wide text-gray-500">
          <tr>
            <th className="px-4 py-3">Nombre</th>
            <th className="px-4 py-3">Correo</th>
            <th className="px-4 py-3">Rol actual</th>
            <th className="px-4 py-3">Estado</th>
            <th className="px-4 py-3">Acciones</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-50">
          {cuentas.map((cuenta) => (
            <tr key={cuenta.id} className="hover:bg-gray-50">
              <td className="px-4 py-3 font-medium">{cuenta.nombre_completo}</td>
              <td className="px-4 py-3 text-gray-500">{cuenta.correo}</td>

              
              <td className="px-4 py-3">
                {selectorAbierto === cuenta.id ? (
                  <div className="flex flex-wrap gap-1">
                    {PERFILES_DISPONIBLES.map((p) => (
                      <button
                        key={p}
                        disabled={cargandoPerfil === cuenta.id}
                        onClick={() => {
                          alAsignarPerfil(cuenta.id, p)
                          setSelectorAbierto(null)
                        }}
                        className={`rounded-full px-2 py-0.5 text-xs font-medium transition-opacity hover:opacity-80 ${
                          cuenta.perfiles.includes(p)
                            ? (COLOR_PERFIL[p] ?? "bg-gray-100 text-gray-700") +
                              " ring-2 ring-offset-1 ring-gray-400"
                            : (COLOR_PERFIL[p] ?? "bg-gray-100 text-gray-700") +
                              " opacity-50"
                        }`}
                      >
                        {p}
                      </button>
                    ))}
                    <button
                      onClick={() => setSelectorAbierto(null)}
                      className="ml-1 text-xs text-gray-400 hover:text-gray-600"
                    >
                      ✕
                    </button>
                  </div>
                ) : (
                  <div className="flex flex-wrap gap-1">
                    {cuenta.perfiles.length > 0 ? (
                      cuenta.perfiles.map((p) => (
                        <Insignia
                          key={p}
                          className={COLOR_PERFIL[p] ?? "bg-gray-100 text-gray-600"}
                        >
                          {p}
                        </Insignia>
                      ))
                    ) : (
                      <span className="text-xs text-gray-400">Sin rol</span>
                    )}
                    <button
                      onClick={() => setSelectorAbierto(cuenta.id)}
                      className="ml-1 rounded text-xs text-gray-400 hover:text-primario-600"
                      title="Cambiar rol"
                    >
                      ✎
                    </button>
                  </div>
                )}
              </td>

              
              <td className="px-4 py-3">
                <Insignia
                  className={
                    cuenta.habilitado
                      ? "bg-green-100 text-green-700"
                      : "bg-gray-100 text-gray-600"
                  }
                >
                  {cuenta.habilitado ? "Activo" : "Suspendido"}
                </Insignia>
              </td>

              
              <td className="px-4 py-3">
                <div className="flex gap-2">
                  <Boton
                    tamano="sm"
                    variante="contorno"
                    cargando={cargandoEstado === cuenta.id}
                    onClick={() => alAlternarEstado(cuenta)}
                  >
                    {cuenta.habilitado ? "Suspender" : "Activar"}
                  </Boton>
                  <Boton
                    tamano="sm"
                    variante="peligro"
                    onClick={() => alEliminar(cuenta.id)}
                  >
                    Eliminar
                  </Boton>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
