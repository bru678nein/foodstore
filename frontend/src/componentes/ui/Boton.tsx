import type { ButtonHTMLAttributes, ReactNode } from "react"

type Variante = "primario" | "secundario" | "contorno" | "peligro" | "fantasma"
type Tamano = "sm" | "md" | "lg"

interface PropsBoton extends ButtonHTMLAttributes<HTMLButtonElement> {
  variante?: Variante
  tamano?: Tamano
  cargando?: boolean
  children: ReactNode
}

const estilosVariante: Record<Variante, string> = {
  primario:
    "bg-primario-500 text-white hover:bg-primario-600 focus:ring-primario-400 active:scale-95 shadow-sm",
  secundario:
    "bg-secundario-500 text-white hover:bg-secundario-600 focus:ring-secundario-500 active:scale-95 shadow-sm",
  contorno:
    "border-2 border-primario-300 bg-white text-primario-600 hover:bg-primario-50 focus:ring-primario-300",
  peligro:
    "bg-error text-white hover:bg-red-600 focus:ring-error active:scale-95 shadow-sm",
  fantasma:
    "bg-transparent text-gray-600 hover:bg-crema-200 focus:ring-gray-300",
}

const estilosTamano: Record<Tamano, string> = {
  sm: "px-3 py-1.5 text-sm rounded-lg",
  md: "px-5 py-2.5 text-sm rounded-xl",
  lg: "px-7 py-3 text-base rounded-xl",
}

export function Boton({
  variante = "primario",
  tamano = "md",
  cargando = false,
  disabled,
  className = "",
  children,
  ...resto
}: PropsBoton) {
  return (
    <button
      disabled={disabled || cargando}
      className={`inline-flex items-center justify-center gap-2 font-bold transition-all focus:outline-none focus:ring-2 focus:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-60 ${estilosVariante[variante]} ${estilosTamano[tamano]} ${className}`}
      {...resto}
    >
      {cargando && (
        <span className="h-4 w-4 animate-spin rounded-full border-2 border-white/40 border-t-white" />
      )}
      {children}
    </button>
  )
}
