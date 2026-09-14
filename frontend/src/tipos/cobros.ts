export interface PreferenciaCobro {
  id_preferencia: string
  init_point: string
  cobro_id: number
}

export interface EstadoCobro {
  id: number
  orden_id: number
  estado_cobro: string
  monto: number
  medio?: string
  id_pago_mp?: string
  id_preferencia_mp?: string
}

export interface EntradaPreferencia {
  orden_id: number
}

export interface EntradaPagoDirecto {
  orden_id: number
  token: string
  payment_method_id: string
  cuotas?: number
  issuer_id?: string
  email_pagador?: string
}

export interface SalidaPagoDirecto {
  id_pago_mp: string
  estado: string
  detalle?: string
}
