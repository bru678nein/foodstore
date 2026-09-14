import type { ReactNode } from "react"

export function EnvolturaPrincipal({ children }: { children: ReactNode }) {
  return (
    <main className="contenedor-pagina flex-1 py-8">{children}</main>
  )
}
