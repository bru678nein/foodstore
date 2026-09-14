import { create } from "zustand"

type EstadoCobro = "inactivo" | "pendiente" | "aprobado" | "rechazado"

interface EstadoPago {
  ordenId: number | null
  preferenciaId: string | null
  estadoCobro: EstadoCobro

  iniciarProceso: (ordenId: number, preferenciaId: string) => void
  actualizarEstado: (estado: EstadoCobro) => void
  reiniciar: () => void
}

export const pagoStore = create<EstadoPago>()((set) => ({
  ordenId: null,
  preferenciaId: null,
  estadoCobro: "inactivo",

  iniciarProceso: (ordenId, preferenciaId) =>
    set({ ordenId, preferenciaId, estadoCobro: "pendiente" }),

  actualizarEstado: (estadoCobro) => set({ estadoCobro }),

  reiniciar: () =>
    set({ ordenId: null, preferenciaId: null, estadoCobro: "inactivo" }),
}))
