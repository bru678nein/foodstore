const formateadorMoneda = new Intl.NumberFormat("es-AR", {
  style: "currency",
  currency: "ARS",
  minimumFractionDigits: 2,
})

export function formatearMoneda(valor: number | string): string {
  const n = Number(valor)
  return formateadorMoneda.format(Number.isFinite(n) ? n : 0)
}

export function formatearFecha(iso: string): string {
  if (!iso) return "-"
  const fecha = new Date(iso)
  if (Number.isNaN(fecha.getTime())) return iso
  return fecha.toLocaleString("es-AR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  })
}
