import { useRef, useState } from "react"
import { Boton } from "@/componentes/ui/Boton"
import { subirImagen } from "@/api/endpoints/archivos"
import { extraerMensajeError } from "@/api/clienteHttp"

interface PropsCargadorImagen {
  alSubir: (url: string, idCdn: string) => void
  etiqueta?: string
}

export function CargadorImagen({
  alSubir,
  etiqueta = "Subir imagen",
}: PropsCargadorImagen) {
  const refInput = useRef<HTMLInputElement>(null)
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [previa, setPrevia] = useState<string | null>(null)

  const manejarArchivo = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const archivo = e.target.files?.[0]
    if (!archivo) return
    setError(null)
    setCargando(true)
    setPrevia(URL.createObjectURL(archivo))
    try {
      const resultado = await subirImagen(archivo)
      alSubir(resultado.url, resultado.id_cdn)
    } catch (err) {
      setError(extraerMensajeError(err, "No se pudo subir la imagen"))
    } finally {
      setCargando(false)
    }
  }

  return (
    <div className="space-y-2">
      <input
        ref={refInput}
        type="file"
        accept="image/*"
        className="hidden"
        onChange={manejarArchivo}
      />
      <div className="flex items-center gap-3">
        <Boton
          type="button"
          variante="contorno"
          cargando={cargando}
          onClick={() => refInput.current?.click()}
        >
          {etiqueta}
        </Boton>
        {previa && (
          <img
            src={previa}
            alt="Vista previa"
            className="h-12 w-12 rounded object-cover"
          />
        )}
      </div>
      {error && <p className="text-xs text-error">{error}</p>}
    </div>
  )
}
