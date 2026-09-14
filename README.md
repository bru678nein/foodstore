# Food Store

Sistema full-stack de gestión de pedidos de comida. Catálogo, carrito, pago con
MercadoPago, seguimiento de pedidos en tiempo real (WebSocket) y panel de
administración con métricas.

> **Stack:** React 18 + TypeScript + Vite + Tailwind · FastAPI + SQLModel + PostgreSQL · WebSocket · Cloudinary · MercadoPago

---

## Requisitos previos

| Herramienta | Versión | Para qué |
|---|---|---|
| Python | 3.11+ | Backend FastAPI |
| Node.js | 18+ | Frontend Vite |
| PostgreSQL | 15+ | Base de datos (o usar Docker) |
| Docker + Docker Compose | — | Alternativa para levantar BD + backend |
| ngrok | — | Exponer el backend para el webhook de MercadoPago |
| Cuenta Cloudinary | — | Almacenamiento de imágenes ([console.cloudinary.com](https://console.cloudinary.com/)) |
| Cuenta MercadoPago Developers | — | Pasarela de pagos ([developers](https://www.mercadopago.com.ar/developers/panel/app)) |

---

## Estructura del repo

```
foodstoreracconto/
├── backend/        # FastAPI + SQLModel + PostgreSQL
│   ├── app/
│   │   ├── modulos/        # Features: sesion, cuentas, domicilios, rubros,
│   │   │                   #           articulos, componentes, ordenes, cobros,
│   │   │                   #           archivos, metricas, tiempo_real
│   │   ├── nucleo/         # Config, dependencias, seguridad, rate limiting
│   │   └── persistencia/   # Entidades SQLModel, Unit of Work, seed
│   ├── pruebas/            # Tests con pytest + TestClient
│   ├── migraciones/        # Alembic
│   ├── requisitos.txt
│   ├── .env.example        # Plantilla de variables del backend
│   └── docker-compose.yml
└── frontend/       # React + TypeScript + Vite
    ├── src/        # paginas, funcionalidades, componentes, hooks, almacenes, api, lib, tipos
    └── .env.example        # Plantilla de variables del frontend
```

---

## Puesta en marcha — Backend

### Opción A — Local (sin Docker)

```bash
cd backend

# 1. Entorno virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Dependencias
pip install -r requisitos.txt

# 3. Variables de entorno
cp .env.example .env             # Windows: copy .env.example .env
#    Editá backend/.env con tus credenciales (ver tabla más abajo)

# 4. Base de datos PostgreSQL corriendo y accesible según DATABASE_URL
#    El esquema y el seed se crean automáticamente al arrancar la app.

# 5. Levantar la API
uvicorn app.principal:aplicacion --host 0.0.0.0 --port 8000 --reload
#    o, equivalente:
bash ejecutar.sh
```

La API queda en `http://localhost:8000`. Documentación interactiva:
- Swagger UI → http://localhost:8000/docs
- ReDoc → http://localhost:8000/redoc

### Opción B — Docker Compose (BD + backend)

```bash
cd backend
cp .env.example .env             # completá las credenciales
docker-compose up --build
```

Levanta PostgreSQL (`base_datos`) y la API (`servidor`) en el puerto 8000.

### Migraciones (Alembic)

Al arrancar, la app crea las tablas y el seed automáticamente. Si preferís
gestionar el esquema con migraciones:

```bash
cd backend
alembic revision --autogenerate -m "descripcion"
alembic upgrade head
```

### Seed / usuario administrador

Al primer arranque se crean los perfiles base (`ADMINISTRADOR`, `INVENTARIO`,
`DESPACHO`, `COMPRADOR`) y una cuenta administradora:

```
Email:    admin@foodstore.com
Password: Admin1234!
```

> ⚠️ Cambiá esta contraseña en producción.

---

## Puesta en marcha — Frontend

```bash
cd frontend

# 1. Dependencias
npm install

# 2. Variables de entorno
cp .env.example .env             # Windows: copy .env.example .env
#    Editá frontend/.env (VITE_URL_API y VITE_URL_WS)

# 3. Dev server
npm run dev                      # http://localhost:5173
```

Build de producción:

```bash
npm run build      # chequeo de tipos (tsc) + build de Vite
npm run preview    # previsualizar el build
```

---

## Webhook de MercadoPago con ngrok

MercadoPago necesita una URL pública (HTTPS) para notificar el resultado de los
pagos al endpoint `POST /api/v1/cobros/webhook`. En desarrollo se expone el
backend con ngrok:

```bash
# Una sola vez: configurá tu authtoken de ngrok
ngrok config add-authtoken <tu-authtoken>

# Exponer el backend (puerto 8000)
ngrok http 8000
```

Copiá la URL pública que genera ngrok (ej. `https://abc123.ngrok-free.app`) y
cargala en el panel de MercadoPago → **Webhooks**, apuntando a:

```
https://<tu-subdominio>.ngrok-free.app/api/v1/cobros/webhook
```

---

## Variables de entorno

### Backend — `backend/.env` (ver `backend/.env.example`)

| Variable | Descripción |
|---|---|
| `DATABASE_URL` | Conexión a PostgreSQL |
| `CLAVE_SECRETA` | Clave para firmar el JWT (mín. 32 caracteres) |
| `ALGORITMO` / `MINUTOS_ACCESO` / `DIAS_RENOVACION` | Parámetros del JWT |
| `ORIGENES_CORS` | Orígenes permitidos por CORS, separados por coma |
| `NUBE_CDN` / `API_KEY_CDN` / `API_SECRET_CDN` | Credenciales de Cloudinary (backend) |
| `TAMANIO_MAXIMO_MB` | Tamaño máximo de imagen subida |
| `TOKEN_MP` | Access Token de MercadoPago (backend) |
| `CLAVE_PUBLICA_MP` | Public Key de MercadoPago (también la usa el frontend) |
| `SECRETO_WEBHOOK_MP` | Secreto para validar la firma del webhook |
| `URL_PUBLICA_BACKEND` | URL pública de ngrok para el webhook (uso operativo) |

### Frontend — `frontend/.env` (ver `frontend/.env.example`)

| Variable | Descripción |
|---|---|
| `VITE_URL_API` | URL base del backend (ej. `http://localhost:8000`) |
| `VITE_URL_WS` | URL del WebSocket (ej. `ws://localhost:8000`) |
| `VITE_CLAVE_PUBLICA_MP` | Public Key de MercadoPago para el checkout (pendiente de integración) |

> Las credenciales de Cloudinary y MercadoPago se obtienen en sus respectivos
> paneles. Usá las credenciales de **prueba** (`TEST-...`) de MercadoPago para
> el entorno sandbox.

---

## Tests

```bash
cd backend
pytest                              # toda la suite
pytest pruebas/test_ordenes.py      # un archivo
pytest -k "test_crear_orden"        # un test por nombre
```

Los tests usan una base SQLite aislada (no PostgreSQL) y el rate limiting está
desactivado en el entorno de pruebas.

---

## Roles (RBAC)

| Perfil | Permisos |
|---|---|
| `ADMINISTRADOR` | Acceso total: cuentas, catálogo, pedidos, stock |
| `INVENTARIO` | Gestión de stock y componentes |
| `DESPACHO` | Avance de estados de pedidos |
| `COMPRADOR` | Catálogo, carrito, pedidos propios |
