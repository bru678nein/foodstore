import { useEffect, useState } from "react"

export function useDebounce<T>(valor: T, retraso = 400): T {
  const [valorDebounced, setValorDebounced] = useState(valor)

  useEffect(() => {
    const temporizador = setTimeout(() => setValorDebounced(valor), retraso)
    return () => clearTimeout(temporizador)
  }, [valor, retraso])

  return valorDebounced
}
