import axios, {
  AxiosError,
  type AxiosRequestConfig,
  type InternalAxiosRequestConfig,
} from "axios"
import { sesionStore } from "@/almacenes/sesionStore"
import type { RespuestaRenovar } from "@/tipos/sesion"

const HOST =
  import.meta.env.VITE_URL_API || "http://localhost:8000"
const PREFIJO_API = "/api/v1"

export const clienteHttp = axios.create({
  baseURL: HOST,
  headers: { "Content-Type": "application/json" },
})

clienteHttp.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    if (config.url && !config.url.startsWith("http") && !config.url.startsWith(PREFIJO_API)) {
      config.url = PREFIJO_API + config.url
    }
    const token = sesionStore.getState().tokenAcceso
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error),
)

interface ConfigReintentable extends AxiosRequestConfig {
  _reintentado?: boolean
}

let renovacionEnCurso: Promise<string | null> | null = null

async function renovarToken(): Promise<string | null> {
  const { tokenRenovacion } = sesionStore.getState()
  if (!tokenRenovacion) return null
  try {
    const { data } = await axios.post<RespuestaRenovar>(
      `${HOST}${PREFIJO_API}/sesion/renovar`,
      { token_renovacion: tokenRenovacion },
    )
    sesionStore.getState().actualizarToken(data.token_acceso)
    if (data.token_renovacion) {
      const cuenta = sesionStore.getState().cuenta
      if (cuenta) {
        sesionStore
          .getState()
          .establecerSesion(cuenta, data.token_acceso, data.token_renovacion)
      }
    }
    return data.token_acceso
  } catch {
    return null
  }
}

function redirigirAIngreso() {
  sesionStore.getState().cerrarSesion()
  if (typeof window !== "undefined" && window.location.pathname !== "/ingresar") {
    window.location.assign("/ingresar")
  }
}

clienteHttp.interceptors.response.use(
  (respuesta) => respuesta,
  async (error: AxiosError) => {
    const original = error.config as ConfigReintentable | undefined
    const esRenovacion = original?.url?.includes("/sesion/renovar")

    if (
      error.response?.status === 401 &&
      original &&
      !original._reintentado &&
      !esRenovacion
    ) {
      original._reintentado = true

      if (!renovacionEnCurso) {
        renovacionEnCurso = renovarToken().finally(() => {
          renovacionEnCurso = null
        })
      }

      const nuevoToken = await renovacionEnCurso

      if (nuevoToken) {
        original.headers = {
          ...original.headers,
          Authorization: `Bearer ${nuevoToken}`,
        }
        return clienteHttp(original)
      }

      redirigirAIngreso()
    }

    return Promise.reject(error)
  },
)

export function extraerMensajeError(error: unknown, porDefecto = "Ocurrió un error"): string {
  if (axios.isAxiosError(error)) {
    const data = error.response?.data as
      | { detalle?: string; mensaje?: string; detail?: string | unknown[] }
      | undefined
    const detail = data?.detail
    if (Array.isArray(detail)) {
      const primero = detail[0] as { msg?: string } | undefined
      return primero?.msg ?? porDefecto
    }
    return (
      (data?.detalle as string | undefined) ??
      (data?.mensaje as string | undefined) ??
      (typeof detail === "string" ? detail : undefined) ??
      error.message ??
      porDefecto
    )
  }
  if (error instanceof Error) return error.message
  return porDefecto
}
