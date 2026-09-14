import { type FormEvent, useState } from "react"
import { Link } from "react-router-dom"
import { Boton } from "@/componentes/ui/Boton"
import { CampoTexto } from "@/componentes/ui/CampoTexto"
import { useRegistro } from "./hooks/useRegistro"
import { extraerMensajeError } from "@/api/clienteHttp"

export function FormularioRegistro() {
  const [nombre, setNombre] = useState("")
  const [correo, setCorreo] = useState("")
  const [contrasena, setContrasena] = useState("")
  const [confirmar, setConfirmar] = useState("")
  const [errorLocal, setErrorLocal] = useState<string | null>(null)
  const registro = useRegistro("/")

  const manejarEnvio = (e: FormEvent) => {
    e.preventDefault()
    setErrorLocal(null)
    if (contrasena !== confirmar) {
      setErrorLocal("Las contraseñas no coinciden")
      return
    }
    if (contrasena.length < 6) {
      setErrorLocal("La contraseña debe tener al menos 6 caracteres")
      return
    }
    registro.mutate({
      nombre_completo: nombre,
      correo,
      contrasena,
    })
  }

  return (
    <form onSubmit={manejarEnvio} className="space-y-4">
      <CampoTexto
        etiqueta="Nombre completo"
        name="nombre"
        autoComplete="name"
        required
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
      />
      <CampoTexto
        etiqueta="Correo electrónico"
        type="email"
        name="correo"
        autoComplete="email"
        required
        value={correo}
        onChange={(e) => setCorreo(e.target.value)}
      />
      <CampoTexto
        etiqueta="Contraseña"
        type="password"
        name="contrasena"
        autoComplete="new-password"
        required
        value={contrasena}
        onChange={(e) => setContrasena(e.target.value)}
      />
      <CampoTexto
        etiqueta="Confirmar contraseña"
        type="password"
        name="confirmar"
        autoComplete="new-password"
        required
        value={confirmar}
        onChange={(e) => setConfirmar(e.target.value)}
        error={errorLocal ?? undefined}
      />

      {registro.isError && (
        <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-error">
          {extraerMensajeError(registro.error, "No se pudo registrar")}
        </p>
      )}

      <Boton type="submit" className="w-full" cargando={registro.isPending}>
        Crear cuenta
      </Boton>

      <p className="text-center text-sm text-gray-500">
        ¿Ya tenés cuenta?{" "}
        <Link to="/ingresar" className="font-medium text-primario-600">
          Ingresá
        </Link>
      </p>
    </form>
  )
}
