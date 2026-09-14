import { useState } from "react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Boton } from "@/componentes/ui/Boton"
import { CampoTexto } from "@/componentes/ui/CampoTexto"
import { Modal } from "@/componentes/ui/Modal"
import { Spinner } from "@/componentes/ui/Spinner"
import { formatearMoneda } from "@/lib/formato"
import {
  actualizarComponente,
  crearComponente,
  eliminarComponente,
  listarComponentes,
} from "@/api/endpoints/catalogo"
import { clavesConsulta } from "@/lib/clavesConsulta"
import type { Componente, UnidadMedida } from "@/tipos/catalogo"
import { type FormEvent } from "react"

const UNIDADES: { valor: UnidadMedida; etiqueta: string }[] = [
  { valor: "ml", etiqueta: "Mililitro (ml)" },
  { valor: "l", etiqueta: "Litro (l)" },
  { valor: "g", etiqueta: "Gramo (g)" },
  { valor: "kg", etiqueta: "Kilogramo (kg)" },
]

interface DatosComponente {
  denominacion: string
  existencias: number
  precio_unitario: number
  unidad: UnidadMedida
  genera_alergia: boolean
}

function FormularioComponente({
  inicial,
  cargando,
  alGuardar,
  alCancelar,
}: {
  inicial?: Componente
  cargando?: boolean
  alGuardar: (datos: DatosComponente) => void
  alCancelar: () => void
}) {
  const [denominacion, setDenominacion] = useState(inicial?.denominacion ?? "")
  const [existencias, setExistencias] = useState(inicial?.existencias ?? 0)
  const [precioUnitario, setPrecioUnitario] = useState(inicial?.precio_unitario ?? 0)
  const [unidad, setUnidad] = useState<UnidadMedida>(inicial?.unidad ?? "g")
  const [generaAlergia, setGeneraAlergia] = useState(inicial?.genera_alergia ?? false)

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (!denominacion.trim()) return
    alGuardar({
      denominacion: denominacion.trim(),
      existencias,
      precio_unitario: precioUnitario,
      unidad,
      genera_alergia: generaAlergia,
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <CampoTexto
        etiqueta="Nombre"
        value={denominacion}
        onChange={(e) => setDenominacion(e.target.value)}
        placeholder="Ej: Queso cheddar"
        required
      />

      <div>
        <label className="mb-1 block text-sm font-medium text-gray-700">
          Unidad de medida
        </label>
        <select
          value={unidad}
          onChange={(e) => setUnidad(e.target.value as UnidadMedida)}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primario-500 focus:outline-none focus:ring-2 focus:ring-primario-500"
        >
          {UNIDADES.map((u) => (
            <option key={u.valor} value={u.valor}>
              {u.etiqueta}
            </option>
          ))}
        </select>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <CampoTexto
          etiqueta={`Existencias (${unidad})`}
          type="number"
          min="0"
          value={String(existencias)}
          onChange={(e) => setExistencias(Math.max(0, parseInt(e.target.value) || 0))}
        />
        <CampoTexto
          etiqueta={`Precio por ${unidad}`}
          type="number"
          min="0"
          step="0.01"
          value={String(precioUnitario)}
          onChange={(e) => setPrecioUnitario(Math.max(0, parseFloat(e.target.value) || 0))}
        />
      </div>

      <label className="flex items-center gap-2 text-sm text-gray-700">
        <input
          type="checkbox"
          checked={generaAlergia}
          onChange={(e) => setGeneraAlergia(e.target.checked)}
          className="h-4 w-4 accent-red-500"
        />
        Es alérgeno
      </label>
      <div className="flex justify-end gap-2 pt-2">
        <Boton type="button" variante="contorno" onClick={alCancelar}>
          Cancelar
        </Boton>
        <Boton type="submit" cargando={cargando}>
          {inicial ? "Actualizar" : "Crear"}
        </Boton>
      </div>
    </form>
  )
}

export function PaginaGestionComponentes() {
  const cliente = useQueryClient()
  const clave = clavesConsulta.componentes.lista()
  const invalidar = () => cliente.invalidateQueries({ queryKey: clave })

  const { data: componentes, isLoading } = useQuery({
    queryKey: clave,
    queryFn: listarComponentes,
  })

  const [modalAbierto, setModalAbierto] = useState(false)
  const [editando, setEditando] = useState<Componente | null>(null)

  const crear = useMutation({
    mutationFn: (datos: DatosComponente) => crearComponente(datos),
    onSuccess: invalidar,
  })

  const actualizar = useMutation({
    mutationFn: ({ id, datos }: { id: number; datos: DatosComponente }) =>
      actualizarComponente(id, datos),
    onSuccess: invalidar,
  })

  const eliminar = useMutation({
    mutationFn: (id: number) => eliminarComponente(id),
    onSuccess: invalidar,
  })

  const abrirNuevo = () => {
    setEditando(null)
    setModalAbierto(true)
  }

  const abrirEdicion = (comp: Componente) => {
    setEditando(comp)
    setModalAbierto(true)
  }

  const cerrar = () => setModalAbierto(false)

  const guardar = (datos: DatosComponente) => {
    if (editando) {
      actualizar.mutate({ id: editando.id, datos }, { onSuccess: cerrar })
    } else {
      crear.mutate(datos, { onSuccess: cerrar })
    }
  }

  const ordenados = [...(componentes ?? [])].sort((a, b) =>
    a.denominacion.localeCompare(b.denominacion, "es"),
  )

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Gestión de componentes</h1>
        <Boton onClick={abrirNuevo}>+ Nuevo componente</Boton>
      </div>

      {isLoading ? (
        <Spinner />
      ) : (
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          {ordenados.map((comp) => (
            <div
              key={comp.id}
              className="flex items-center justify-between rounded-xl border border-gray-100 bg-white p-4 shadow-sm"
            >
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-medium">{comp.denominacion}</span>
                  {comp.genera_alergia && (
                    <span className="rounded-full bg-red-100 px-2 py-0.5 text-xs font-medium text-red-600">
                      alérgeno
                    </span>
                  )}
                </div>
                <span className="text-xs text-gray-400">
                  Stock: {comp.existencias} {comp.unidad} · {formatearMoneda(comp.precio_unitario)}/{comp.unidad}
                </span>
              </div>
              <div className="flex gap-3">
                <button
                  type="button"
                  onClick={() => abrirEdicion(comp)}
                  className="text-sm text-secundario-600 hover:underline"
                >
                  Editar
                </button>
                <button
                  type="button"
                  onClick={() => eliminar.mutate(comp.id)}
                  className="text-sm text-error hover:underline"
                >
                  Eliminar
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      <Modal
        abierto={modalAbierto}
        alCerrar={cerrar}
        titulo={editando ? "Editar componente" : "Nuevo componente"}
      >
        <FormularioComponente
          inicial={editando ?? undefined}
          cargando={crear.isPending || actualizar.isPending}
          alGuardar={guardar}
          alCancelar={cerrar}
        />
      </Modal>
    </div>
  )
}
