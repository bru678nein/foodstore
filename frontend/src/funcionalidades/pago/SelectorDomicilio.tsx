import { useEffect, useState } from "react"
import { Boton } from "@/componentes/ui/Boton"
import { Modal } from "@/componentes/ui/Modal"
import { ListaDomicilios } from "@/funcionalidades/perfil/ListaDomicilios"
import { FormularioDomicilio } from "@/funcionalidades/perfil/FormularioDomicilio"
import { useDomicilios } from "@/funcionalidades/perfil/hooks/useDomicilios"

interface PropsSelectorDomicilio {
  domicilioSeleccionado: number | null
  alSeleccionar: (id: number) => void
}

export function SelectorDomicilio({
  domicilioSeleccionado,
  alSeleccionar,
}: PropsSelectorDomicilio) {
  const { consulta, crear } = useDomicilios()
  const [modalAbierto, setModalAbierto] = useState(false)

    useEffect(() => {
    if (domicilioSeleccionado || !consulta.data?.length) return
    const predeterminado = consulta.data.find((d) => d.es_predeterminado)
    alSeleccionar((predeterminado ?? consulta.data[0]).id)
  }, [consulta.data, domicilioSeleccionado, alSeleccionar])

  return (
    <div className="space-y-3">
      <ListaDomicilios
        domicilios={consulta.data}
        cargando={consulta.isLoading}
        seleccionableId={domicilioSeleccionado}
        alSeleccionar={alSeleccionar}
      />
      <Boton variante="contorno" onClick={() => setModalAbierto(true)}>
        + Agregar domicilio
      </Boton>

      <Modal
        abierto={modalAbierto}
        alCerrar={() => setModalAbierto(false)}
        titulo="Nuevo domicilio"
      >
        <FormularioDomicilio
          cargando={crear.isPending}
          alGuardar={(entrada) =>
            crear.mutate(entrada, {
              onSuccess: (dom) => {
                alSeleccionar(dom.id)
                setModalAbierto(false)
              },
            })
          }
          alCancelar={() => setModalAbierto(false)}
        />
      </Modal>
    </div>
  )
}
