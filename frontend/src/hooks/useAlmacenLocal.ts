import { useCallback, useEffect, useState } from "react"

export function useAlmacenLocal<T>(
  clave: string,
  valorInicial: T,
): [T, (valor: T | ((prev: T) => T)) => void] {
  const [valor, setValor] = useState<T>(() => {
    try {
      const crudo = window.localStorage.getItem(clave)
      return crudo ? (JSON.parse(crudo) as T) : valorInicial
    } catch {
      return valorInicial
    }
  })

  useEffect(() => {
    try {
      window.localStorage.setItem(clave, JSON.stringify(valor))
    } catch {
          }
  }, [clave, valor])

  const actualizar = useCallback(
    (nuevo: T | ((prev: T) => T)) => setValor(nuevo),
    [],
  )

  return [valor, actualizar]
}
