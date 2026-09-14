import { create } from "zustand"
import { persist } from "zustand/middleware"
import type { CuentaBasica } from "@/tipos/sesion"

interface EstadoSesion {
  cuenta: CuentaBasica | null
  tokenAcceso: string | null
  tokenRenovacion: string | null
  estaAutenticado: boolean

  establecerSesion: (
    cuenta: CuentaBasica,
    tokenAcceso: string,
    tokenRenovacion: string,
  ) => void
  actualizarToken: (nuevoToken: string) => void
  cerrarSesion: () => void
  tienePerfil: (perfil: string) => boolean
}

export const sesionStore = create<EstadoSesion>()(
  persist(
    (set, get) => ({
      cuenta: null,
      tokenAcceso: null,
      tokenRenovacion: null,
      estaAutenticado: false,

      establecerSesion: (cuenta, tokenAcceso, tokenRenovacion) =>
        set({
          cuenta,
          tokenAcceso,
          tokenRenovacion,
          estaAutenticado: true,
        }),

      actualizarToken: (nuevoToken) => set({ tokenAcceso: nuevoToken }),

      cerrarSesion: () =>
        set({
          cuenta: null,
          tokenAcceso: null,
          tokenRenovacion: null,
          estaAutenticado: false,
        }),

      tienePerfil: (perfil) => get().cuenta?.perfiles.includes(perfil) ?? false,
    }),
    {
      name: "fs-sesion",
      partialize: (estado) => ({
        cuenta: estado.cuenta,
        tokenAcceso: estado.tokenAcceso,
        tokenRenovacion: estado.tokenRenovacion,
        estaAutenticado: estado.estaAutenticado,
      }),
    },
  ),
)
