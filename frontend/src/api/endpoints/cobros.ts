import { clienteHttp } from "../clienteHttp"
import type { EntradaPagoDirecto, EstadoCobro, PreferenciaCobro, SalidaPagoDirecto } from "@/tipos/cobros"

export async function crearPreferencia(
  ordenId: number,
): Promise<PreferenciaCobro> {
  const { data } = await clienteHttp.post<PreferenciaCobro>(
    "/cobros/preferencia",
    { orden_id: ordenId },
  )
  return data
}

export async function pagarConTarjetaMP(
  entrada: EntradaPagoDirecto,
): Promise<SalidaPagoDirecto> {
  const { data } = await clienteHttp.post<SalidaPagoDirecto>(
    "/cobros/pago-directo",
    entrada,
  )
  return data
}

export async function obtenerEstadoCobro(
  ordenId: number,
): Promise<EstadoCobro> {
  const { data } = await clienteHttp.get<EstadoCobro>(`/cobros/${ordenId}`)
  return data
}
