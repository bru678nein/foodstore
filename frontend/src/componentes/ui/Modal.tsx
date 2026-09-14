import { type ReactNode, useEffect } from "react"

interface PropsModal {
  abierto: boolean
  alCerrar: () => void
  titulo?: string
  children: ReactNode
  anchoMax?: string
}

export function Modal({
  abierto,
  alCerrar,
  titulo,
  children,
  anchoMax = "max-w-lg",
}: PropsModal) {
  useEffect(() => {
    if (!abierto) return
    const manejador = (e: KeyboardEvent) => {
      if (e.key === "Escape") alCerrar()
    }
    window.addEventListener("keydown", manejador)
    document.body.style.overflow = "hidden"
    return () => {
      window.removeEventListener("keydown", manejador)
      document.body.style.overflow = ""
    }
  }, [abierto, alCerrar])

  if (!abierto) return null

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4 backdrop-blur-sm"
      onClick={alCerrar}
    >
      <div
        className={`w-full ${anchoMax} max-h-[90vh] overflow-y-auto rounded-3xl bg-white shadow-2xl`}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between border-b border-crema-200 px-6 py-4">
          <h3 className="text-lg font-extrabold text-gray-900">{titulo}</h3>
          <button
            onClick={alCerrar}
            className="flex h-8 w-8 items-center justify-center rounded-full text-gray-400 hover:bg-crema-100 hover:text-gray-600 transition-colors"
            aria-label="Cerrar"
          >
            ✕
          </button>
        </div>
        <div className="px-6 py-5">{children}</div>
      </div>
    </div>
  )
}
