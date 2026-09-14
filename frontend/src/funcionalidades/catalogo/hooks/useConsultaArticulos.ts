import { useQuery } from "@tanstack/react-query"
import { listarArticulos } from "@/api/endpoints/catalogo"
import { clavesConsulta } from "@/lib/clavesConsulta"
import type { ParametrosArticulos } from "@/tipos/catalogo"

export function useConsultaArticulos(params: ParametrosArticulos) {
  return useQuery({
    queryKey: clavesConsulta.articulos.lista(params),
    queryFn: () => listarArticulos(params),
    placeholderData: (anterior) => anterior,
    staleTime: 0,
    refetchOnMount: "always",
    refetchOnWindowFocus: "always",
    refetchInterval: 10_000,
  })
}
