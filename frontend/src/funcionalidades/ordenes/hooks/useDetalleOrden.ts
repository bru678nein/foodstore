import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { cancelarOrden, obtenerOrden } from "@/api/endpoints/ordenes"
import { clavesConsulta } from "@/lib/clavesConsulta"
import type { RespuestaOrden } from "@/tipos/ordenes"

export function useDetalleOrden(id: number) {
  return useQuery({
    queryKey: clavesConsulta.ordenes.detalle(id),
    queryFn: () => obtenerOrden(id),
    enabled: Number.isFinite(id) && id > 0,
  })
}

export function useCancelarOrden(id: number) {
  const cliente = useQueryClient()
  const claveDetalle = clavesConsulta.ordenes.detalle(id)

  return useMutation({
    mutationFn: () => cancelarOrden(id),

        onMutate: async () => {
      await cliente.cancelQueries({ queryKey: claveDetalle })
      const anterior = cliente.getQueryData<RespuestaOrden>(claveDetalle)
      if (anterior) {
        cliente.setQueryData<RespuestaOrden>(claveDetalle, {
          ...anterior,
          estado_actual: "CANCELADO",
        })
      }
      return { anterior }
    },

        onError: (_err, _vars, ctx) => {
      if (ctx?.anterior) {
        cliente.setQueryData(claveDetalle, ctx.anterior)
      }
    },

    onSuccess: (orden) => {
      cliente.setQueryData(claveDetalle, orden)
      cliente.invalidateQueries({ queryKey: clavesConsulta.ordenes.misOrdenes() })
    },
  })
}
