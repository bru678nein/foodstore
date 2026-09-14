import type { ReactNode } from "react"
import { sesionStore } from "@/almacenes/sesionStore"

interface PropsGuardiaRol {
  perfiles: string[]
  children: ReactNode
  fallback?: ReactNode
}

export function GuardiaRol({
  perfiles,
  children,
  fallback = null,
}: PropsGuardiaRol) {
  const cuenta = sesionStore((s) => s.cuenta)
  const tieneAlguno = perfiles.some((p) => cuenta?.perfiles.includes(p))
  return <>{tieneAlguno ? children : fallback}</>
}
