import { clienteHttp } from "../clienteHttp"
import type { CuentaAdmin } from "@/tipos/admin"

export async function listarCuentas(): Promise<CuentaAdmin[]> {
  const { data } = await clienteHttp.get<CuentaAdmin[]>("/cuentas")
  return data
}

export async function cambiarEstadoCuenta(
  id: number,
  habilitado: boolean,
): Promise<CuentaAdmin> {
  const { data } = await clienteHttp.patch<CuentaAdmin>(
    `/cuentas/${id}/estado`,
    { habilitado },
  )
  return data
}

export async function asignarPerfilCuenta(
  id: number,
  perfil: string,
): Promise<CuentaAdmin> {
  const { data } = await clienteHttp.patch<CuentaAdmin>(
    `/cuentas/${id}/perfil`,
    { perfil },
  )
  return data
}

export async function eliminarCuenta(id: number): Promise<void> {
  await clienteHttp.delete(`/cuentas/${id}`)
}
