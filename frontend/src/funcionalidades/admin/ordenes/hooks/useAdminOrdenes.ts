import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import {
  cambiarEstadoOrden,
  listarTodasLasOrdenes,
} from "@/api/endpoints/ordenes"
import { clavesConsulta } from "@/lib/clavesConsulta"
import type { EstadoOrden } from "@/tipos/ordenes"

export function useAdminOrdenes() {
  const cliente = useQueryClient()

  const consulta = useQuery({
    queryKey: clavesConsulta.ordenes.todas(),
    queryFn: listarTodasLasOrdenes,
  })

  const cambiarEstado = useMutation({
    mutationFn: ({ id, estado }: { id: number; estado: EstadoOrden }) =>
      cambiarEstadoOrden(id, estado),
    onSuccess: (orden) => {
      cliente.invalidateQueries({ queryKey: clavesConsulta.ordenes.todas() })
      cliente.invalidateQueries({
        queryKey: clavesConsulta.ordenes.detalle(orden.id),
      })
    },
  })

  return { consulta, cambiarEstado }
}
