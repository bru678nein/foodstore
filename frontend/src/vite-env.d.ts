
interface ImportMetaEnv {
  readonly VITE_URL_API: string
  readonly VITE_URL_WS: string
  readonly VITE_CLAVE_PUBLICA_MP: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
