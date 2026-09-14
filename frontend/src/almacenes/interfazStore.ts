import { create } from "zustand"

interface EstadoInterfaz {
  modalActivo: string | null
  estaNavAbierta: boolean

  abrirModal: (id: string) => void
  cerrarModal: () => void
  alternarNav: () => void
}

export const interfazStore = create<EstadoInterfaz>()((set) => ({
  modalActivo: null,
  estaNavAbierta: false,

  abrirModal: (id) => set({ modalActivo: id }),
  cerrarModal: () => set({ modalActivo: null }),
  alternarNav: () => set((estado) => ({ estaNavAbierta: !estado.estaNavAbierta })),
}))
