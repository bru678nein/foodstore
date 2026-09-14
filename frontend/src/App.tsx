import { RouterProvider } from "react-router-dom"
import { enrutadorApp } from "@/enrutador/EnrutadorApp"

export function App() {
  return <RouterProvider router={enrutadorApp} />
}
