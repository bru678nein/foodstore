import { clienteHttp } from "../clienteHttp"
import type { Domicilio, EntradaDomicilio } from "@/tipos/ordenes"

export async function listarDomicilios(): Promise<Domicilio[]> {
  const { data } = await clienteHttp.get<Domicilio[]>("/domicilios")
  return data
}

export async function crearDomicilio(
  entrada: EntradaDomicilio,
): Promise<Domicilio> {
  const { data } = await clienteHttp.post<Domicilio>("/domicilios", entrada)
  return data
}

export async function actualizarDomicilio(
  id: number,
  entrada: EntradaDomicilio,
): Promise<Domicilio> {
  const { data } = await clienteHttp.put<Domicilio>(
    `/domicilios/${id}`,
    entrada,
  )
  return data
}

export async function eliminarDomicilio(id: number): Promise<void> {
  await clienteHttp.delete(`/domicilios/${id}`)
}

export async function marcarPredeterminado(id: number): Promise<Domicilio> {
  const { data } = await clienteHttp.patch<Domicilio>(
    `/domicilios/${id}/predeterminado`,
  )
  return data
}
