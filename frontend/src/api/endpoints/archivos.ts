import { clienteHttp } from "../clienteHttp"

export interface RespuestaImagen {
  id_cdn: string
  url: string
}

export async function subirImagen(archivo: File): Promise<RespuestaImagen> {
  const formulario = new FormData()
  formulario.append("imagen", archivo)
  const { data } = await clienteHttp.post<RespuestaImagen>(
    "/archivos/imagen",
    formulario,
    { headers: { "Content-Type": "multipart/form-data" } },
  )
  return data
}

export async function eliminarImagen(idCdn: string): Promise<void> {
  await clienteHttp.delete(`/archivos/imagen/${idCdn}`)
}
