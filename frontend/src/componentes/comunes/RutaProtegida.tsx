import { Navigate, Outlet } from "react-router-dom"
import { sesionStore } from "@/almacenes/sesionStore"

interface PropsRutaProtegida {
  perfilesRequeridos?: string[]
}

export function RutaProtegida({ perfilesRequeridos }: PropsRutaProtegida) {
  const estaAutenticado = sesionStore((s) => s.estaAutenticado)
  const tokenAcceso = sesionStore((s) => s.tokenAcceso)
  const cuenta = sesionStore((s) => s.cuenta)

  if (!estaAutenticado || !tokenAcceso) {
    return <Navigate to="/ingresar" replace />
  }

  if (perfilesRequeridos && perfilesRequeridos.length > 0) {
    const tieneAlguno = perfilesRequeridos.some((p) =>
      cuenta?.perfiles.includes(p),
    )
    if (!tieneAlguno) {
      return <Navigate to="/" replace />
    }
  }

  return <Outlet />
}
