import { forwardRef, type InputHTMLAttributes } from "react"

interface PropsCampo extends InputHTMLAttributes<HTMLInputElement> {
  etiqueta?: string
  error?: string
}

export const CampoTexto = forwardRef<HTMLInputElement, PropsCampo>(
  function CampoTexto({ etiqueta, error, className = "", id, ...resto }, ref) {
    const idCampo = id || resto.name
    return (
      <div className="w-full">
        {etiqueta && (
          <label
            htmlFor={idCampo}
            className="mb-1.5 block text-sm font-bold text-gray-700"
          >
            {etiqueta}
          </label>
        )}
        <input
          ref={ref}
          id={idCampo}
          className={`w-full rounded-xl border px-3.5 py-2.5 text-sm shadow-sm transition focus:outline-none focus:ring-2 ${
            error
              ? "border-error bg-red-50 focus:ring-error"
              : "border-crema-300 bg-crema-50 focus:border-primario-400 focus:ring-primario-300"
          } ${className}`}
          {...resto}
        />
        {error && <p className="mt-1 text-xs font-semibold text-error">{error}</p>}
      </div>
    )
  },
)
