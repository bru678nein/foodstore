import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { UtensilsCrossed } from "lucide-react"
import { sesionStore } from "@/almacenes/sesionStore"
import { carritoStore } from "@/almacenes/carritoStore"
import { GuardiaRol } from "@/componentes/comunes/GuardiaRol"
import { cerrarSesionRemota } from "@/api/endpoints/sesion"

export function BarraNavegacion() {
  const navigate = useNavigate()
  const estaAutenticado = sesionStore((s) => s.estaAutenticado)
  const cuenta = sesionStore((s) => s.cuenta)
  const cerrarSesion = sesionStore((s) => s.cerrarSesion)
  const alternarCarrito = carritoStore((s) => s.alternarCarrito)
  const cantidad = carritoStore((s) => s.elementos.reduce((t, e) => t + e.cantidad, 0))
  const [abierto, setAbierto] = useState(false)

  const cerrar = () => setAbierto(false)

  const manejarCerrarSesion = async () => {
    try { await cerrarSesionRemota() } catch {  }
    cerrarSesion()
    cerrar()
    navigate("/")
  }

  return (
    <>
      <header className="sticky top-0 z-40 border-b border-crema-200 bg-crema-100/95 backdrop-blur">
        <div className="contenedor-pagina flex h-16 items-center justify-between">
            
          <div className="flex items-center gap-2">
            <button
              onClick={() => setAbierto((v) => !v)}
              className="rounded-xl p-2 text-gray-700 hover:bg-crema-200 transition-colors"
              aria-label={abierto ? "Cerrar menú" : "Abrir menú"}
            >
              {abierto ? (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              )}
            </button>

            <Link to="/" onClick={cerrar} className="flex items-center gap-2 group">
              <span className="flex h-9 w-9 items-center justify-center rounded-xl bg-primario-500 text-white shadow-sm transition-transform group-hover:scale-105">
                <UtensilsCrossed className="h-5 w-5" />
              </span>
              <span className="text-xl font-extrabold text-gray-900">
                Food<span className="text-primario-500">Store</span>
              </span>
            </Link>
          </div>

          
          <div className="flex items-center gap-1">
            
            <button
              onClick={alternarCarrito}
              className="relative rounded-xl p-2 text-gray-700 hover:bg-crema-200 transition-colors"
              aria-label="Carrito"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13l-1.5 6h13M7 13L5.4 5M10 21a1 1 0 100-2 1 1 0 000 2zm7 0a1 1 0 100-2 1 1 0 000 2z" />
              </svg>
              {cantidad > 0 && (
                <span className="absolute -right-0.5 -top-0.5 flex h-5 w-5 items-center justify-center rounded-full bg-primario-500 text-xs font-extrabold text-white shadow-sm">
                  {cantidad}
                </span>
              )}
            </button>

            </div>
        </div>
      </header>

      
      {abierto && (
        <div
          className="fixed inset-0 z-30 bg-black/30 backdrop-blur-sm"
          onClick={cerrar}
        />
      )}

      
      <aside
        className={`fixed left-0 top-0 z-50 flex h-full w-72 flex-col bg-white shadow-2xl transition-transform duration-300 ${
          abierto ? "translate-x-0" : "-translate-x-full"
        }`}
      >
        
        <div className="flex h-16 items-center justify-between border-b border-crema-200 bg-crema-50 px-5">
          <span className="font-extrabold text-gray-900">
            Food<span className="text-primario-500">Store</span>
          </span>
          <button
            onClick={cerrar}
            className="rounded-xl p-1.5 text-gray-500 hover:bg-crema-200 transition-colors"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        
        {estaAutenticado && cuenta && (
          <div className="border-b border-crema-100 bg-crema-50 px-5 py-4">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-primario-100 text-primario-700 font-extrabold text-base border border-primario-200">
                {cuenta.nombre_completo?.[0]?.toUpperCase() ?? "U"}
              </div>
              <div className="min-w-0">
                <p className="truncate text-sm font-bold text-gray-900">{cuenta.nombre_completo}</p>
                <p className="truncate text-xs text-gray-500">{cuenta.correo}</p>
              </div>
            </div>
          </div>
        )}

        
        <nav className="flex-1 overflow-y-auto py-3">
          <EnlaceMenu to="/" onClick={cerrar}>Catálogo</EnlaceMenu>

          {estaAutenticado && (
            <>
              <EnlaceMenu to="/mis-ordenes" onClick={cerrar}>Mis órdenes</EnlaceMenu>
              <EnlaceMenu to="/perfil" onClick={cerrar}>Mi perfil</EnlaceMenu>
              <EnlaceMenu to="/domicilios" onClick={cerrar}>Mis domicilios</EnlaceMenu>
            </>
          )}

          <GuardiaRol perfiles={["ADMINISTRADOR", "DESPACHO", "INVENTARIO"]}>
            <div className="mx-4 my-2 border-t border-crema-200" />
            <p className="px-5 pb-1 pt-2 text-xs font-semibold uppercase tracking-wide text-gray-400">
              Administración
            </p>
            <EnlaceMenu to="/admin" onClick={cerrar}>Tablero</EnlaceMenu>
            <EnlaceMenu to="/admin/articulos" onClick={cerrar}>Artículos</EnlaceMenu>
            <EnlaceMenu to="/admin/categorias" onClick={cerrar}>Categorías</EnlaceMenu>
            <EnlaceMenu to="/admin/componentes" onClick={cerrar}>Componentes</EnlaceMenu>
            <EnlaceMenu to="/admin/ordenes" onClick={cerrar}>Órdenes</EnlaceMenu>
            <EnlaceMenu to="/admin/cuentas" onClick={cerrar}>Cuentas</EnlaceMenu>
          </GuardiaRol>
        </nav>

        
        <div className="border-t border-crema-200 p-4">
          {estaAutenticado ? (
            <button
              onClick={manejarCerrarSesion}
              className="w-full rounded-xl border-2 border-red-200 px-4 py-2.5 text-sm font-semibold text-error transition-colors hover:bg-red-50"
            >
              Cerrar sesión
            </button>
          ) : (
            <div className="flex flex-col gap-2">
              <Link
                to="/ingresar"
                onClick={cerrar}
                className="block rounded-xl border-2 border-primario-300 px-4 py-2.5 text-center text-sm font-semibold text-primario-600 transition-colors hover:bg-primario-50"
              >
                Ingresar
              </Link>
              <Link
                to="/registrarse"
                onClick={cerrar}
                className="block rounded-xl bg-primario-500 px-4 py-2.5 text-center text-sm font-bold text-white shadow-sm transition-all hover:bg-primario-600 active:scale-95"
              >
                Registrarse
              </Link>
            </div>
          )}
        </div>
      </aside>
    </>
  )
}

function EnlaceMenu({ to, onClick, children }: { to: string; onClick: () => void; children: React.ReactNode }) {
  return (
    <Link
      to={to}
      onClick={onClick}
      className="block px-5 py-3 text-sm font-semibold text-gray-700 transition-colors hover:bg-crema-50 hover:text-primario-600"
    >
      {children}
    </Link>
  )
}
