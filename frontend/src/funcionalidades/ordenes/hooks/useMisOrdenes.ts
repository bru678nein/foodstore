import { useQuery } from "@tanstack/react-query"
import { listarMisOrdenes } from "@/api/endpoints/ordenes"
import { clavesConsulta } from "@/lib/clavesConsulta"

export function useMisOrdenes() {
  return useQuery({
    queryKey: clavesConsulta.ordenes.misOrdenes(),
    queryFn: listarMisOrdenes,
  })
}
