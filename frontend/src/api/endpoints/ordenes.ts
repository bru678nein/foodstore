import { clienteHttp } from "../clienteHttp"
import type {
  EntradaOrden,
  EstadoOrden,
  RespuestaOrden,
} from "@/tipos/ordenes"

export async function crearOrden(
  entrada: EntradaOrden,
): Promise<RespuestaOrden> {
  const { data } = await clienteHttp.post<RespuestaOrden>("/ordenes", entrada)
  return data
}

export async function listarMisOrdenes(): Promise<RespuestaOrden[]> {
  const { data } = await clienteHttp.get<RespuestaOrden[]>(
    "/ordenes/mis-ordenes",
  )
  return data
}

export async function obtenerOrden(id: number): Promise<RespuestaOrden> {
  const { data } = await clienteHttp.get<RespuestaOrden>(`/ordenes/${id}`)
  return data
}

export async function listarTodasLasOrdenes(): Promise<RespuestaOrden[]> {
  const { data } = await clienteHttp.get<RespuestaOrden[]>("/ordenes")
  return data
}

export async function cambiarEstadoOrden(
  id: number,
  estado: EstadoOrden,
): Promise<RespuestaOrden> {
  const { data } = await clienteHttp.patch<RespuestaOrden>(
    `/ordenes/${id}/estado`,
    { estado_nuevo: estado },
  )
  return data
}

export async function cancelarOrden(id: number): Promise<RespuestaOrden> {
  const { data } = await clienteHttp.post<RespuestaOrden>(
    `/ordenes/${id}/cancelar`,
  )
  return data
}
