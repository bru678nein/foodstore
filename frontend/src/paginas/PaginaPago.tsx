import { FormularioPago } from "@/funcionalidades/pago/FormularioPago"

export function PaginaPago() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Finalizar compra</h1>
      <FormularioPago />
    </div>
  )
}
