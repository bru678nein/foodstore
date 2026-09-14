import { create } from "zustand"

interface Toast {
  id: number
  mensaje: string
}

interface EstadoToast {
  toasts: Toast[]
  agregar: (mensaje: string) => void
  quitar: (id: number) => void
}

let contador = 0

export const toastStore = create<EstadoToast>()((set) => ({
  toasts: [],

  agregar: (mensaje) => {
    const id = ++contador
    set((s) => ({ toasts: [...s.toasts, { id, mensaje }] }))
    setTimeout(() => {
      set((s) => ({ toasts: s.toasts.filter((t) => t.id !== id) }))
    }, 3000)
  },

  quitar: (id) => set((s) => ({ toasts: s.toasts.filter((t) => t.id !== id) })),
}))
