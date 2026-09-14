import { create } from "zustand"
import type { EventoWS } from "@/tipos/ws"
import { sesionStore } from "./sesionStore"

const _WS_BASE = (import.meta.env.VITE_URL_WS as string | undefined) ?? "ws://localhost:8000"
const URL_WS = _WS_BASE.replace(/\/ws\/?$/, "")
const MAX_INTENTOS = 8
const DEMORA_BASE_MS = 1000
const DEMORA_MAX_MS = 30_000

function calcularDemora(intento: number): number {
  const exponencial = DEMORA_BASE_MS * 2 ** intento
  const tope = Math.min(exponencial, DEMORA_MAX_MS)
  const jitter = tope * 0.25 * (Math.random() * 2 - 1)
  return Math.round(tope + jitter)
}

interface EstadoConexion {
  socket: WebSocket | null
  estaConectado: boolean
  ultimoEvento: EventoWS | null
  intentosReconexion: number
  canalActual: string | null
  _timerId: ReturnType<typeof setTimeout> | null

  conectar: (canal: string) => void
  desconectar: () => void
  registrarEvento: (evento: EventoWS) => void
}

export const conexionStore = create<EstadoConexion>()((set, get) => ({
  socket: null,
  estaConectado: false,
  ultimoEvento: null,
  intentosReconexion: 0,
  canalActual: null,
  _timerId: null,

  conectar: (canal) => {
    const { socket, canalActual } = get()

        if (
      socket &&
      canalActual === canal &&
      (socket.readyState === WebSocket.OPEN ||
        socket.readyState === WebSocket.CONNECTING)
    ) {
      return
    }

        if (socket) {
      socket.onclose = null
      socket.onerror = null
      socket.close()
    }

    const token = sesionStore.getState().tokenAcceso
    const url = `${URL_WS}/ws/${canal}${token ? `?token=${token}` : ""}`
    const ws = new WebSocket(url)

    ws.onopen = () => {
      set({ estaConectado: true, intentosReconexion: 0 })
    }

    ws.onmessage = (mensaje) => {
      try {
        const datos = JSON.parse(mensaje.data) as EventoWS
        set({ ultimoEvento: datos })
      } catch {
        set({
          ultimoEvento: {
            evento: "mensaje_crudo",
            datos: { raw: String(mensaje.data) },
            timestamp: new Date().toISOString(),
          },
        })
      }
    }

    ws.onerror = () => {
      ws.close()
    }

    ws.onclose = () => {
      set({ estaConectado: false, socket: null })

      const { intentosReconexion, canalActual: canalVigente } = get()

            if (canalVigente !== canal) return
      if (intentosReconexion >= MAX_INTENTOS) return

      const demora = calcularDemora(intentosReconexion)
      const timerId = setTimeout(() => {
        if (get().canalActual === canal) get().conectar(canal)
      }, demora)

      set({
        intentosReconexion: intentosReconexion + 1,
        _timerId: timerId,
      })
    }

    set({ socket: ws, canalActual: canal })
  },

  desconectar: () => {
    const { socket, _timerId } = get()

        if (_timerId !== null) clearTimeout(_timerId)

        set({ canalActual: null, _timerId: null })

    if (socket) {
      socket.onclose = null
      socket.onerror = null
      socket.close()
    }

    set({ socket: null, estaConectado: false, intentosReconexion: 0 })
  },

  registrarEvento: (evento) => set({ ultimoEvento: evento }),
}))

if (typeof document !== "undefined") {
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState !== "visible") return
    const { socket, canalActual, estaConectado, conectar } =
      conexionStore.getState()
    const muerto =
      !socket ||
      socket.readyState === WebSocket.CLOSED ||
      socket.readyState === WebSocket.CLOSING
    if (canalActual && !estaConectado && muerto) {
      conexionStore.setState({ intentosReconexion: 0 })
      conectar(canalActual)
    }
  })
}
