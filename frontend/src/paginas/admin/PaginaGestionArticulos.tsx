import { useState } from "react"
import { Boton } from "@/componentes/ui/Boton"
import { Modal } from "@/componentes/ui/Modal"
import { Spinner } from "@/componentes/ui/Spinner"
import { TablaArticulos } from "@/funcionalidades/admin/articulos/TablaArticulos"
import { FormularioArticulo, type ImagenPendiente } from "@/funcionalidades/admin/articulos/FormularioArticulo"
import { useAdminArticulos } from "@/funcionalidades/admin/articulos/hooks/useAdminArticulos"
import { vincularImagenArticulo } from "@/api/endpoints/catalogo"
import type { ArticuloLista, ArticuloDetalle, EntradaArticulo } from "@/tipos/catalogo"

export function PaginaGestionArticulos() {
  const { consulta, crear, actualizar, eliminar, ajustarExistencias } =
    useAdminArticulos()
  const [modalAbierto, setModalAbierto] = useState(false)
  const [editando, setEditando] = useState<ArticuloLista | null>(null)

  const abrirNuevo = () => {
    setEditando(null)
    setModalAbierto(true)
  }

  const abrirEdicion = (articulo: ArticuloLista) => {
    setEditando(articulo)
    setModalAbierto(true)
  }

  const cerrar = () => setModalAbierto(false)

  const vincularImagen = async (articulo: ArticuloDetalle, imagen?: ImagenPendiente) => {
    if (imagen) {
      await vincularImagenArticulo(articulo.id, imagen.url, imagen.idCdn)
    }
  }

  const guardar = (entrada: EntradaArticulo, imagen?: ImagenPendiente) => {
    if (editando) {
      actualizar.mutate(
        { id: editando.id, entrada },
        { onSuccess: async (art) => { await vincularImagen(art, imagen); cerrar() } },
      )
    } else {
      crear.mutate(entrada, {
        onSuccess: async (art) => { await vincularImagen(art, imagen); cerrar() },
      })
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Gestión de artículos</h1>
        <Boton onClick={abrirNuevo}>+ Nuevo artículo</Boton>
      </div>

      {consulta.isLoading ? (
        <Spinner />
      ) : (
        <TablaArticulos
          articulos={[...(consulta.data?.items ?? [])].sort((a, b) =>
            a.titulo.localeCompare(b.titulo, "es"),
          )}
          alEditar={abrirEdicion}
          alEliminar={(id) => eliminar.mutate(id)}
          alAjustarExistencias={(id, existencias) =>
            ajustarExistencias.mutate({ id, existencias })
          }
        />
      )}

      <Modal
        abierto={modalAbierto}
        alCerrar={cerrar}
        titulo={editando ? "Editar artículo" : "Nuevo artículo"}
        anchoMax="max-w-2xl"
      >
        <FormularioArticulo
          inicial={editando ?? undefined}
          cargando={crear.isPending || actualizar.isPending}
          alGuardar={guardar}
          alCancelar={cerrar}
        />
      </Modal>
    </div>
  )
}
