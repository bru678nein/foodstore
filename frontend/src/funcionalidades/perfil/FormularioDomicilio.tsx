import { type FormEvent, useState } from "react"
import { Boton } from "@/componentes/ui/Boton"
import { CampoTexto } from "@/componentes/ui/CampoTexto"
import type { Domicilio, EntradaDomicilio } from "@/tipos/ordenes"

interface PropsFormularioDomicilio {
  inicial?: Domicilio
  alGuardar: (entrada: EntradaDomicilio) => void
  cargando?: boolean
  alCancelar?: () => void
}

export function FormularioDomicilio({
  inicial,
  alGuardar,
  cargando,
  alCancelar,
}: PropsFormularioDomicilio) {
  const [via, setVia] = useState(inicial?.via ?? "")
  const [altura, setAltura] = useState(inicial?.altura ?? "")
  const [localidad, setLocalidad] = useState(inicial?.localidad ?? "")
  const [provincia, setProvincia] = useState(inicial?.provincia ?? "")
  const [codigoPostal, setCodigoPostal] = useState(inicial?.codigo_postal ?? "")

  const manejarEnvio = (e: FormEvent) => {
    e.preventDefault()
    alGuardar({
      via,
      altura,
      localidad,
      provincia,
      codigo_postal: codigoPostal || undefined,
    })
  }

  return (
    <form onSubmit={manejarEnvio} className="space-y-3">
      <div className="grid grid-cols-3 gap-3">
        <div className="col-span-2">
          <CampoTexto
            etiqueta="Calle / Av."
            required
            value={via}
            onChange={(e) => setVia(e.target.value)}
            placeholder="Ej: Av. Corrientes"
          />
        </div>
        <CampoTexto
          etiqueta="Número"
          required
          value={altura}
          onChange={(e) => setAltura(e.target.value)}
          placeholder="1234"
        />
      </div>
      <div className="grid grid-cols-2 gap-3">
        <CampoTexto
          etiqueta="Localidad"
          required
          value={localidad}
          onChange={(e) => setLocalidad(e.target.value)}
          placeholder="Ej: CABA"
        />
        <CampoTexto
          etiqueta="Provincia"
          required
          value={provincia}
          onChange={(e) => setProvincia(e.target.value)}
          placeholder="Ej: Buenos Aires"
        />
      </div>
      <CampoTexto
        etiqueta="Código postal (opcional)"
        value={codigoPostal}
        onChange={(e) => setCodigoPostal(e.target.value)}
        placeholder="1043"
      />
      <div className="flex justify-end gap-2 pt-2">
        {alCancelar && (
          <Boton type="button" variante="contorno" onClick={alCancelar}>
            Cancelar
          </Boton>
        )}
        <Boton type="submit" cargando={cargando}>
          Guardar domicilio
        </Boton>
      </div>
    </form>
  )
}
