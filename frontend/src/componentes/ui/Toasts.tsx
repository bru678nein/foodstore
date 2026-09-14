import { toastStore } from "@/almacenes/toastStore"

export function Toasts() {
  const toasts = toastStore((s) => s.toasts)
  const quitar = toastStore((s) => s.quitar)

  if (toasts.length === 0) return null

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col gap-2">
      {toasts.map((t) => (
        <div
          key={t.id}
          className="flex items-center gap-3 rounded-xl bg-green-600 px-4 py-3 text-sm font-medium text-white shadow-lg"
        >
          <span>{t.mensaje}</span>
          <button
            onClick={() => quitar(t.id)}
            className="ml-1 text-white/70 hover:text-white"
            aria-label="Cerrar"
          >
            ✕
          </button>
        </div>
      ))}
    </div>
  )
}
