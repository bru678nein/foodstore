import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import {
  actualizarArticulo,
  actualizarExistencias,
  crearArticulo,
  eliminarArticulo,
  listarArticulos,
} from "@/api/endpoints/catalogo"
import { clavesConsulta } from "@/lib/clavesConsulta"
import type { EntradaArticulo } from "@/tipos/catalogo"

export function useAdminArticulos() {
  const cliente = useQueryClient()
  const invalidar = () =>
    cliente.invalidateQueries({ queryKey: clavesConsulta.articulos.todos() })

  const consulta = useQuery({
    queryKey: clavesConsulta.articulos.lista({ porPagina: 100, pagina: 1 }),
    queryFn: () => listarArticulos({ porPagina: 100, pagina: 1 }),
  })

  const crear = useMutation({
    mutationFn: (entrada: EntradaArticulo) => crearArticulo(entrada),
    onSuccess: invalidar,
  })

  const actualizar = useMutation({
    mutationFn: ({ id, entrada }: { id: number; entrada: EntradaArticulo }) =>
      actualizarArticulo(id, entrada),
    onSuccess: invalidar,
  })

  const eliminar = useMutation({
    mutationFn: (id: number) => eliminarArticulo(id),
    onSuccess: invalidar,
  })

  const ajustarExistencias = useMutation({
    mutationFn: ({ id, existencias }: { id: number; existencias: number }) =>
      actualizarExistencias(id, existencias),
    onSuccess: invalidar,
  })

  return { consulta, crear, actualizar, eliminar, ajustarExistencias }
}
