import { carritoStore } from "@/almacenes/carritoStore"

export function useAccionesCarrito() {
  const elementos = carritoStore((s) => s.elementos)
  const agregarElemento = carritoStore((s) => s.agregarElemento)
  const quitarElemento = carritoStore((s) => s.quitarElemento)
  const cambiarCantidad = carritoStore((s) => s.cambiarCantidad)
  const vaciarCarrito = carritoStore((s) => s.vaciarCarrito)
  const total = carritoStore((s) =>
    s.elementos.reduce((t, e) => t + e.precioUnitario * e.cantidad, 0),
  )
  const cantidadTotal = carritoStore((s) =>
    s.elementos.reduce((t, e) => t + e.cantidad, 0),
  )

  return {
    elementos,
    agregarElemento,
    quitarElemento,
    cambiarCantidad,
    vaciarCarrito,
    total,
    cantidadTotal,
  }
}
