import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import {
  asignarPerfilCuenta,
  cambiarEstadoCuenta,
  eliminarCuenta,
  listarCuentas,
} from "@/api/endpoints/cuentas"
import { clavesConsulta } from "@/lib/clavesConsulta"

export function useAdminCuentas() {
  const cliente = useQueryClient()
  const clave = clavesConsulta.admin.cuentas()
  const invalidar = () => cliente.invalidateQueries({ queryKey: clave })

  const consulta = useQuery({ queryKey: clave, queryFn: listarCuentas })

  const cambiarEstado = useMutation({
    mutationFn: ({ id, habilitado }: { id: number; habilitado: boolean }) =>
      cambiarEstadoCuenta(id, habilitado),
    onSuccess: invalidar,
  })

  const asignarPerfil = useMutation({
    mutationFn: ({ id, perfil }: { id: number; perfil: string }) =>
      asignarPerfilCuenta(id, perfil),
    onSuccess: invalidar,
  })

  const eliminar = useMutation({
    mutationFn: (id: number) => eliminarCuenta(id),
    onSuccess: invalidar,
  })

  return { consulta, cambiarEstado, asignarPerfil, eliminar }
}
