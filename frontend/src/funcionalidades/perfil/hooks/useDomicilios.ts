import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import {
  actualizarDomicilio,
  crearDomicilio,
  eliminarDomicilio,
  listarDomicilios,
  marcarPredeterminado,
} from "@/api/endpoints/domicilios"
import { clavesConsulta } from "@/lib/clavesConsulta"
import type { EntradaDomicilio } from "@/tipos/ordenes"

export function useDomicilios() {
  const cliente = useQueryClient()
  const clave = clavesConsulta.domicilios.lista()

  const consulta = useQuery({
    queryKey: clave,
    queryFn: listarDomicilios,
  })

  const invalidar = () => cliente.invalidateQueries({ queryKey: clave })

  const crear = useMutation({
    mutationFn: (entrada: EntradaDomicilio) => crearDomicilio(entrada),
    onSuccess: invalidar,
  })

  const actualizar = useMutation({
    mutationFn: ({ id, entrada }: { id: number; entrada: EntradaDomicilio }) =>
      actualizarDomicilio(id, entrada),
    onSuccess: invalidar,
  })

  const eliminar = useMutation({
    mutationFn: (id: number) => eliminarDomicilio(id),
    onSuccess: invalidar,
  })

  const predeterminar = useMutation({
    mutationFn: (id: number) => marcarPredeterminado(id),
    onSuccess: invalidar,
  })

  return { consulta, crear, actualizar, eliminar, predeterminar }
}
