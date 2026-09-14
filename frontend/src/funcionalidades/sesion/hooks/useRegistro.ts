import { useMutation } from "@tanstack/react-query"
import { useNavigate } from "react-router-dom"
import { registrar } from "@/api/endpoints/sesion"
import { sesionStore } from "@/almacenes/sesionStore"
import type { DatosRegistro } from "@/tipos/sesion"

export function useRegistro(rutaDestino = "/") {
  const navigate = useNavigate()
  const establecerSesion = sesionStore((s) => s.establecerSesion)

  return useMutation({
    mutationFn: (datos: DatosRegistro) => registrar(datos),
    onSuccess: (data) => {
      establecerSesion(data.cuenta, data.token_acceso, data.token_renovacion)
      navigate(rutaDestino, { replace: true })
    },
  })
}
