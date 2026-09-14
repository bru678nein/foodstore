export type EstadoOrden =
  | "PENDIENTE"
  | "CONFIRMADO"
  | "EN_PREPARACION"
  | "ENTREGADO"
  | "CANCELADO"

export interface DomicilioBasico {
  id: number
  via: string
  altura: string
  localidad: string
  provincia: string
  codigo_postal?: string
}

export interface Domicilio extends DomicilioBasico {
  es_predeterminado: boolean
}

export interface EntradaDomicilio {
  via: string
  altura: string
  localidad: string
  provincia: string
  codigo_postal?: string
  es_predeterminado?: boolean
}

export interface RespuestaPartida {
  id: number
  titulo_capturado: string
  precio_capturado: number
  unidades: number
  importe_parcial: number
  componentes_excluidos: string[]
}

export interface EntradaBitacora {
  estado: EstadoOrden
  registrada_en: string
  nota?: string
}

export interface CobroBasico {
  id: number
  estado: string
  medio?: string
  preferencia_id?: string
  init_point?: string
}

export interface RespuestaOrden {
  id: number
  cuenta_id: number
  estado_actual: EstadoOrden
  tipo_entrega: TipoEntrega
  forma_pago_codigo: FormaPago
  total: number
  subtotal: number
  descuento: number
  costo_envio: number
  domicilio: DomicilioBasico | null
  partidas: RespuestaPartida[]
  bitacora: EntradaBitacora[]
  cobro: CobroBasico | null
  registrada_en: string
}

export interface PartidaNueva {
  articulo_id: number
  unidades: number
  componentes_excluidos: number[]
}

export type TipoEntrega = "DOMICILIO" | "LOCAL"
export type FormaPago = "MERCADOPAGO" | "MP_CARD" | "TARJETA" | "EFECTIVO"

export interface EntradaOrden {
  domicilio_id?: number
  tipo_entrega: TipoEntrega
  forma_pago_codigo: FormaPago
  partidas: PartidaNueva[]
}
