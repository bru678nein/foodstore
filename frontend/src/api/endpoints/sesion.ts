import { clienteHttp } from "../clienteHttp"
import type {
  CredencialesIngreso,
  CuentaBasica,
  DatosRegistro,
  RespuestaToken,
} from "@/tipos/sesion"

export async function registrar(datos: DatosRegistro): Promise<RespuestaToken> {
  const { data } = await clienteHttp.post<RespuestaToken>(
    "/sesion/registrar",
    datos,
  )
  return data
}

export async function iniciarSesion(
  credenciales: CredencialesIngreso,
): Promise<RespuestaToken> {
  const { data } = await clienteHttp.post<RespuestaToken>(
    "/sesion/iniciar",
    credenciales,
  )
  return data
}

export async function cerrarSesionRemota(): Promise<void> {
  await clienteHttp.post("/sesion/cerrar")
}

export async function obtenerMiCuenta(): Promise<CuentaBasica> {
  const { data } = await clienteHttp.get<CuentaBasica>("/sesion/mi-cuenta")
  return data
}
