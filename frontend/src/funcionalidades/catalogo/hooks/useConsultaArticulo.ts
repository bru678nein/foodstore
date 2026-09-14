import { useQuery } from "@tanstack/react-query"
import { obtenerArticulo } from "@/api/endpoints/catalogo"
import { clavesConsulta } from "@/lib/clavesConsulta"

export function useConsultaArticulo(id: number) {
  return useQuery({
    queryKey: clavesConsulta.articulos.detalle(id),
    queryFn: () => obtenerArticulo(id),
    enabled: Number.isFinite(id) && id > 0,
  })
}
