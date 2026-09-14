export type Perfil =
  | "CLIENTE"
  | "ADMINISTRADOR"
  | "INVENTARIO"
  | "DESPACHO"

export interface CuentaBasica {
  id: number
  correo: string
  nombre_completo: string
  perfiles: string[]
}

export interface RespuestaToken {
  token_acceso: string
  token_renovacion: string
  tipo: string
  cuenta: CuentaBasica
}

export interface CredencialesIngreso {
  correo: string
  contrasena: string
}

export interface DatosRegistro {
  nombre_completo: string
  correo: string
  contrasena: string
}

export interface RespuestaRenovar {
  token_acceso: string
  token_renovacion?: string
}
