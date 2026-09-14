import { useMutation } from "@tanstack/react-query"
import { useNavigate } from "react-router-dom"
import { iniciarSesion } from "@/api/endpoints/sesion"
import { sesionStore } from "@/almacenes/sesionStore"
import { extraerMensajeError } from "@/api/clienteHttp"
import type { CredencialesIngreso } from "@/tipos/sesion"

export function useIngreso(rutaDestino = "/") {
  const navigate = useNavigate()
  const establecerSesion = sesionStore((s) => s.establecerSesion)

  return useMutation({
    mutationFn: (credenciales: CredencialesIngreso) =>
      iniciarSesion(credenciales),
    onSuccess: (data) => {
      establecerSesion(data.cuenta, data.token_acceso, data.token_renovacion)
      navigate(rutaDestino, { replace: true })
    },
    meta: { mensajeError: "No se pudo iniciar sesión" },
    onError: (error) => {
      console.error(extraerMensajeError(error))
    },
  })
}
