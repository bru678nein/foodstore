import { type FormEvent, useState } from "react"
import { Link } from "react-router-dom"
import { Boton } from "@/componentes/ui/Boton"
import { CampoTexto } from "@/componentes/ui/CampoTexto"
import { useIngreso } from "./hooks/useIngreso"
import { extraerMensajeError } from "@/api/clienteHttp"

export function FormularioIngreso() {
  const [correo, setCorreo] = useState("")
  const [contrasena, setContrasena] = useState("")
  const ingreso = useIngreso("/")

  const manejarEnvio = (e: FormEvent) => {
    e.preventDefault()
    ingreso.mutate({ correo, contrasena })
  }

  return (
    <form onSubmit={manejarEnvio} className="space-y-4">
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
        autoComplete="current-password"
        required
        value={contrasena}
        onChange={(e) => setContrasena(e.target.value)}
      />

      <div className="rounded-lg border border-gray-200 bg-gray-50 px-4 py-3 text-xs text-gray-500">
        <p className="font-semibold text-gray-600 mb-1">Credenciales de prueba (admin)</p>
        <p>📧 admin@foodstore.com</p>
        <p>🔑 Admin1234!</p>
      </div>

      {ingreso.isError && (
        <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-error">
          {extraerMensajeError(ingreso.error, "Credenciales inválidas")}
        </p>
      )}

      <Boton type="submit" className="w-full" cargando={ingreso.isPending}>
        Ingresar
      </Boton>

      <p className="text-center text-sm text-gray-500">
        ¿No tenés cuenta?{" "}
        <Link to="/registrarse" className="font-medium text-primario-600">
          Registrate
        </Link>
      </p>
    </form>
  )
}
