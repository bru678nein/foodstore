import { useState } from "react"
import { Link } from "react-router-dom"
import { UtensilsCrossed } from "lucide-react"
import { Boton } from "@/componentes/ui/Boton"
import { Modal } from "@/componentes/ui/Modal"
import { carritoStore } from "@/almacenes/carritoStore"
import { obtenerArticulo } from "@/api/endpoints/catalogo"
import { formatearMoneda } from "@/lib/formato"
import type { ArticuloLista, ComposicionItem } from "@/tipos/catalogo"

export function TarjetaArticulo({ articulo }: { articulo: ArticuloLista }) {
  const agregarElemento = carritoStore((s) => s.agregarElemento)
  const [modalAbierto, setModalAbierto] = useState(false)
  const [composicion, setComposicion] = useState<ComposicionItem[]>([])
  const [excluidos, setExcluidos] = useState<number[]>([])
  const [cargandoModal, setCargandoModal] = useState(false)

  const sinStock = articulo.existencias <= 0 || !articulo.disponible

  const agregarDirecto = (excluir: number[] = []) => {
    agregarElemento({
      articuloId: articulo.id,
      titulo: articulo.titulo,
      precioUnitario: Number(articulo.precio_unitario),
      imagenUrl: articulo.imagen_principal,
      componentesAExcluir: excluir,
    })
  }

  const manejarAgregar = async () => {
    if (sinStock) return
    setCargandoModal(true)
    try {
      const detalle = await obtenerArticulo(articulo.id)
      const extraibles = detalle.composicion.filter((c) => c.extraible)
      if (extraibles.length > 0) {
        setComposicion(detalle.composicion)
        setExcluidos([])
        setModalAbierto(true)
      } else {
        agregarDirecto()
      }
    } catch {
      agregarDirecto()
    } finally {
      setCargandoModal(false)
    }
  }

  const alternarExcluido = (id: number) => {
    setExcluidos((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id],
    )
  }

  const confirmarPersonalizado = () => {
    agregarDirecto(excluidos)
    setModalAbierto(false)
  }

  return (
    <>
      <div className="group flex flex-col overflow-hidden rounded-2xl bg-white shadow-tarjeta transition-all duration-200 hover:-translate-y-1 hover:shadow-tarjeta-hover">
        
        <Link to={`/articulos/${articulo.id}`} className="block">
          <div className="relative aspect-[4/3] overflow-hidden bg-crema-100">
            {articulo.imagen_principal ? (
              <img
                src={articulo.imagen_principal}
                alt={articulo.titulo}
                className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-105"
              />
            ) : (
              <div className="flex h-full w-full items-center justify-center text-primario-200">
                <UtensilsCrossed className="h-10 w-10" />
              </div>
            )}
            {sinStock && (
              <div className="absolute inset-0 flex items-center justify-center bg-black/40">
                <span className="rounded-full bg-white/90 px-3 py-1 text-xs font-bold text-gray-700">
                  Sin stock
                </span>
              </div>
            )}
            {articulo.categorias.length > 0 && (
              <div className="absolute bottom-2 left-2 flex gap-1">
                {articulo.categorias.slice(0, 2).map((c) => (
                  <span
                    key={c.id}
                    className="rounded-full bg-black/50 px-2 py-0.5 text-xs font-semibold text-white backdrop-blur-sm"
                  >
                    {c.nombre}
                  </span>
                ))}
              </div>
            )}
          </div>
        </Link>

        
        <div className="flex flex-1 flex-col p-4">
          <Link
            to={`/articulos/${articulo.id}`}
            className="mb-3 font-extrabold leading-tight text-gray-900 hover:text-primario-600 transition-colors"
          >
            {articulo.titulo}
          </Link>

          <div className="mt-auto flex items-center justify-between gap-2">
            <span className="text-xl font-extrabold text-primario-500">
              {formatearMoneda(articulo.precio_unitario)}
            </span>
            <Boton
              tamano="sm"
              disabled={sinStock}
              cargando={cargandoModal}
              onClick={manejarAgregar}
            >
              + Agregar
            </Boton>
          </div>
        </div>
      </div>

      <Modal
        abierto={modalAbierto}
        alCerrar={() => setModalAbierto(false)}
        titulo={`Personalizar ${articulo.titulo}`}
      >
        <p className="mb-4 text-sm text-gray-500">
          Destildá los ingredientes que querés quitar:
        </p>
        <div className="space-y-2">
          {composicion.map((item) => (
            <label
              key={item.id}
              className={`flex items-center justify-between rounded-xl border px-4 py-2.5 transition-colors ${
                item.extraible
                  ? "cursor-pointer border-crema-200 hover:bg-crema-50"
                  : "border-gray-100 opacity-60"
              }`}
            >
              <span className="text-sm font-semibold text-gray-700">{item.denominacion}</span>
              {item.extraible ? (
                <input
                  type="checkbox"
                  checked={!excluidos.includes(item.id)}
                  onChange={() => alternarExcluido(item.id)}
                  className="h-4 w-4 accent-primario-500"
                />
              ) : (
                <span className="text-xs font-semibold text-gray-400">fijo</span>
              )}
            </label>
          ))}
        </div>
        <div className="mt-5 flex justify-end gap-2">
          <Boton variante="contorno" onClick={() => setModalAbierto(false)}>
            Cancelar
          </Boton>
          <Boton onClick={confirmarPersonalizado}>Agregar al carrito</Boton>
        </div>
      </Modal>
    </>
  )
}
