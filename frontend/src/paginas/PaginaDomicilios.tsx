import { useState } from "react"
import { Boton } from "@/componentes/ui/Boton"
import { Modal } from "@/componentes/ui/Modal"
import { ListaDomicilios } from "@/funcionalidades/perfil/ListaDomicilios"
import { FormularioDomicilio } from "@/funcionalidades/perfil/FormularioDomicilio"
import { useDomicilios } from "@/funcionalidades/perfil/hooks/useDomicilios"
import type { Domicilio } from "@/tipos/ordenes"

export function PaginaDomicilios() {
  const { consulta, crear, actualizar, eliminar, predeterminar } =
    useDomicilios()
  const [modalAbierto, setModalAbierto] = useState(false)
  const [editando, setEditando] = useState<Domicilio | null>(null)

  const abrirNuevo = () => {
    setEditando(null)
    setModalAbierto(true)
  }

  const abrirEdicion = (dom: Domicilio) => {
    setEditando(dom)
    setModalAbierto(true)
  }

  const guardar = (entrada: Parameters<typeof crear.mutate>[0]) => {
    if (editando) {
      actualizar.mutate(
        { id: editando.id, entrada },
        { onSuccess: () => setModalAbierto(false) },
      )
    } else {
      crear.mutate(entrada, { onSuccess: () => setModalAbierto(false) })
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Mis domicilios</h1>
        <Boton onClick={abrirNuevo}>+ Nuevo domicilio</Boton>
      </div>

      <ListaDomicilios
        domicilios={consulta.data}
        cargando={consulta.isLoading}
        alPredeterminar={(id) => predeterminar.mutate(id)}
        alEditar={abrirEdicion}
        alEliminar={(id) => eliminar.mutate(id)}
      />

      <Modal
        abierto={modalAbierto}
        alCerrar={() => setModalAbierto(false)}
        titulo={editando ? "Editar domicilio" : "Nuevo domicilio"}
      >
        <FormularioDomicilio
          inicial={editando ?? undefined}
          cargando={crear.isPending || actualizar.isPending}
          alGuardar={guardar}
          alCancelar={() => setModalAbierto(false)}
        />
      </Modal>
    </div>
  )
}
