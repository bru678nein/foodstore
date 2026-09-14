import { initMercadoPago } from "@mercadopago/sdk-react"

const CLAVE_PUBLICA = (import.meta.env.VITE_CLAVE_PUBLICA_MP as string | undefined) ?? ""

let inicializado = false

export function inicializarMP(): void {
  if (inicializado || !CLAVE_PUBLICA) return
  inicializado = true
  initMercadoPago(CLAVE_PUBLICA, { locale: "es-AR" })
}

export const MP_CONFIGURADO = Boolean(CLAVE_PUBLICA)
