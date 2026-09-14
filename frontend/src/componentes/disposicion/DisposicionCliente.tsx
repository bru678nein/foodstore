import { useEffect } from "react"
import { Outlet } from "react-router-dom"
import { useQueryClient } from "@tanstack/react-query"
import { BarraNavegacion } from "./BarraNavegacion"
import { Toasts } from "@/componentes/ui/Toasts"
import { CajonCarrito } from "@/funcionalidades/carrito/CajonCarrito"
import { sesionStore } from "@/almacenes/sesionStore"

const _WS_BASE = (import.meta.env.VITE_URL_WS as string | undefined) ?? "ws://localhost:8000"
export const URL_WS_BASE = _WS_BASE.replace(/\/ws\/?$/, "")

const EVENTOS_STOCK = new Set(["orden_creada", "orden_cancelada", "orden_actualizada", "articulo_actualizado"])

export function useStockWS() {
  const cliente = useQueryClient()
  const token = sesionStore((s) => s.tokenAcceso)

  useEffect(() => {
    if (!token) return
    let ws: WebSocket | null = null
    let timerId: ReturnType<typeof setTimeout> | null = null
    let activo = true

    const conectar = () => {
      if (!activo) return
      ws = new WebSocket(`${URL_WS_BASE}/ws/ordenes?token=${token}`)

      ws.onmessage = (msg) => {
        try {
          const datos = JSON.parse(msg.data as string) as { evento: string }
          if (EVENTOS_STOCK.has(datos.evento)) {
            void cliente.invalidateQueries({
              predicate: (query) => {
                const k = query.queryKey[0]
                return k === "articulos" || k === "componentes"
              },
            })
          }
        } catch {}
      }

      ws.onclose = () => {
        if (activo) timerId = setTimeout(conectar, 3000)
      }

      ws.onerror = () => { ws?.close() }
    }

    conectar()

    return () => {
      activo = false
      if (timerId) clearTimeout(timerId)
      if (ws) { ws.onclose = null; ws.close() }
    }
  }, [token, cliente])
}

export function DisposicionCliente() {
  useStockWS()
  return (
    <div className="flex min-h-full flex-col">
      <BarraNavegacion />
      <main className="contenedor-pagina flex-1 py-8">
        <Outlet />
      </main>
      <footer className="border-t border-crema-200 bg-crema-50 py-6">
        <div className="contenedor-pagina text-center text-sm font-semibold text-gray-400">
          FoodStore · Comida rica a domicilio
        </div>
      </footer>
      <Toasts />
      <CajonCarrito />
    </div>
  )
}
