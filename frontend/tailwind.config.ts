import type { Config } from "tailwindcss"

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Nunito", "sans-serif"],
      },
      colors: {
        primario: {
          50:  "#fff8f0",
          100: "#ffecd6",
          200: "#ffd4a8",
          300: "#ffb870",
          400: "#ff9540",
          500: "#f97316",
          600: "#ea580c",
          700: "#c2410c",
        },
        calido: {
          50:  "#fdf8f0",
          100: "#faf0dc",
          200: "#f5e0b8",
          300: "#edcc8a",
          400: "#e4b55c",
          500: "#d4963a",
        },
        crema: {
          50:  "#fefdf9",
          100: "#fdf8ef",
          200: "#f9f0dc",
          300: "#f2e4c2",
        },
        secundario: {
          50:  "#ecfdf5",
          100: "#d1fae5",
          500: "#10b981",
          600: "#059669",
        },
        exito:      "#22c55e",
        advertencia:"#f59e0b",
        error:      "#ef4444",
      },
      borderRadius: {
        "2xl": "1rem",
        "3xl": "1.5rem",
      },
      boxShadow: {
        tarjeta: "0 2px 12px 0 rgba(180,100,30,0.08), 0 1px 3px 0 rgba(180,100,30,0.06)",
        "tarjeta-hover": "0 8px 28px 0 rgba(180,100,30,0.14), 0 2px 8px 0 rgba(180,100,30,0.08)",
        suave: "0 1px 6px 0 rgba(0,0,0,0.06)",
      },
    },
  },
  plugins: [],
} satisfies Config
