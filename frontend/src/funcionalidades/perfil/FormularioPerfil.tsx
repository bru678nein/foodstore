import { useState } from "react"
import { Boton } from "@/componentes/ui/Boton"
import { CampoTexto } from "@/componentes/ui/CampoTexto"
import { sesionStore } from "@/almacenes/sesionStore"

export function FormularioPerfil() {
  const cuenta = sesionStore((s) => s.cuenta)
  const establecerSesion = sesionStore((s) => s.establecerSesion)
  const tokenAcceso = sesionStore((s) => s.tokenAcceso)
  const tokenRenovacion = sesionStore((s) => s.tokenRenovacion)
  const [nombre, setNombre] = useState(cuenta?.nombre_completo ?? "")
  const [guardado, setGuardado] = useState(false)

  const manejarGuardar = (e: React.FormEvent) => {
    e.preventDefault()
            if (cuenta && tokenAcceso && tokenRenovacion) {
      establecerSesion(
        { ...cuenta, nombre_completo: nombre },
        tokenAcceso,
        tokenRenovacion,
      )
      setGuardado(true)
      setTimeout(() => setGuardado(false), 2500)
    }
  }

  return (
    <form
      onSubmit={manejarGuardar}
      className="max-w-md space-y-4 rounded-xl border border-gray-100 bg-white p-5 shadow-sm"
    >
      <CampoTexto
        etiqueta="Nombre completo"
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
      />
      <CampoTexto
        etiqueta="Correo electrónico"
        value={cuenta?.correo ?? ""}
        disabled
      />
      <div className="flex items-center gap-3">
        <Boton type="submit">Guardar cambios</Boton>
        {guardado && (
          <span className="text-sm text-exito">Cambios guardados ✓</span>
        )}
      </div>
    </form>
  )
}
