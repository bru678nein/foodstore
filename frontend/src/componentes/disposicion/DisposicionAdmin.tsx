import { Outlet } from "react-router-dom"
import { BarraNavegacion } from "./BarraNavegacion"
import { useStockWS } from "./DisposicionCliente"

export function DisposicionAdmin() {
  useStockWS()
  return (
    <div className="flex min-h-full flex-col">
      <BarraNavegacion />
      <main className="contenedor-pagina flex-1 py-8">
        <Outlet />
      </main>
    </div>
  )
}
