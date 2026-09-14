import { useEffect } from "react"
import { conexionStore } from "@/almacenes/conexionStore"

export function useConexionWS(canal: string | null) {
  const conectar = conexionStore((s) => s.conectar)
  const desconectar = conexionStore((s) => s.desconectar)
  const ultimoEvento = conexionStore((s) => s.ultimoEvento)
  const estaConectado = conexionStore((s) => s.estaConectado)

  useEffect(() => {
    if (!canal) return
    conectar(canal)
    return () => desconectar()
  }, [canal, conectar, desconectar])

  return { ultimoEvento, estaConectado }
}
