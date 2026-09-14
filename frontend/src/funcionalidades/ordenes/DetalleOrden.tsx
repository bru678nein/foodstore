import { useEffect } from "react"
import { useQueryClient } from "@tanstack/react-query"
import { Boton } from "@/componentes/ui/Boton"
import { Spinner } from "@/componentes/ui/Spinner"
import { InsigniaEstado } from "@/componentes/comunes/InsigniaEstado"
import { LineaTiempoOrden } from "./LineaTiempoOrden"
import { useCancelarOrden, useDetalleOrden } from "./hooks/useDetalleOrden"
import { useConexionWS } from "@/hooks/useConexionWS"
import { clavesConsulta } from "@/lib/clavesConsulta"
import { formatearMoneda } from "@/lib/formato"

export function DetalleOrden({ ordenId }: { ordenId: number }) {
  const cliente = useQueryClient()
  const { data: orden, isLoading, isError } = useDetalleOrden(ordenId)
  const cancelar = useCancelarOrden(ordenId)
  const { ultimoEvento, estaConectado } = useConexionWS(
    Number.isFinite(ordenId) ? `orden:${ordenId}` : null,
  )

  useEffect(() => {
    if (!ultimoEvento) return
    cliente.invalidateQueries({ queryKey: clavesConsulta.ordenes.detalle(ordenId) })
  }, [ultimoEvento, cliente, ordenId])

  if (isLoading) return <Spinner texto="Cargando orden..." />
  if (isError || !orden)
    return (
      <p className="rounded-lg bg-red-50 px-4 py-3 text-error">
        No se pudo cargar la orden.
      </p>
    )

  const puedeCancelar = orden.estado_actual === "PENDIENTE"

  return (
    <div className="grid gap-6 lg:grid-cols-3">
      <div className="space-y-6 lg:col-span-2">
        <div className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <h1 className="text-xl font-bold">Orden #{orden.id}</h1>
              <p className="flex items-center gap-2 text-xs text-gray-400">
                <span
                  className={`inline-block h-2 w-2 rounded-full ${
                    estaConectado ? "bg-exito" : "bg-gray-300"
                  }`}
                />
                {estaConectado ? "En vivo" : "Sin conexión en vivo"}
              </p>
            </div>
            <InsigniaEstado estado={orden.estado_actual} />
          </div>

          <div className="mt-5 space-y-3">
            {orden.partidas.map((partida) => (
              <div
                key={partida.id}
                className="flex items-start justify-between border-b border-gray-50 pb-3 last:border-0"
              >
                <div>
                  <p className="font-medium text-gray-900">
                    {partida.unidades}× {partida.titulo_capturado}
                  </p>
                  {partida.componentes_excluidos.length > 0 && (
                    <p className="text-xs text-gray-400">
                      Sin: {partida.componentes_excluidos.join(", ")}
                    </p>
                  )}
                </div>
                <span className="font-medium">
                  {formatearMoneda(partida.importe_parcial)}
                </span>
              </div>
            ))}
          </div>

          <div className="mt-4 space-y-2 border-t border-gray-100 pt-4">
            {orden.costo_envio > 0 && (
              <div className="flex justify-between text-sm text-gray-500">
                <span>Subtotal</span>
                <span>{formatearMoneda(orden.subtotal)}</span>
              </div>
            )}
            {orden.descuento > 0 && (
              <div className="flex justify-between text-sm text-green-600">
                <span>Descuento</span>
                <span>− {formatearMoneda(orden.descuento)}</span>
              </div>
            )}
            {orden.costo_envio > 0 && (
              <div className="flex justify-between text-sm text-gray-500">
                <span>Envío</span>
                <span>{formatearMoneda(orden.costo_envio)}</span>
              </div>
            )}
            <div className="flex justify-between text-lg font-bold border-t border-gray-100 pt-2">
              <span>Total</span>
              <span className="text-primario-600">
                {formatearMoneda(orden.total)}
              </span>
            </div>
          </div>

          {puedeCancelar && (
            <div className="mt-5">
              <Boton
                variante="peligro"
                cargando={cancelar.isPending}
                onClick={() => cancelar.mutate()}
              >
                Cancelar orden
              </Boton>
            </div>
          )}
        </div>

        <div className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
          <h2 className="mb-4 font-semibold">Seguimiento</h2>
          <LineaTiempoOrden bitacora={orden.bitacora} />
        </div>
      </div>

      <div className="space-y-6">
        <div className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
          <h2 className="mb-3 font-semibold">Entrega</h2>
          {orden.domicilio ? (
            <>
              <p className="text-sm text-gray-700">
                {orden.domicilio.via} {orden.domicilio.altura}
              </p>
              <p className="text-sm text-gray-500">
                {orden.domicilio.localidad}, {orden.domicilio.provincia}
              </p>
            </>
          ) : (
            <p className="text-sm text-gray-700">Retiro en local</p>
          )}
        </div>

        {orden.cobro && (
          <div className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
            <h2 className="mb-3 font-semibold">Pago</h2>
            <p className="text-sm text-gray-700">Estado: {orden.cobro.estado}</p>
            {orden.cobro.medio && (
              <p className="text-sm text-gray-500">Medio: {orden.cobro.medio}</p>
            )}
            {orden.cobro.init_point && orden.cobro.estado !== "aprobado" && (
              <a
                href={orden.cobro.init_point}
                className="mt-3 inline-block text-sm font-medium text-secundario-600 hover:underline"
              >
                Continuar pago →
              </a>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
