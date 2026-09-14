import type { ReactNode } from "react"

interface PropsTarjetaKpi {
  titulo: string
  valor: string
  icono?: ReactNode
  color?: string
}

export function TarjetaKpi({
  titulo,
  valor,
  icono,
  color = "bg-primario-50 text-primario-600",
}: PropsTarjetaKpi) {
  return (
    <div className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-500">{titulo}</p>
          <p className="mt-1 text-2xl font-bold text-gray-900">{valor}</p>
        </div>
        {icono && (
          <span className={`flex h-12 w-12 items-center justify-center rounded-lg ${color}`}>
            {icono}
          </span>
        )}
      </div>
    </div>
  )
}
