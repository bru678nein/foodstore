import { create } from "zustand"
import { persist } from "zustand/middleware"
import type { ElementoCarrito } from "@/tipos/carrito"
import { toastStore } from "./toastStore"

interface EstadoCarrito {
  elementos: ElementoCarrito[]
  estaAbierto: boolean

  agregarElemento: (elemento: Omit<ElementoCarrito, "cantidad">) => void
  quitarElemento: (articuloId: number) => void
  cambiarCantidad: (articuloId: number, cantidad: number) => void
  vaciarCarrito: () => void
  alternarCarrito: () => void
  cerrarCarrito: () => void
  calcularTotal: () => number
  contarElementos: () => number
}

export const carritoStore = create<EstadoCarrito>()(
  persist(
    (set, get) => ({
      elementos: [],
      estaAbierto: false,

      agregarElemento: (elemento) => {
        set((estado) => {
          const existente = estado.elementos.find(
            (e) => e.articuloId === elemento.articuloId,
          )
          if (existente) {
            return {
              elementos: estado.elementos.map((e) =>
                e.articuloId === elemento.articuloId
                  ? { ...e, cantidad: e.cantidad + 1 }
                  : e,
              ),
            }
          }
          return {
            elementos: [...estado.elementos, { ...elemento, cantidad: 1 }],
          }
        })
        toastStore.getState().agregar(`${elemento.titulo} agregado al carrito`)
      },

      quitarElemento: (articuloId) =>
        set((estado) => ({
          elementos: estado.elementos.filter(
            (e) => e.articuloId !== articuloId,
          ),
        })),

      cambiarCantidad: (articuloId, cantidad) =>
        set((estado) => ({
          elementos:
            cantidad <= 0
              ? estado.elementos.filter((e) => e.articuloId !== articuloId)
              : estado.elementos.map((e) =>
                  e.articuloId === articuloId ? { ...e, cantidad } : e,
                ),
        })),

      vaciarCarrito: () => set({ elementos: [] }),

      alternarCarrito: () =>
        set((estado) => ({ estaAbierto: !estado.estaAbierto })),

      cerrarCarrito: () => set({ estaAbierto: false }),

      calcularTotal: () =>
        get().elementos.reduce(
          (total, e) => total + e.precioUnitario * e.cantidad,
          0,
        ),

      contarElementos: () =>
        get().elementos.reduce((total, e) => total + e.cantidad, 0),
    }),
    {
      name: "fs-carrito",
      partialize: (estado) => ({ elementos: estado.elementos }),
    },
  ),
)
