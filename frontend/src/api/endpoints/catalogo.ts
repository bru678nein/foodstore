import { clienteHttp } from "../clienteHttp"
import type {
  ArticuloDetalle,
  ArticuloLista,
  Componente,
  EntradaArticulo,
  EntradaCategoria,
  EntradaComponente,
  ParametrosArticulos,
  RespuestaPaginada,
  CategoriaSalida,
} from "@/tipos/catalogo"

export async function listarArticulos(
  params: ParametrosArticulos,
): Promise<RespuestaPaginada<ArticuloLista>> {
  const { data } = await clienteHttp.get<RespuestaPaginada<ArticuloLista>>(
    "/articulos",
    {
      params: {
        categoria: params.categoria,
        disponible: params.disponible,
        q: params.q || undefined,
        pagina: params.pagina ?? 1,
        por_pagina: params.porPagina ?? 12,
      },
    },
  )
  return data
}

export async function obtenerArticulo(id: number): Promise<ArticuloDetalle> {
  const { data } = await clienteHttp.get<ArticuloDetalle>(`/articulos/${id}`)
  return data
}

export async function crearArticulo(
  entrada: EntradaArticulo,
): Promise<ArticuloDetalle> {
  const { data } = await clienteHttp.post<ArticuloDetalle>(
    "/articulos",
    entrada,
  )
  return data
}

export async function actualizarArticulo(
  id: number,
  entrada: EntradaArticulo,
): Promise<ArticuloDetalle> {
  const { data } = await clienteHttp.put<ArticuloDetalle>(
    `/articulos/${id}`,
    entrada,
  )
  return data
}

export async function eliminarArticulo(id: number): Promise<void> {
  await clienteHttp.delete(`/articulos/${id}`)
}

export async function actualizarExistencias(
  id: number,
  existencias: number,
): Promise<ArticuloLista> {
  const { data } = await clienteHttp.patch<ArticuloLista>(
    `/articulos/${id}/existencias`,
    { existencias },
  )
  return data
}

export async function vincularImagenArticulo(
  id: number,
  url: string,
  idCdn: string,
  posicion = 0,
): Promise<void> {
  await clienteHttp.post(`/articulos/${id}/galeria`, null, {
    params: { url_imagen: url, id_cdn: idCdn, posicion },
  })
}

export async function eliminarImagenGaleria(
  id: number,
  imgId: number,
): Promise<void> {
  await clienteHttp.delete(`/articulos/${id}/galeria/${imgId}`)
}

export async function listarCategorias(): Promise<CategoriaSalida[]> {
  const { data } = await clienteHttp.get<CategoriaSalida[]>("/categorias")
  return data
}

export async function crearCategoria(entrada: EntradaCategoria): Promise<CategoriaSalida> {
  const { data } = await clienteHttp.post<CategoriaSalida>("/categorias", entrada)
  return data
}

export async function actualizarCategoria(
  id: number,
  entrada: EntradaCategoria,
): Promise<CategoriaSalida> {
  const { data } = await clienteHttp.put<CategoriaSalida>(`/categorias/${id}`, entrada)
  return data
}

export async function eliminarCategoria(id: number): Promise<void> {
  await clienteHttp.delete(`/categorias/${id}`)
}

export async function listarComponentes(): Promise<Componente[]> {
  const { data } = await clienteHttp.get<Componente[]>("/componentes")
  return data
}

export async function crearComponente(
  entrada: EntradaComponente,
): Promise<Componente> {
  const { data } = await clienteHttp.post<Componente>("/componentes", entrada)
  return data
}

export async function actualizarComponente(
  id: number,
  entrada: EntradaComponente,
): Promise<Componente> {
  const { data } = await clienteHttp.put<Componente>(
    `/componentes/${id}`,
    entrada,
  )
  return data
}

export async function eliminarComponente(id: number): Promise<void> {
  await clienteHttp.delete(`/componentes/${id}`)
}
