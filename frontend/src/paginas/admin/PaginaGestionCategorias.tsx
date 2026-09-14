import { useState } from "react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Boton } from "@/componentes/ui/Boton"
import { CampoTexto } from "@/componentes/ui/CampoTexto"
import { Modal } from "@/componentes/ui/Modal"
import { Spinner } from "@/componentes/ui/Spinner"
import {
  actualizarCategoria,
  crearCategoria,
  eliminarCategoria,
  listarCategorias,
} from "@/api/endpoints/catalogo"
import { clavesConsulta } from "@/lib/clavesConsulta"
import type { CategoriaSalida } from "@/tipos/catalogo"
import { type FormEvent } from "react"

function aplanarCategorias(categorias: CategoriaSalida[], nivel = 0): Array<CategoriaSalida & { nivel: number }> {
  return categorias.flatMap((c) => [
    { ...c, nivel },
    ...aplanarCategorias(c.hijos ?? [], nivel + 1),
  ])
}

function ordenarCategorias(cats: CategoriaSalida[]): CategoriaSalida[] {
  return [...cats]
    .sort((a, b) => a.nombre.localeCompare(b.nombre, "es"))
    .map((c) => ({ ...c, hijos: ordenarCategorias(c.hijos ?? []) }))
}

function FormularioCategoria({
  inicial,
  todasCategorias,
  cargando,
  alGuardar,
  alCancelar,
}: {
  inicial?: CategoriaSalida
  todasCategorias: CategoriaSalida[]
  cargando?: boolean
  alGuardar: (nombre: string, padre_id: number | null) => void
  alCancelar: () => void
}) {
  const [nombre, setNombre] = useState(inicial?.nombre ?? "")
  const [padreId, setPadreId] = useState<number | null>(inicial?.padre_id ?? null)

  const planas = aplanarCategorias(todasCategorias)
  const opciones = inicial
    ? planas.filter((c) => c.id !== inicial.id)
    : planas

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (!nombre.trim()) return
    alGuardar(nombre.trim(), padreId)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <CampoTexto
        etiqueta="Nombre"
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
        placeholder="Ej: Hamburguesas"
        required
      />
      <div>
        <label className="mb-1 block text-sm font-medium text-gray-700">
          Categoría padre
        </label>
        <select
          value={padreId ?? ""}
          onChange={(e) => setPadreId(e.target.value ? Number(e.target.value) : null)}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primario-500 focus:outline-none focus:ring-2 focus:ring-primario-500"
        >
          <option value="">Sin categoría padre (raíz)</option>
          {opciones.map((c) => (
            <option key={c.id} value={c.id}>
              {"  ".repeat(c.nivel)}{c.nivel > 0 ? "↳ " : ""}{c.nombre}
            </option>
          ))}
        </select>
      </div>
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

function FilaCategoria({
  categoria,
  nivel,
  alEditar,
  alEliminar,
}: {
  categoria: CategoriaSalida
  nivel: number
  alEditar: (c: CategoriaSalida) => void
  alEliminar: (id: number) => void
}) {
  return (
    <>
      <div
        className="flex items-center justify-between rounded-xl border border-gray-100 bg-white p-4 shadow-sm"
        style={{ marginLeft: `${nivel * 1.5}rem` }}
      >
        <div className="flex items-center gap-2">
          {nivel > 0 && <span className="text-gray-300 text-sm">↳</span>}
          <span className="font-medium">{categoria.nombre}</span>
          {(categoria.hijos?.length ?? 0) > 0 && (
            <span className="rounded-full bg-primario-100 px-2 py-0.5 text-xs font-medium text-primario-600">
              {categoria.hijos.length} subcategoría{categoria.hijos.length !== 1 ? "s" : ""}
            </span>
          )}
        </div>
        <div className="flex gap-3">
          <button
            type="button"
            onClick={() => alEditar(categoria)}
            className="text-sm text-secundario-600 hover:underline"
          >
            Editar
          </button>
          <button
            type="button"
            onClick={() => alEliminar(categoria.id)}
            className="text-sm text-error hover:underline"
          >
            Eliminar
          </button>
        </div>
      </div>
      {(categoria.hijos ?? []).map((hijo) => (
        <FilaCategoria
          key={hijo.id}
          categoria={hijo}
          nivel={nivel + 1}
          alEditar={alEditar}
          alEliminar={alEliminar}
        />
      ))}
    </>
  )
}

export function PaginaGestionCategorias() {
  const cliente = useQueryClient()
  const clave = clavesConsulta.categorias.lista()
  const invalidar = () => cliente.invalidateQueries({ queryKey: clave })

  const { data: categorias, isLoading } = useQuery({
    queryKey: clave,
    queryFn: listarCategorias,
  })

  const [modalAbierto, setModalAbierto] = useState(false)
  const [editando, setEditando] = useState<CategoriaSalida | null>(null)

  const crear = useMutation({
    mutationFn: (datos: { nombre: string; padre_id: number | null }) =>
      crearCategoria({ nombre: datos.nombre, padre_id: datos.padre_id }),
    onSuccess: invalidar,
  })

  const actualizar = useMutation({
    mutationFn: ({ id, datos }: { id: number; datos: { nombre: string; padre_id: number | null } }) =>
      actualizarCategoria(id, { nombre: datos.nombre, padre_id: datos.padre_id }),
    onSuccess: invalidar,
  })

  const eliminar = useMutation({
    mutationFn: (id: number) => eliminarCategoria(id),
    onSuccess: invalidar,
  })

  const abrirNuevo = () => {
    setEditando(null)
    setModalAbierto(true)
  }

  const abrirEdicion = (cat: CategoriaSalida) => {
    setEditando(cat)
    setModalAbierto(true)
  }

  const cerrar = () => setModalAbierto(false)

  const guardar = (nombre: string, padre_id: number | null) => {
    if (editando) {
      actualizar.mutate({ id: editando.id, datos: { nombre, padre_id } }, { onSuccess: cerrar })
    } else {
      crear.mutate({ nombre, padre_id }, { onSuccess: cerrar })
    }
  }

  const todasCategorias = ordenarCategorias(categorias ?? [])

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Gestión de categorías</h1>
        <Boton onClick={abrirNuevo}>+ Nueva categoría</Boton>
      </div>

      {isLoading ? (
        <Spinner />
      ) : (
        <div className="space-y-2">
          {todasCategorias.map((cat) => (
            <FilaCategoria
              key={cat.id}
              categoria={cat}
              nivel={0}
              alEditar={abrirEdicion}
              alEliminar={(id) => eliminar.mutate(id)}
            />
          ))}
        </div>
      )}

      <Modal
        abierto={modalAbierto}
        alCerrar={cerrar}
        titulo={editando ? "Editar categoría" : "Nueva categoría"}
      >
        <FormularioCategoria
          inicial={editando ?? undefined}
          todasCategorias={todasCategorias}
          cargando={crear.isPending || actualizar.isPending}
          alGuardar={guardar}
          alCancelar={cerrar}
        />
      </Modal>
    </div>
  )
}
