import { formatearMoneda } from "@/lib/formato"

interface PropsResumenCarrito {
  total: number
  cantidad: number
  children?: React.ReactNode
}

export function ResumenCarrito({
  total,
  cantidad,
  children,
}: PropsResumenCarrito) {
  return (
    <div className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
      <h3 className="mb-4 text-lg font-semibold">Resumen del pedido</h3>
      <div className="space-y-2 text-sm">
        <div className="flex justify-between text-gray-600">
          <span>Artículos</span>
          <span>{cantidad}</span>
        </div>
        <div className="flex justify-between text-gray-600">
          <span>Subtotal</span>
          <span>{formatearMoneda(total)}</span>
        </div>
        <div className="my-2 border-t border-gray-100" />
        <div className="flex justify-between text-base font-bold">
          <span>Total</span>
          <span className="text-primario-600">{formatearMoneda(total)}</span>
        </div>
      </div>
      {children && <div className="mt-5">{children}</div>}
    </div>
  )
}
