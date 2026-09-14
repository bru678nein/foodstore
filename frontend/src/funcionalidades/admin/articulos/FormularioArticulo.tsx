import { type FormEvent, useState, useMemo } from "react"
import { AlertTriangle } from "lucide-react"
import { Boton } from "@/componentes/ui/Boton"
import { CampoTexto } from "@/componentes/ui/CampoTexto"
import { CargadorImagen } from "@/componentes/comunes/CargadorImagen"
import { useConsultaCategorias } from "@/funcionalidades/catalogo/hooks/useConsultaCategorias"
import { useConsultaComponentes } from "@/funcionalidades/catalogo/hooks/useConsultaComponentes"
import { formatearMoneda } from "@/lib/formato"
import type { ArticuloLista, EntradaArticulo, CategoriaSalida } from "@/tipos/catalogo"

function aplanarCategorias(cats: CategoriaSalida[]): CategoriaSalida[] {
  return cats.flatMap((c) => [c, ...aplanarCategorias(c.hijos ?? [])])
}

export interface ImagenPendiente { url: string; idCdn: string }

interface PropsFormularioArticulo {
  inicial?: ArticuloLista
  alGuardar: (entrada: EntradaArticulo, imagen?: ImagenPendiente) => void
  cargando?: boolean
  alCancelar?: () => void
}

interface ItemComposicion {
  componente_id: number
  extraible: boolean
  cantidad_gramos: number
}

export function FormularioArticulo({
  inicial,
  alGuardar,
  cargando,
  alCancelar,
}: PropsFormularioArticulo) {
  const { data: categorias } = useConsultaCategorias()
  const { data: componentes } = useConsultaComponentes()

  const [titulo, setTitulo] = useState(inicial?.titulo ?? "")
  const [descripcion, setDescripcion] = useState("")
  const [precio, setPrecio] = useState(
    inicial?.precio_unitario != null ? String(inicial.precio_unitario) : "",
  )
  const [existencias, setExistencias] = useState(
    inicial?.existencias != null ? String(inicial.existencias) : "0",
  )
  const [disponible, setDisponible] = useState(inicial?.disponible ?? true)
  const [esPrefabricado, setEsPrefabricado] = useState(inicial?.es_prefabricado ?? false)
  const [categoriasSel, setCategoriasSel] = useState<number[]>(
    inicial?.categorias.map((c) => c.id) ?? [],
  )
  const [composicion, setComposicion] = useState<ItemComposicion[]>([])
  const [margen, setMargen] = useState(30)
  const [imagenPendiente, setImagenPendiente] = useState<ImagenPendiente | null>(null)

  const costoIngredientes = useMemo(() => {
    if (!componentes) return 0
    return composicion.reduce((total, item) => {
      const comp = componentes.find((c) => c.id === item.componente_id)
      return total + (comp?.precio_unitario ?? 0) * item.cantidad_gramos
    }, 0)
  }, [composicion, componentes])

  const precioSugerido = costoIngredientes * (1 + margen / 100)
  const imagenUrl = imagenPendiente?.url ?? inicial?.imagen_principal ?? null

  const alternarCategoria = (id: number) =>
    setCategoriasSel((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id],
    )

  const estaEnComposicion = (id: number) =>
    composicion.some((c) => c.componente_id === id)

  const alternarComponente = (id: number) => {
    setComposicion((prev) =>
      estaEnComposicion(id)
        ? prev.filter((c) => c.componente_id !== id)
        : [...prev, { componente_id: id, extraible: false, cantidad_gramos: 0 }],
    )
  }

  const alternarExtraible = (id: number) => {
    setComposicion((prev) =>
      prev.map((c) =>
        c.componente_id === id ? { ...c, extraible: !c.extraible } : c,
      ),
    )
  }

  const setCantidadGramos = (id: number, gramos: number) => {
    setComposicion((prev) =>
      prev.map((c) =>
        c.componente_id === id ? { ...c, cantidad_gramos: gramos } : c,
      ),
    )
  }

  const manejarEnvio = (e: FormEvent) => {
    e.preventDefault()
    alGuardar(
      {
        titulo,
        descripcion,
        precio_unitario: Number(precio),
        existencias: Number(existencias),
        disponible,
        es_prefabricado: esPrefabricado,
        categorias: categoriasSel,
        composicion: esPrefabricado ? [] : composicion,
      },
      imagenPendiente ?? undefined,
    )
  }

  return (
    <form onSubmit={manejarEnvio} className="space-y-4">
      <CampoTexto
        etiqueta="Título"
        required
        value={titulo}
        onChange={(e) => setTitulo(e.target.value)}
      />
      <div>
        <label className="mb-1 block text-sm font-medium text-gray-700">
          Descripción
        </label>
        <textarea
          rows={3}
          value={descripcion}
          onChange={(e) => setDescripcion(e.target.value)}
          className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm focus:border-primario-500 focus:outline-none focus:ring-2 focus:ring-primario-500"
        />
      </div>
      <div className="grid grid-cols-2 gap-3">
        <CampoTexto
          etiqueta="Precio unitario"
          type="number"
          min="0"
          step="0.01"
          required
          value={precio}
          onChange={(e) => setPrecio(e.target.value)}
        />
        <CampoTexto
          etiqueta="Existencias"
          type="number"
          min="0"
          required
          value={existencias}
          onChange={(e) => setExistencias(e.target.value)}
        />
      </div>

      
      <div>
        <p className="mb-1 text-sm font-medium text-gray-700">Categorías</p>
        <div className="flex flex-wrap gap-2">
          {aplanarCategorias(categorias ?? []).map((categoria) => (
            <button
              key={categoria.id}
              type="button"
              onClick={() => alternarCategoria(categoria.id)}
              className={`rounded-full px-3 py-1 text-sm ${
                categoriasSel.includes(categoria.id)
                  ? "bg-primario-500 text-white"
                  : "bg-gray-100 text-gray-600"
              }`}
            >
              {categoria.nombre}
            </button>
          ))}
        </div>
      </div>

      
      <label className="flex items-center gap-2 text-sm text-gray-700">
        <input
          type="checkbox"
          checked={esPrefabricado}
          onChange={(e) => setEsPrefabricado(e.target.checked)}
          className="h-4 w-4 accent-primario-500"
        />
        Producto prefabricado
      </label>

      
      {!esPrefabricado && <div>
        <p className="mb-1 text-sm font-medium text-gray-700">Ingredientes</p>
        {componentes && componentes.length > 0 ? (
          <div className="max-h-48 overflow-y-auto rounded-lg border border-gray-200 p-2">
            <div className="space-y-1">
              {[...componentes]
                .sort((a, b) => a.denominacion.localeCompare(b.denominacion, "es"))
                .map((comp) => {
                const seleccionado = estaEnComposicion(comp.id)
                const item = composicion.find((c) => c.componente_id === comp.id)
                return (
                  <div
                    key={comp.id}
                    className="flex items-center justify-between rounded px-2 py-1 hover:bg-gray-50"
                  >
                    <label className="flex cursor-pointer items-center gap-2 text-sm">
                      <input
                        type="checkbox"
                        checked={seleccionado}
                        onChange={() => alternarComponente(comp.id)}
                        className="h-4 w-4 accent-primario-500"
                      />
                      <span className={seleccionado ? "font-medium" : "text-gray-600"}>
                        {comp.denominacion}
                      </span>
                      {comp.genera_alergia && (
                        <span className="flex items-center rounded-full bg-red-100 p-0.5 text-red-500">
                          <AlertTriangle className="h-3 w-3" />
                        </span>
                      )}
                    </label>

                    {seleccionado && (
                      <div className="flex items-center gap-3">
                        <div className="flex items-center gap-1">
                          <input
                            type="number"
                            min="0"
                            value={item?.cantidad_gramos ?? 0}
                            onChange={(e) =>
                              setCantidadGramos(comp.id, Math.max(0, parseInt(e.target.value) || 0))
                            }
                            className="w-16 rounded border border-gray-300 px-1.5 py-0.5 text-xs focus:border-primario-500 focus:outline-none"
                          />
                          <span className="text-xs text-gray-400">{comp.unidad ?? "g"}</span>
                        </div>
                        <label className="flex cursor-pointer items-center gap-1 text-xs text-gray-500">
                          <input
                            type="checkbox"
                            checked={item?.extraible ?? false}
                            onChange={() => alternarExtraible(comp.id)}
                            className="h-3 w-3 accent-orange-500"
                          />
                          removible
                        </label>
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          </div>
        ) : (
          <p className="text-xs text-gray-400">
            No hay ingredientes cargados. Creá algunos en "Ingredientes".
          </p>
        )}
        {composicion.length > 0 && (
          <p className="mt-1 text-xs text-gray-400">
            {composicion.length} ingrediente{composicion.length !== 1 ? "s" : ""} seleccionado
            {composicion.length !== 1 ? "s" : ""}
          </p>
        )}
      </div>}

      
      {!esPrefabricado && composicion.length > 0 && costoIngredientes > 0 && (
        <div className="rounded-xl border border-primario-100 bg-primario-50 p-4 space-y-3">
          <p className="text-sm font-semibold text-primario-800">Calculadora de precio</p>
          <div className="flex items-center gap-3">
            <label className="text-sm text-gray-600 whitespace-nowrap">Margen de ganancia</label>
            <div className="flex items-center gap-1">
              <input
                type="number"
                min="0"
                max="10000"
                step="1"
                value={margen}
                onChange={(e) => setMargen(Math.max(0, parseInt(e.target.value) || 0))}
                className="w-20 rounded-lg border border-gray-300 px-2 py-1 text-sm focus:border-primario-500 focus:outline-none focus:ring-2 focus:ring-primario-500"
              />
              <span className="text-sm text-gray-500">%</span>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-2 text-sm">
            <div className="rounded-lg bg-white px-3 py-2">
              <p className="text-xs text-gray-400">Costo de ingredientes</p>
              <p className="font-medium text-gray-700">{formatearMoneda(costoIngredientes)}</p>
            </div>
            <div className="rounded-lg bg-white px-3 py-2">
              <p className="text-xs text-gray-400">Precio sugerido</p>
              <p className="font-semibold text-primario-700">{formatearMoneda(precioSugerido)}</p>
            </div>
          </div>
          <Boton
            type="button"
            variante="contorno"
            onClick={() => setPrecio(precioSugerido.toFixed(2))}
          >
            Aplicar precio sugerido
          </Boton>
        </div>
      )}

      
      <div>
        <p className="mb-1 text-sm font-medium text-gray-700">
          Imagen principal
        </p>
        <CargadorImagen alSubir={(url, idCdn) => setImagenPendiente({ url, idCdn })} />
        {imagenUrl && (
          <img
            src={imagenUrl}
            alt="Imagen"
            className="mt-2 h-20 w-20 rounded object-cover"
          />
        )}
      </div>

      <label className="flex items-center gap-2 text-sm text-gray-700">
        <input
          type="checkbox"
          checked={disponible}
          onChange={(e) => setDisponible(e.target.checked)}
          className="h-4 w-4 accent-primario-500"
        />
        Disponible para la venta
      </label>

      <div className="flex justify-end gap-2 pt-2">
        {alCancelar && (
          <Boton type="button" variante="contorno" onClick={alCancelar}>
            Cancelar
          </Boton>
        )}
        <Boton type="submit" cargando={cargando}>
          Guardar artículo
        </Boton>
      </div>
    </form>
  )
}
