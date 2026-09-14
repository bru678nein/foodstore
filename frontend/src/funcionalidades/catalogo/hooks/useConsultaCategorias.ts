import { useQuery } from "@tanstack/react-query"
import { listarCategorias } from "@/api/endpoints/catalogo"
import { clavesConsulta } from "@/lib/clavesConsulta"

export function useConsultaCategorias() {
  return useQuery({
    queryKey: clavesConsulta.categorias.lista(),
    queryFn: listarCategorias,
    staleTime: 1000 * 60 * 30,
  })
}
