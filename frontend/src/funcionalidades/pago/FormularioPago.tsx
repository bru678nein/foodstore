import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { Boton } from "@/componentes/ui/Boton"
import { SelectorDomicilio } from "./SelectorDomicilio"
import { BrickPago, BrickPagoCargando } from "./BrickPago"
import { CardPaymentMP } from "./CardPaymentMP"
import { ResumenCarrito } from "@/funcionalidades/carrito/ResumenCarrito"
import { ElementoCarrito } from "@/funcionalidades/carrito/ElementoCarrito"
import { useAccionesCarrito } from "@/funcionalidades/carrito/hooks/useAccionesCarrito"
import { useProcesarPago } from "./hooks/useProcesarPago"
import type { FormaPago, TipoEntrega } from "@/tipos/ordenes"

type Paso = "configurar" | "pagar"

const FORMAS_PAGO_LOCAL: { codigo: FormaPago; etiqueta: string; descripcion?: string }[] = [
  { codigo: "EFECTIVO", etiqueta: "Efectivo", descripcion: "Pagás al retirar en el local." },
  { codigo: "TARJETA", etiqueta: "Tarjeta", descripcion: "Pagás con tarjeta al retirar." },
  { codigo: "MERCADOPAGO", etiqueta: "Mercado Pago Checkout", descripcion: "Serás redirigido a Mercado Pago." },
  { codigo: "MP_CARD", etiqueta: "Tarjeta vía Mercado Pago", descripcion: "Pagás con tarjeta sin salir de la app." },
]

const FORMAS_PAGO_DOMICILIO: { codigo: FormaPago; etiqueta: string; descripcion?: string }[] = [
  { codigo: "TARJETA", etiqueta: "Tarjeta", descripcion: "Pagás con tarjeta al recibir el pedido." },
  { codigo: "MERCADOPAGO", etiqueta: "Mercado Pago Checkout", descripcion: "Serás redirigido a Mercado Pago." },
  { codigo: "MP_CARD", etiqueta: "Tarjeta vía Mercado Pago", descripcion: "Pagás con tarjeta sin salir de la app." },
]

export function FormularioPago() {
  const navigate = useNavigate()
  const { elementos, total, cantidadTotal } = useAccionesCarrito()
  const { confirmarPedido, procesando, error } = useProcesarPago()

  const [tipoEntrega, setTipoEntrega] = useState<TipoEntrega>("DOMICILIO")
  const [domicilioId, setDomicilioId] = useState<number | null>(null)
  const [formaPago, setFormaPago] = useState<FormaPago>("MERCADOPAGO")
  const [paso, setPaso] = useState<Paso>("configurar")
  const [preferenciaId, setPreferenciaId] = useState<string | null>(null)
  const [ordenId, setOrdenId] = useState<number | null>(null)
  const [totalOrden, setTotalOrden] = useState<number>(0)
  const [errorPago, setErrorPago] = useState<string | null>(null)

    const cambiarTipoEntrega = (tipo: TipoEntrega) => {
    setTipoEntrega(tipo)
    if (tipo === "DOMICILIO" && formaPago === "EFECTIVO") {
      setFormaPago("MERCADOPAGO")
    }
  }

  if (elementos.length === 0 && paso === "configurar") {
    return (
      <div className="flex flex-col items-center gap-3 py-16 text-center">
        <p className="text-lg font-medium">Tu carrito está vacío</p>
        <Boton onClick={() => navigate("/")}>Ver catálogo</Boton>
      </div>
    )
  }

  const manejarConfirmar = async () => {
    if (tipoEntrega === "DOMICILIO" && !domicilioId) return
    const resultado = await confirmarPedido({ domicilioId, tipoEntrega, formaPago })
    if (!resultado) return
    setOrdenId(resultado.ordenId)
    setTotalOrden(resultado.totalOrden)
    if (resultado.preferenciaId) {
      setPreferenciaId(resultado.preferenciaId)
    }
    setPaso("pagar")
  }

    if (paso === "pagar") {
    return (
      <div className="space-y-6">
        {errorPago && (
          <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-error">
            {errorPago}
            <button
              className="ml-3 underline underline-offset-2"
              onClick={() => setErrorPago(null)}
            >
              Reintentar
            </button>
          </div>
        )}
        {formaPago === "MP_CARD" && ordenId ? (
          <CardPaymentMP
            ordenId={ordenId}
            monto={totalOrden}
            onExito={(idPago) => navigate(`/pago/exito?external_reference=${ordenId}${idPago ? `&payment_id=${idPago}` : ""}`)}
            onError={(msg) => setErrorPago(msg)}
          />
        ) : procesando || !preferenciaId || !ordenId ? (
          <BrickPagoCargando />
        ) : (
          <BrickPago preferenciaId={preferenciaId} ordenId={ordenId} onError={(msg) => setErrorPago(msg)} />
        )}
        <div className="text-center">
          <button
            className="text-sm text-gray-400 underline underline-offset-2 hover:text-gray-600"
            onClick={() => navigate("/mis-ordenes")}
          >
            Ver mis pedidos
          </button>
        </div>
      </div>
    )
  }

  const opcionesPago =
    tipoEntrega === "LOCAL" ? FORMAS_PAGO_LOCAL : FORMAS_PAGO_DOMICILIO

  const puedeConfirmar =
    tipoEntrega === "LOCAL" || (tipoEntrega === "DOMICILIO" && domicilioId !== null)

  return (
    <div className="grid gap-6 lg:grid-cols-3">
      <div className="space-y-5 lg:col-span-2">

        
        <section className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
          <h2 className="mb-4 text-lg font-semibold">1. ¿Cómo recibís tu pedido?</h2>
          <div className="grid grid-cols-2 gap-3">
            {(
              [
                { valor: "DOMICILIO", texto: "Envío a domicilio" },
                { valor: "LOCAL", texto: "Retiro en local" },
              ] as { valor: TipoEntrega; texto: string }[]
            ).map(({ valor, texto }) => (
              <button
                key={valor}
                type="button"
                onClick={() => cambiarTipoEntrega(valor)}
                className={`rounded-xl border-2 p-4 text-sm font-medium transition ${
                  tipoEntrega === valor
                    ? "border-primario-500 bg-primario-50 text-primario-700"
                    : "border-gray-200 text-gray-500 hover:border-gray-300"
                }`}
              >
                {texto}
              </button>
            ))}
          </div>
        </section>

        
        {tipoEntrega === "DOMICILIO" && (
          <section className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
            <h2 className="mb-4 text-lg font-semibold">2. Domicilio de entrega</h2>
            <SelectorDomicilio
              domicilioSeleccionado={domicilioId}
              alSeleccionar={setDomicilioId}
            />
          </section>
        )}

        
        <section className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
          <h2 className="mb-4 text-lg font-semibold">
            {tipoEntrega === "LOCAL" ? "2." : "3."} Forma de pago
          </h2>
          <div className="flex flex-col gap-2">
            {opcionesPago.map(({ codigo, etiqueta, descripcion }) => (
              <button
                key={codigo}
                type="button"
                onClick={() => setFormaPago(codigo)}
                className={`rounded-xl border-2 px-4 py-3 text-left text-sm font-medium transition ${
                  formaPago === codigo
                    ? "border-primario-500 bg-primario-50 text-primario-700"
                    : "border-gray-200 text-gray-500 hover:border-gray-300"
                }`}
              >
                {etiqueta}
                {descripcion && (
                  <span className="block text-xs font-normal opacity-70">{descripcion}</span>
                )}
              </button>
            ))}
          </div>
        </section>

        
        <section className="rounded-xl border border-gray-100 bg-white p-5 shadow-sm">
          <h2 className="mb-2 text-lg font-semibold">Resumen del pedido</h2>
          <div className="divide-y divide-gray-100">
            {elementos.map((e) => (
              <ElementoCarrito key={e.articuloId} elemento={e} />
            ))}
          </div>
        </section>
      </div>

      
      <div className="space-y-4">
        <ResumenCarrito total={total} cantidad={cantidadTotal}>
          {tipoEntrega === "LOCAL" && (
            <p className="mb-2 text-center text-xs text-green-600 font-medium">
              Sin costo de envío
            </p>
          )}
          {error && (
            <p className="mb-3 rounded-lg bg-red-50 px-3 py-2 text-sm text-error">
              {error}
            </p>
          )}
          <Boton
            className="w-full"
            cargando={procesando}
            disabled={!puedeConfirmar || procesando}
            onClick={() => void manejarConfirmar()}
          >
            {formaPago === "MERCADOPAGO" || formaPago === "MP_CARD" ? "Ir a pagar" : "Confirmar pedido"}
          </Boton>
          {tipoEntrega === "DOMICILIO" && !domicilioId && (
            <p className="mt-2 text-center text-xs text-gray-400">
              Seleccioná un domicilio para continuar
            </p>
          )}
        </ResumenCarrito>
      </div>
    </div>
  )
}
