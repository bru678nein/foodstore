interface PropsSpinner {
  className?: string
  texto?: string
}

export function Spinner({ className = "", texto }: PropsSpinner) {
  return (
    <div className={`flex flex-col items-center justify-center gap-3 py-10 ${className}`}>
      <span className="h-8 w-8 animate-spin rounded-full border-4 border-primario-100 border-t-primario-500" />
      {texto && <p className="text-sm text-gray-500">{texto}</p>}
    </div>
  )
}
