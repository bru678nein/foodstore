import type { ReactNode } from "react"

interface PropsInsignia {
  children: ReactNode
  className?: string
}

export function Insignia({ children, className = "" }: PropsInsignia) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-bold ${className}`}
    >
      {children}
    </span>
  )
}
