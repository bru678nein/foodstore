import { useState } from "react"
import { Boton } from "@/componentes/ui/Boton"
import { Insignia } from "@/componentes/ui/Insignia"
import { formatearMoneda } from "@/lib/formato"
import type { ArticuloLista } from "@/tipos/catalogo"

interface PropsTablaArticulos {
  articulos: ArticuloLista[]
  alEditar: (articulo: ArticuloLista) => void
  alEliminar: (id: number) => void
  alAjustarExistencias: (id: number, existencias: number) => void
}

function CeldaExistencias({
  articulo,
  alAjustar,
}: {
  articulo: ArticuloLista
  alAjustar: (id: number, existencias: number) => void
}) {
  const [valor, setValor] = useState(String(articulo.existencias))
  const cambio = Number(valor) !== articulo.existencias

  return (
    <div className="flex items-center gap-1">
      <input
        type="number"
        min="0"
        value={valor}
        onChange={(e) => setValor(e.target.value)}
        className="w-20 rounded border border-gray-300 px-2 py-1 text-sm focus:border-primario-500 focus:outline-none"
      />
      {cambio && (
        <button
          onClick={() => alAjustar(articulo.id, Number(valor))}
          className="rounded bg-primario-500 px-2 py-1 text-xs text-white hover:bg-primario-600"
        >
          ✓
        </button>
      )}
    </div>
  )
}

export function TablaArticulos({
  articulos,
  alEditar,
  alEliminar,
  alAjustarExistencias,
}: PropsTablaArticulos) {
  if (articulos.length === 0) {
    return (
      <p className="rounded-lg border border-dashed border-gray-200 p-8 text-center text-sm text-gray-400">
        No hay artículos cargados.
      </p>
    )
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-gray-100 bg-white shadow-sm">
      <table className="min-w-full divide-y divide-gray-100 text-sm">
        <thead className="bg-gray-50 text-left text-xs uppercase tracking-wide text-gray-500">
          <tr>
            <th className="px-4 py-3">Título</th>
            <th className="px-4 py-3">Precio</th>
            <th className="px-4 py-3">Existencias</th>
            <th className="px-4 py-3">Categorías</th>
            <th className="px-4 py-3">Estado</th>
            <th className="px-4 py-3">Acciones</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-50">
          {articulos.map((articulo) => (
            <tr key={articulo.id} className="hover:bg-gray-50">
              <td className="px-4 py-3 font-medium">{articulo.titulo}</td>
              <td className="px-4 py-3">
                {formatearMoneda(articulo.precio_unitario)}
              </td>
              <td className="px-4 py-3">
                <CeldaExistencias
                  articulo={articulo}
                  alAjustar={alAjustarExistencias}
                />
              </td>
              <td className="px-4 py-3 text-gray-500">
                {articulo.categorias.map((c) => c.nombre).join(", ") || "—"}
              </td>
              <td className="px-4 py-3">
                <Insignia
                  className={
                    articulo.disponible
                      ? "bg-green-100 text-green-700"
                      : "bg-gray-100 text-gray-600"
                  }
                >
                  {articulo.disponible ? "Disponible" : "Oculto"}
                </Insignia>
              </td>
              <td className="px-4 py-3">
                <div className="flex gap-2">
                  <Boton
                    tamano="sm"
                    variante="contorno"
                    onClick={() => alEditar(articulo)}
                  >
                    Editar
                  </Boton>
                  <Boton
                    tamano="sm"
                    variante="peligro"
                    onClick={() => alEliminar(articulo.id)}
                  >
                    Eliminar
                  </Boton>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
