import { CardPayment } from "@mercadopago/sdk-react"
import { useState } from "react"
import { pagarConTarjetaMP } from "@/api/endpoints/cobros"
import { sesionStore } from "@/almacenes/sesionStore"
import { inicializarMP, MP_CONFIGURADO } from "@/lib/mercadopago"
import { extraerMensajeError } from "@/api/clienteHttp"

inicializarMP()

interface Props {
  ordenId: number
  monto: number
  onExito: (idPago?: string) => void
  onError: (msg: string) => void
}

type DatosFormMP = {
  token: string
  payment_method_id: string
  installments?: number | string
  issuer_id?: string
  payer?: { email?: string }
}

export function CardPaymentMP({ ordenId, monto, onExito, onError }: Props) {
  const correo = sesionStore((s) => s.cuenta?.correo)
  const [procesando, setProcesando] = useState(false)

  if (!MP_CONFIGURADO) {
    return (
      <div className="rounded-xl border border-yellow-200 bg-yellow-50 p-5 text-center text-sm text-yellow-800">
        <p className="font-semibold">MercadoPago no configurado</p>
        <p className="mt-1 text-xs">
          Definí <code className="rounded bg-yellow-100 px-1">VITE_CLAVE_PUBLICA_MP</code> en tu{" "}
          <code className="rounded bg-yellow-100 px-1">.env</code>.
        </p>
      </div>
    )
  }

  const manejarSubmit = async (formData: DatosFormMP) => {
    setProcesando(true)
    try {
      const resultado = await pagarConTarjetaMP({
        orden_id: ordenId,
        token: formData.token,
        payment_method_id: formData.payment_method_id,
        cuotas: Number(formData.installments ?? 1),
        issuer_id: formData.issuer_id,
        email_pagador: formData.payer?.email ?? correo ?? "",
      })

      if (resultado.estado === "approved") {
        onExito(resultado.id_pago_mp)
      } else if (resultado.estado === "rejected") {
        onError(`Pago rechazado: ${resultado.detalle ?? "intentá con otra tarjeta"}`)
      } else {
        onError(`Pago ${resultado.estado}: ${resultado.detalle ?? "esperá la confirmación"}`)
      }
    } catch (err: unknown) {
      onError(extraerMensajeError(err, "No se pudo procesar el pago"))
    } finally {
      setProcesando(false)
    }
  }

  return (
    <div className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
      <h2 className="mb-4 text-lg font-semibold">3. Pagá con tarjeta</h2>
      {procesando && (
        <p className="mb-3 text-center text-sm text-gray-500">Procesando pago...</p>
      )}
      <CardPayment
        initialization={{ amount: monto }}
        onSubmit={manejarSubmit}
        onReady={() => undefined}
        onError={(err) => onError(err?.message ?? "Error en el formulario de pago")}
      />
    </div>
  )
}
