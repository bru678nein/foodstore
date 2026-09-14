import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useQueryClient } from "@tanstack/react-query"
import { crearOrden } from "@/api/endpoints/ordenes"
import { crearPreferencia } from "@/api/endpoints/cobros"
import { carritoStore } from "@/almacenes/carritoStore"
import { pagoStore } from "@/almacenes/pagoStore"
import { clavesConsulta } from "@/lib/clavesConsulta"
import { extraerMensajeError } from "@/api/clienteHttp"
import type { FormaPago, PartidaNueva, TipoEntrega } from "@/tipos/ordenes"

interface ParamsConfirmar {
  domicilioId: number | null
  tipoEntrega: TipoEntrega
  formaPago: FormaPago
}

interface ResultadoPago {
  ordenId: number
  preferenciaId: string | null
  totalOrden: number
}

export function useProcesarPago() {
  const navigate = useNavigate()
  const cliente = useQueryClient()
  const elementos = carritoStore((s) => s.elementos)
  const vaciarCarrito = carritoStore((s) => s.vaciarCarrito)
  const iniciarProceso = pagoStore((s) => s.iniciarProceso)
  const [procesando, setProcesando] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const confirmarPedido = async ({
    domicilioId,
    tipoEntrega,
    formaPago,
  }: ParamsConfirmar): Promise<ResultadoPago | null> => {
    setError(null)
    if (elementos.length === 0) {
      setError("Tu carrito está vacío")
      return null
    }
    setProcesando(true)
    try {
      const partidas: PartidaNueva[] = elementos.map((e) => ({
        articulo_id: e.articuloId,
        unidades: e.cantidad,
        componentes_excluidos: e.componentesAExcluir,
      }))

      const totalAntes = elementos.reduce((t, e) => t + Number(e.precioUnitario) * e.cantidad, 0)

      const orden = await crearOrden({
        domicilio_id: domicilioId ?? undefined,
        tipo_entrega: tipoEntrega,
        forma_pago_codigo: formaPago,
        partidas,
      })

      vaciarCarrito()
      cliente.invalidateQueries({ queryKey: clavesConsulta.ordenes.misOrdenes() })
      void cliente.invalidateQueries({
        predicate: (query) => {
          const k = query.queryKey[0]
          return k === "articulos" || k === "componentes"
        },
      })

      if (formaPago === "MERCADOPAGO") {
        const preferencia = await crearPreferencia(orden.id)
        iniciarProceso(orden.id, preferencia.id_preferencia)
        return { ordenId: orden.id, preferenciaId: preferencia.id_preferencia, totalOrden: totalAntes }
      }

      if (formaPago === "MP_CARD") {
        return { ordenId: orden.id, preferenciaId: null, totalOrden: totalAntes }
      }

            navigate(`/mis-ordenes/${orden.id}`)
      return null
    } catch (err) {
      setError(extraerMensajeError(err, "No se pudo procesar el pedido"))
      return null
    } finally {
      setProcesando(false)
    }
  }

  return { confirmarPedido, procesando, error }
}
