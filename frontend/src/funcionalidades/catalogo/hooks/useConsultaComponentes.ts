import { useQuery } from "@tanstack/react-query"
import { listarComponentes } from "@/api/endpoints/catalogo"
import { clavesConsulta } from "@/lib/clavesConsulta"

export function useConsultaComponentes() {
  return useQuery({
    queryKey: clavesConsulta.componentes.lista(),
    queryFn: listarComponentes,
    staleTime: 1000 * 60 * 30,
  })
}
