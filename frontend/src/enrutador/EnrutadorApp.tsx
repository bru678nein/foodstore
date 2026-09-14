import { createBrowserRouter } from "react-router-dom"
import { DisposicionCliente } from "@/componentes/disposicion/DisposicionCliente"
import { DisposicionAdmin } from "@/componentes/disposicion/DisposicionAdmin"
import { RutaProtegida } from "@/componentes/comunes/RutaProtegida"

import { PaginaIngreso } from "@/paginas/PaginaIngreso"
import { PaginaRegistro } from "@/paginas/PaginaRegistro"
import { PaginaCatalogo } from "@/paginas/PaginaCatalogo"
import { PaginaDetalleArticulo } from "@/paginas/PaginaDetalleArticulo"
import { PaginaCarrito } from "@/paginas/PaginaCarrito"
import { PaginaPago } from "@/paginas/PaginaPago"
import { PaginaPagoExito } from "@/paginas/PaginaPagoExito"
import { PaginaPagoError } from "@/paginas/PaginaPagoError"
import { PaginaPagoPendiente } from "@/paginas/PaginaPagoPendiente"
import { PaginaMisOrdenes } from "@/paginas/PaginaMisOrdenes"
import { PaginaDetalleOrden } from "@/paginas/PaginaDetalleOrden"
import { PaginaPerfil } from "@/paginas/PaginaPerfil"
import { PaginaDomicilios } from "@/paginas/PaginaDomicilios"

import { PaginaTablero } from "@/paginas/admin/PaginaTablero"
import { PaginaGestionArticulos } from "@/paginas/admin/PaginaGestionArticulos"
import { PaginaGestionCategorias } from "@/paginas/admin/PaginaGestionCategorias"
import { PaginaGestionComponentes } from "@/paginas/admin/PaginaGestionComponentes"
import { PaginaGestionOrdenes } from "@/paginas/admin/PaginaGestionOrdenes"
import { PaginaGestionCuentas } from "@/paginas/admin/PaginaGestionCuentas"

export const enrutadorApp = createBrowserRouter([
    { path: "/ingresar", element: <PaginaIngreso /> },
  { path: "/registrarse", element: <PaginaRegistro /> },

    {
    element: <DisposicionCliente />,
    children: [
      { path: "/", element: <PaginaCatalogo /> },
      { path: "/articulos/:id", element: <PaginaDetalleArticulo /> },
      { path: "/carrito", element: <PaginaCarrito /> },
      {
        element: <RutaProtegida />,
        children: [
          { path: "/pago", element: <PaginaPago /> },
          { path: "/pago/exito", element: <PaginaPagoExito /> },
          { path: "/pago/error", element: <PaginaPagoError /> },
          { path: "/pago/pendiente", element: <PaginaPagoPendiente /> },
          { path: "/mis-ordenes", element: <PaginaMisOrdenes /> },
          { path: "/mis-ordenes/:id", element: <PaginaDetalleOrden /> },
          { path: "/perfil", element: <PaginaPerfil /> },
          { path: "/domicilios", element: <PaginaDomicilios /> },
        ],
      },
    ],
  },

    {
    element: <RutaProtegida perfilesRequeridos={["ADMINISTRADOR", "DESPACHO", "INVENTARIO"]} />,
    children: [
      {
        element: <DisposicionAdmin />,
        children: [
          {
            element: <RutaProtegida perfilesRequeridos={["ADMINISTRADOR"]} />,
            children: [
              { path: "/admin", element: <PaginaTablero /> },
              { path: "/admin/articulos", element: <PaginaGestionArticulos /> },
              { path: "/admin/categorias", element: <PaginaGestionCategorias /> },
              {
                path: "/admin/componentes",
                element: <PaginaGestionComponentes />,
              },
              { path: "/admin/cuentas", element: <PaginaGestionCuentas /> },
            ],
          },
          {
            element: (
              <RutaProtegida
                perfilesRequeridos={["ADMINISTRADOR", "DESPACHO"]}
              />
            ),
            children: [
              { path: "/admin/ordenes", element: <PaginaGestionOrdenes /> },
            ],
          },
        ],
      },
    ],
  },

    { path: "*", element: <PaginaCatalogo /> },
])
