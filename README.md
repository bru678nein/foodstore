<div align="center">

# 🍔 Food Store

**A full-stack food ordering platform with a customer storefront, MercadoPago checkout, real-time order tracking over WebSockets, and a back office with analytics.**

![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-5-646CFF?logo=vite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3-06B6D4?logo=tailwindcss&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)
![SQLModel](https://img.shields.io/badge/SQLModel-ORM-7E56C2)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)
![MercadoPago](https://img.shields.io/badge/MercadoPago-payments-00B1EA?logo=mercadopago&logoColor=white)
![Cloudinary](https://img.shields.io/badge/Cloudinary-media-3448C5?logo=cloudinary&logoColor=white)

![Food Store catalog](docs/screenshots/01-catalog.png)

</div>

> [!NOTE]
> **Recovered project.** I originally built this project under a GitHub account I no longer have access to. I recovered it and re-uploaded it here, so the commit history starts from the re-upload.

## Contents

- [Overview](#overview)
- [Features](#features)
- [Screenshots](#screenshots)
- [Tech stack](#tech-stack)
- [Architecture](#architecture)
- [Domain model](#domain-model)
- [Order lifecycle](#order-lifecycle)
- [Authentication and authorization](#authentication-and-authorization)
- [Payments with MercadoPago](#payments-with-mercadopago)
- [Real-time updates](#real-time-updates)
- [Getting started](#getting-started)
- [Environment variables](#environment-variables)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Project structure](#project-structure)

---

## Overview

Food Store covers the whole lifecycle of a food order. A customer browses the catalog and builds a cart. They check out with delivery or pickup and pay through MercadoPago. Then they follow the order live while staff move it through the kitchen. Staff manage the catalog, stock, accounts, and orders from a role-based back office with a metrics dashboard.

It is a monorepo with two independent applications:

| App | Path | Stack |
|---|---|---|
| REST + WebSocket API | [`backend/`](backend) | Python, FastAPI, SQLModel, PostgreSQL |
| Single-page application | [`frontend/`](frontend) | React, TypeScript, Vite, Tailwind CSS |

Four roles exist: **COMPRADOR** (customer), **ADMINISTRADOR** (administrator), **DESPACHO** (dispatch), and **INVENTARIO** (inventory).

> [!NOTE]
> **Naming convention.** Domain code, routes, and UI copy are written in Spanish. This glossary maps the terms you'll see in the codebase:
>
> | Spanish | English | | Spanish | English |
> |---|---|---|---|---|
> | `articulo` | product | | `cuenta` / `perfil` | account / role |
> | `categoria` | category | | `domicilio` | address |
> | `componente` | ingredient | | `sesion` | auth session |
> | `orden` / `partida` | order / line item | | `tiempo_real` | real time |
> | `cobro` | payment | | `metricas` | metrics |
> | `enrutador` / `servicio` / `repositorio` / `esquemas` | router / service / repository / schemas | | `almacenes` / `funcionalidades` / `paginas` | stores / features / pages |

---

## Features

**Storefront**
- Catalog with nested categories, category filters, a debounced search (400 ms), and pagination.
- Product detail page with a gallery and the ingredient list, which marks each ingredient as fixed or removable.
- Cart that persists across reloads and sessions (`localStorage`).
- Responsive layout down to phone widths.

**Checkout and payments**
- Delivery to a saved address, or pickup at the store.
- Four payment methods:

  | Method | How it works |
  |---|---|
  | Cash | Pickup orders only |
  | Card on delivery | Paid when the order arrives |
  | MercadoPago Checkout Pro | The customer is redirected to MercadoPago to pay |
  | Card Payment Brick | The customer pays by card inside the app |

- Stock is reserved when an order is created and returned if the order is cancelled.

**Live order tracking**
- The order detail page shows a **Live** indicator and updates over WebSocket. You don't need to refresh.
- A timeline of every state change, built from a server-side audit log.

**Back office**
- Dashboard with KPIs (sales today and this month, average ticket, active orders) and four charts.
- Kanban board of orders by state. Each state change is checked against a state machine.
- Management of products, categories (as a tree), ingredients (with stock and an allergen flag), accounts, and roles.

**Security**
- Short-lived JWT access tokens.
- Revocable refresh tokens stored on the server.
- bcrypt password hashing.
- Role checks enforced on the server.
- Rate-limited login and registration.
- HMAC-verified payment webhooks.

---

## Screenshots

> Taken with the demo dataset from [`seed_demo.py`](backend/seed_demo.py). Product photos come from Unsplash.

### Storefront

| Product detail | Cart |
|---|---|
| ![Product detail with removable ingredients](docs/screenshots/02-product-detail.png) | ![Cart with order summary](docs/screenshots/03-cart.png) |

### Checkout and tracking

| Checkout | My orders |
|---|---|
| ![Checkout: delivery, address and payment method](docs/screenshots/04-checkout.png) | ![Customer order history](docs/screenshots/05-my-orders.png) |

| Live order tracking | Mobile |
|---|---|
| ![Order detail with live indicator and state timeline](docs/screenshots/06-order-tracking.png) | <img src="docs/screenshots/11-mobile-catalog.png" alt="Mobile catalog" width="280"> |

### Back office

![Admin dashboard with KPIs and charts](docs/screenshots/07-admin-dashboard.png)

| Order board (Kanban) | Product management |
|---|---|
| ![Orders grouped by state with transition actions](docs/screenshots/08-admin-orders.png) | ![Product table with inline stock editing](docs/screenshots/09-admin-products.png) |

### API

![Interactive OpenAPI documentation](docs/screenshots/10-api-docs.png)

---

## Tech stack

### Frontend

| Technology | Version | Role in this project |
|---|---|---|
| [React](https://react.dev) | 18.3 | UI library. Built from function components and hooks. |
| [TypeScript](https://www.typescriptlang.org) | 5.x (strict) | Types shared across the API layer, stores, and components. `npm run build` runs `tsc -b` before bundling, so type errors fail the build. |
| [Vite](https://vitejs.dev) | 5.4 | Dev server with hot reload, and the production bundler. Configures the `@/` → `src/` import alias. |
| [Tailwind CSS](https://tailwindcss.com) | 3.4 | Styling with utility classes. A custom theme sets the colours (`primario` orange, `calido`, `crema`, `secundario`) and the Nunito font. |
| [React Router](https://reactrouter.com) | 6 | Routing with `createBrowserRouter`: nested layouts for the customer and admin areas, and route guards per role. |
| [TanStack Query](https://tanstack.com/query) | 5 | **Server state.** Caches API data (5-minute stale time) and builds query keys from one factory ([`lib/clavesConsulta.ts`](frontend/src/lib/clavesConsulta.ts)). Cancelling an order updates the screen before the server replies (optimistic update). |
| [Zustand](https://zustand.docs.pmnd.rs) | 4.5 | **Client state.** Holds the session, the cart (saved with `persist`), the WebSocket connection, the payment state, the UI state, and toasts. |
| [Axios](https://axios-http.com) | 1.x | HTTP client. Its interceptors add the bearer token and refresh an expired token without the user noticing. |
| [Recharts](https://recharts.org) | 2.15 | Dashboard charts: line, pie, and bar. |
| [MercadoPago SDK React](https://github.com/mercadopago/sdk-react) | 1.0 | Two payment widgets: the `Wallet` button (Checkout Pro) and the `CardPayment` brick. |
| [Lucide](https://lucide.dev) | — | Icons. |

> **Why split server state and client state?** Data that belongs to the backend (products, orders, metrics) lives in TanStack Query, which handles caching, refetching, and invalidation. Zustand only holds data that exists solely in the browser, such as the cart or the open socket. This keeps each store small and avoids stale copies of server data.

### Backend

| Technology | Version | Role in this project |
|---|---|---|
| [FastAPI](https://fastapi.tiangolo.com) | ≥ 0.115 | ASGI web framework. Supplies dependency injection (`Depends`), request validation, native WebSockets, and generated OpenAPI docs at `/docs` and `/redoc`. |
| [Uvicorn](https://www.uvicorn.org) | ≥ 0.30 | ASGI server. |
| [SQLModel](https://sqlmodel.tiangolo.com) | ≥ 0.0.21 | ORM that combines SQLAlchemy and Pydantic. The same classes define the database tables and validate data. |
| [PostgreSQL](https://www.postgresql.org) | 16 | Main database, run from the `postgres:16` image in Docker Compose. Connected through `psycopg2`. |
| [Alembic](https://alembic.sqlalchemy.org) | ≥ 1.13 | Database migrations in [`migraciones/`](backend/migraciones). |
| [Pydantic v2](https://docs.pydantic.dev) + pydantic-settings | ≥ 2.4 | Request and response models, and typed settings loaded from environment variables. |
| [python-jose](https://github.com/mpdavis/python-jose) | ≥ 3.3 | Signs and verifies JWTs (HS256). |
| [passlib](https://passlib.readthedocs.io) + bcrypt | 1.7.4 / 4.0 | Password hashing. `bcrypt` is pinned below 4.1 because passlib 1.7.4 doesn't support newer versions. |
| [SlowAPI](https://slowapi.readthedocs.io) | ≥ 0.1.9 | Rate limiting per client IP. |
| [Cloudinary SDK](https://cloudinary.com/documentation/python_integration) | ≥ 1.40 | Image storage. Uploads are signed on the server. |
| [MercadoPago SDK](https://github.com/mercadopago/sdk-python) | ≥ 2.2 | Creates payment preferences and payments, and looks up payments for the webhook. |
| [pytest](https://pytest.org) + httpx `TestClient` + pytest-cov | ≥ 8.3 | API tests with a coverage gate. |

### Infrastructure

- **Docker Compose** runs PostgreSQL 16 and the API. The API image is built from `python:3.12-slim`.
- **ngrok** gives the local API a public HTTPS URL, so MercadoPago can reach the webhook during development.
- **No third-party credentials are needed to run the app.** Without them, Cloudinary and MercadoPago switch to simulated responses, so you can run the whole app locally.

---

## Architecture

### System overview

```mermaid
flowchart LR
    subgraph Browser["Browser · React SPA"]
        UI["Pages & features"]
        RQ["TanStack Query<br/>(server state)"]
        ZS["Zustand<br/>(client state)"]
    end

    subgraph API["FastAPI · Uvicorn"]
        REST["REST API<br/>/api/v1"]
        WS["WebSocket<br/>/ws/{channel}"]
    end

    DB[("PostgreSQL")]
    CDN["Cloudinary"]
    MP["MercadoPago"]

    UI --> RQ
    UI --> ZS
    RQ -- "Axios + JWT" --> REST
    ZS <-- "live events" --> WS
    REST --> DB
    REST -- "signed uploads" --> CDN
    REST -- "preferences / payments" --> MP
    MP -- "webhook (HMAC-signed)" --> REST
    REST -. "broadcast" .-> WS
```

### Backend: modular, layered design

The backend is split into feature modules under [`backend/app/modulos/`](backend/app/modulos). Each module holds its whole stack, from the HTTP route down to the database queries:

```
modulos/ordenes/
├── enrutador.py        # HTTP layer: FastAPI router, auth dependencies, DI factory
├── servicio.py         # Business rules: validation, stock, state transitions
├── repositorio.py      # Data access: SQLModel queries
├── esquemas.py         # Pydantic DTOs — the API contract
└── maquina_estados.py  # Module-specific domain logic (order state machine)
```

A request passes through **router → service → repository → database session**. Cross-cutting concerns live outside the modules:

| Package | Responsibility |
|---|---|
| [`nucleo/`](backend/app/nucleo) | Settings (`ajustes.py`), auth dependencies (`dependencias.py`), hashing and JWT (`proteccion.py`), rate limiter (`limitador.py`) |
| [`persistencia/`](backend/app/persistencia) | Database engine, Unit of Work, base repository, entities, startup seed |

**Main patterns**

- **Unit of Work.** `GestorTransaccion` wraps one SQLModel session per request. Repositories only *flush* changes. The Unit of Work *commits* when the handler succeeds and *rolls back* on any exception, so one request is one transaction. Endpoints that also send WebSocket events commit first, so clients never see data that isn't saved yet.
- **Dependency injection.** Each router gets its service from a `Depends(obtener_servicio)` factory. Tests can replace any layer without patching imports.
- **Soft delete.** Accounts, products, categories, ingredients, and addresses get an `eliminado_en` timestamp instead of being deleted, so order history stays consistent.
- **Price snapshots.** Each order line copies the product title and unit price at purchase time. Later catalog changes never change past orders.
- **Startup bootstrap.** When the app starts, its lifespan hook creates any missing tables and seeds the lookup data (roles, order states, payment methods, units) and the admin account. It is safe to run on every start.

### Frontend: feature-based structure

```
frontend/src/
├── paginas/           # Route-level pages — thin containers
├── funcionalidades/   # Feature modules: components + React Query hooks
│   ├── catalogo/  carrito/  pago/  ordenes/  perfil/  sesion/
│   └── admin/{articulos,cuentas,ordenes,tablero}
├── componentes/
│   ├── ui/            # Design-system primitives (Boton, Modal, CampoTexto, Paginacion…)
│   ├── comunes/       # Route guards, image uploader, status badges
│   └── disposicion/   # Customer and admin layouts, navigation drawer
├── almacenes/         # Zustand stores
├── api/               # Axios client + one endpoint file per backend module
├── hooks/             # useConexionWS, useDebounce, useAlmacenLocal
├── enrutador/         # Route table
├── lib/               # Query keys, formatters, MercadoPago setup
└── tipos/             # Shared TypeScript types
```

- **Container/presentational split.** Pages and feature hooks load and change data. Feature components mostly receive props and render them.
- **Silent token refresh.** When a request gets `401`, the Axios interceptor starts **one** refresh call to `/sesion/renovar`. Other requests that fail at the same time wait for it, then each retries once. If the refresh fails, the session is cleared and the user is sent to the login page.
- **Guards.** `RutaProtegida` protects routes: it sends logged-out users to login and users without the right role back to the home page. `GuardiaRol` shows or hides parts of the UI by role.

---

## Domain model

```mermaid
erDiagram
    CUENTA ||--o{ CUENTA_PERFIL : has
    PERFIL ||--o{ CUENTA_PERFIL : grants
    CUENTA ||--o{ TOKEN_RENOVACION : owns
    CUENTA ||--o{ DOMICILIO : owns
    CUENTA ||--o{ ORDEN : places
    DOMICILIO |o--o{ ORDEN : "delivered to"
    CATEGORIA |o--o{ CATEGORIA : "parent of"
    CATEGORIA ||--o{ ARTICULO_CATEGORIA : classifies
    ARTICULO ||--o{ ARTICULO_CATEGORIA : "belongs to"
    ARTICULO ||--o{ ARTICULO_IMAGEN : gallery
    ARTICULO ||--o{ COMPOSICION_ARTICULO : "made of"
    COMPONENTE ||--o{ COMPOSICION_ARTICULO : "used in"
    ORDEN ||--|{ PARTIDA_ORDEN : contains
    ARTICULO |o--o{ PARTIDA_ORDEN : "snapshot of"
    ORDEN ||--o{ BITACORA_ORDEN : "audit trail"
    ORDEN ||--o| COBRO : "paid by"
```

- **Products and ingredients** are linked through `COMPOSICION_ARTICULO`. Each link stores a quantity and whether the ingredient can be removed. Creating an order takes stock from the product and from every ingredient (quantity × units).
- **Categories** reference themselves through `padre_id`, which lets them form a tree of any depth. A category that still has children can't be deleted.
- **Lookup tables** (`PERFIL`, `ESTADO_PEDIDO`, `FORMA_PAGO`, `UNIDAD_MEDIDA`) are seeded when the app starts.

---

## Order lifecycle

Order state changes go through an explicit state machine ([`maquina_estados.py`](backend/app/modulos/ordenes/maquina_estados.py)). An invalid change returns `409 Conflict`.

```mermaid
stateDiagram-v2
    [*] --> PENDIENTE: order created · stock reserved
    PENDIENTE --> CONFIRMADO: payment approved or staff
    PENDIENTE --> CANCELADO: customer or staff · stock restored
    CONFIRMADO --> EN_PREPARACION: staff
    CONFIRMADO --> CANCELADO: staff · stock restored
    EN_PREPARACION --> ENTREGADO: staff
    EN_PREPARACION --> CANCELADO: staff
    ENTREGADO --> [*]
    CANCELADO --> [*]
```

- *Staff* means `ADMINISTRADOR` or `DESPACHO`. Customers can only cancel their own orders, and only while the order is `PENDIENTE`.
- Every change adds a row to `BITACORA_ORDEN` (who, when, from → to) and sends a WebSocket event.
- Business rules:
  - Delivery orders need an address that belongs to the customer.
  - Cash is only accepted for pickup.
  - Stock is checked before any stock is taken; not enough stock returns `409`.

---

## Authentication and authorization

```mermaid
sequenceDiagram
    participant C as Client
    participant A as API
    participant D as Database

    C->>A: POST /sesion/iniciar {correo, contrasena}
    A->>D: verify bcrypt hash
    A-->>C: access JWT (30 min) + refresh token (7 days)
    C->>A: GET /ordenes/mis-ordenes (Bearer JWT)
    A->>D: load account + roles
    A-->>C: 200 OK
    Note over C,A: access token expires
    C->>A: POST /sesion/renovar {token_renovacion}
    A->>D: check token exists, not revoked, not expired
    A-->>C: new access JWT
```

- **Access token.** A JWT signed with HS256. It carries the account id, email, and roles.
- **Refresh token.** Not a JWT. It is a random 64-byte URL-safe string stored in the `token_renovacion` table, so the server can revoke it (logout does this).
- **Authorization** is done by the `requerir_perfil(...)` dependency. It reloads the account's roles from the database on every request instead of trusting the JWT claims, so a role change takes effect right away.
- **Rate limiting.** Login and registration allow 5 requests per 15 minutes per IP. Going over returns `429`.

| Capability | COMPRADOR | DESPACHO | INVENTARIO | ADMINISTRADOR |
|---|:---:|:---:|:---:|:---:|
| Browse catalog | ✅ | ✅ | ✅ | ✅ |
| Place and cancel own orders, pay | ✅ | | | ✅ |
| View all orders, change order state | | ✅ | | ✅ |
| Manage ingredients, update stock | | | ✅ | ✅ |
| Manage products, categories, accounts, uploads | | | | ✅ |
| Metrics dashboard | | | | ✅ |

---

## Payments with MercadoPago

The integration lives in [`modulos/cobros/`](backend/app/modulos/cobros) and supports two flows.

### Checkout Pro (redirect) + webhook

```mermaid
sequenceDiagram
    actor U as Customer
    participant W as React SPA
    participant A as FastAPI
    participant M as MercadoPago

    U->>W: Confirm checkout
    W->>A: POST /ordenes
    A-->>W: order PENDIENTE (stock reserved)
    W->>A: POST /cobros/preferencia {orden_id}
    A->>M: create preference (external_reference = order id)
    M-->>A: preference id
    A-->>W: preference id
    W->>M: Wallet brick → redirect to Checkout Pro
    U->>M: pays
    M->>A: POST /cobros/webhook (x-signature, x-request-id)
    A->>A: verify HMAC-SHA256 signature
    A->>M: fetch payment by id
    A->>A: update COBRO · PENDIENTE → CONFIRMADO
    A-->>W: WebSocket "pago_aprobado"
```

**Webhook signature check.** The API rebuilds the signed message as `id:{data.id};request-id:{x-request-id};ts:{ts};`. It computes an HMAC-SHA256 of that message with `SECRETO_WEBHOOK_MP` and compares the result with the `v1` value from the `x-signature` header using `hmac.compare_digest`, which takes the same time whether or not the values match. A missing or wrong signature returns `401`.

> [!WARNING]
> If `SECRETO_WEBHOOK_MP` is empty, the signature check is skipped. That is convenient for local development. Always set it in production.

### Card Payment Brick (in-app)

The `CardPayment` brick turns the card details into a token inside the browser, so the raw card number never reaches our servers. The frontend sends that token to `POST /cobros/pago-directo`, and the API creates the payment through the MercadoPago SDK. If the payment is approved, the order moves to `CONFIRMADO` straight away.

---

## Real-time updates

Endpoint: `ws://<host>/ws/{channel}?token=<access JWT>`. An invalid or expired token closes the socket with code `1008`.

| Channel | Subscribed by | Events |
|---|---|---|
| `ordenes` | Admin order board, catalog stock | `orden_creada`, `orden_actualizada`, `orden_cancelada`, `pago_aprobado`, `articulo_actualizado` |
| `orden:{id}` | Order detail page | Order events for that order |
| `cuenta:{id}` | Customer's order list | Order events for that customer |

**The client treats events as signals to refetch.** The REST API is the only source of truth. When an event arrives, the client invalidates the related TanStack Query caches, and the data is fetched again over REST. Events therefore stay small, and the client can't get out of sync with the server.

**Reconnection.** One shared socket lives in a Zustand store ([`almacenes/conexionStore.ts`](frontend/src/almacenes/conexionStore.ts)). If it drops, the store reconnects with exponential backoff: the wait starts at 1 s, grows up to 30 s, varies by ±25% at random, and stops after 8 attempts. It also reconnects when the tab becomes visible again.

> [!NOTE]
> The server keeps its list of connected sockets in memory, so live updates only work with a single API process. To run more instances, you would need a shared pub/sub broker such as Redis.

---

## Getting started

### Prerequisites

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.11+ (3.12 recommended) | Backend |
| Node.js | 18+ | Frontend |
| PostgreSQL | 15+ | Database. You can use Docker instead of a local install. |
| Docker + Docker Compose | — | *Optional:* runs the database and the API in containers |
| ngrok | — | *Optional:* public URL for the MercadoPago webhook |
| Cloudinary account | — | *Optional:* image uploads ([console](https://console.cloudinary.com/)) |
| MercadoPago developer account | — | *Optional:* real payments ([dashboard](https://www.mercadopago.com.ar/developers/panel/app)) |

### 1. Clone

```bash
git clone https://github.com/bru678nein/foodstore.git
cd foodstore
```

### 2. Backend

**Option A: Docker Compose.** This starts PostgreSQL and the API.

```bash
cd backend
cp .env.example .env        # fill in credentials (optional)
docker compose up --build
```

**Option B: run it locally.**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requisitos.txt
cp .env.example ../.env      # see note below
uvicorn app.principal:aplicacion --reload --port 8000
```

> [!IMPORTANT]
> **Where the `.env` file goes.** When you run the API locally, settings are read from a `.env` file at the **repository root**, because [`ajustes.py`](backend/app/nucleo/ajustes.py) looks for it there. Docker Compose reads `backend/.env` instead. Every setting has a default, so the API starts without any `.env` file, as long as PostgreSQL is reachable at the default `DATABASE_URL`.

The API runs at `http://localhost:8000`. Interactive docs are at [`/docs`](http://localhost:8000/docs) (Swagger UI) and [`/redoc`](http://localhost:8000/redoc).

### 3. Demo data (optional)

When it first starts, the API creates the lookup tables and one admin account. To fill the app with a full demo catalog (36 products, 42 ingredients, 19 categories), extra accounts, and orders in every state:

```bash
cd backend
python seed_demo.py
```

> [!CAUTION]
> `seed_demo.py` runs `DROP SCHEMA public CASCADE` before it seeds, which **deletes everything** in the target database. Always point `DATABASE_URL` at a database you can throw away.

To attach product photos, run `python -X utf8 seed_imagenes.py`. It uploads the photos to Cloudinary, so it needs Cloudinary credentials.

| Account | Password | Role |
|---|---|---|
| `admin@foodstore.com` | `Admin1234!` | ADMINISTRADOR (always created) |
| `despacho@foodstore.com` | `Despacho1!` | DESPACHO |
| `inventario@foodstore.com` | `Inventario1!` | INVENTARIO |
| `comprador@foodstore.com` | `Comprador1!` | COMPRADOR, with 5 orders |

> [!WARNING]
> Change the admin password before deploying anywhere public.

### 4. Frontend

```bash
cd frontend
npm install
cp .env.example .env         # VITE_URL_API, VITE_URL_WS, VITE_CLAVE_PUBLICA_MP
npm run dev                  # http://localhost:5173
```

Production build:

```bash
npm run build                # type-check (tsc -b) + Vite build
npm run preview              # serve the build locally
```

### 5. MercadoPago webhook with ngrok (optional)

MercadoPago sends payment results to a public HTTPS URL. To receive them during local development, expose the API with ngrok:

```bash
ngrok config add-authtoken <your-authtoken>   # once
ngrok http 8000
```

In the MercadoPago dashboard, go to **Webhooks** and register:

```
https://<your-subdomain>.ngrok-free.app/api/v1/cobros/webhook
```

Set `URL_API` to the ngrok URL so that new payment preferences include it as their `notification_url`. Use MercadoPago's **test** credentials (`TEST-...`) for the sandbox.

---

## Environment variables

<details>
<summary><strong>Backend</strong> (template: <a href="backend/.env.example"><code>backend/.env.example</code></a>)</summary>

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql://postgres:postgres@localhost:5432/foodstore_new` | PostgreSQL connection string |
| `CLAVE_SECRETA` | development placeholder | JWT signing key, at least 32 characters. **Change it in production.** |
| `ALGORITMO` | `HS256` | JWT algorithm |
| `MINUTOS_ACCESO` | `30` | How long an access token lasts, in minutes |
| `DIAS_RENOVACION` | `7` | How long a refresh token lasts, in days |
| `ORIGENES_CORS` | `http://localhost:5173,http://localhost:3000` | Origins allowed by CORS, separated by commas |
| `URL_FRONTEND` | `http://localhost:5173` | Base URL for MercadoPago's return URLs (only added when not on localhost) |
| `URL_API` | `http://localhost:8000` | Base URL for MercadoPago's `notification_url` (only added when public) |
| `NUBE_CDN` / `API_KEY_CDN` / `API_SECRET_CDN` | empty | Cloudinary credentials. If empty, uploads are simulated. |
| `TAMANIO_MAXIMO_MB` | `5` | Maximum image upload size, in MB |
| `TOKEN_MP` | empty | MercadoPago access token. If empty, preferences are simulated. |
| `CLAVE_PUBLICA_MP` | empty | MercadoPago public key |
| `SECRETO_WEBHOOK_MP` | empty | Webhook signature secret. If empty, the signature check is skipped. |

</details>

<details>
<summary><strong>Frontend</strong> (template: <a href="frontend/.env.example"><code>frontend/.env.example</code></a>)</summary>

| Variable | Example | Description |
|---|---|---|
| `VITE_URL_API` | `http://localhost:8000` | Backend base URL. `/api/v1` is added automatically. |
| `VITE_URL_WS` | `ws://localhost:8000` | WebSocket base URL. Use `wss://` behind HTTPS. |
| `VITE_CLAVE_PUBLICA_MP` | `TEST-xxxx…` | MercadoPago public key for the payment widgets. Without it, the widgets show a "not configured" notice. |

Only variables that start with `VITE_` are sent to the browser. **Never put backend secrets here.**

</details>

---

## Testing

The backend tests use **pytest** with FastAPI's `TestClient`:

- Each test runs against a **separate SQLite database** that is dropped, recreated, and seeded again. Tests never touch PostgreSQL.
- Fixtures provide ready-made admin and customer tokens and auth headers.
- The MercadoPago payment lookup is mocked with `unittest.mock.patch`, so the webhook can be tested without network calls.
- The rate limiter is turned off during tests.

Tests are grouped by module: `test_sesion`, `test_ordenes`, `test_cobros`, `test_metricas`, `test_tiempo_real`.

```bash
cd backend
pytest                              # full suite; pytest.ini enforces 60% coverage
pytest pruebas/test_ordenes.py      # one file
pytest -k "test_crear_orden"        # one test by name
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `429 Too Many Requests` on login | Login is limited to 5 attempts per 15 minutes per IP | Wait, or restart the API (the limiter only keeps counts in memory) |
| API ignores `backend/.env` when run locally | Local settings are read from the repository root | Move the file to `./.env` (see [Backend](#2-backend)) |
| Products show a placeholder instead of a photo | Demo products have no images | Run `seed_imagenes.py` with Cloudinary credentials, or upload images from the admin panel |
---

## Project structure

<details>
<summary>Expand</summary>

```
foodstore/
├── backend/
│   ├── app/
│   │   ├── principal.py          # App factory, middleware, router mounting, lifespan
│   │   ├── modulos/              # Feature modules
│   │   │   ├── sesion/           #   auth: register, login, refresh, logout
│   │   │   ├── cuentas/          #   account & role administration
│   │   │   ├── domicilios/       #   customer addresses
│   │   │   ├── categorias/       #   category tree
│   │   │   ├── articulos/        #   products, gallery, stock
│   │   │   ├── componentes/      #   ingredients, allergens
│   │   │   ├── ordenes/          #   orders + state machine
│   │   │   ├── cobros/           #   MercadoPago payments & webhook
│   │   │   ├── archivos/         #   Cloudinary uploads
│   │   │   ├── metricas/         #   dashboard aggregates
│   │   │   └── tiempo_real/      #   WebSocket connection manager
│   │   ├── nucleo/               # Settings, security, dependencies, rate limiter
│   │   └── persistencia/         # Engine, Unit of Work, entities, startup seed
│   ├── migraciones/              # Alembic migrations
│   ├── pruebas/                  # pytest suite
│   ├── seed_demo.py              # Demo dataset (destructive)
│   ├── seed_imagenes.py          # Product photos → Cloudinary
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requisitos.txt
├── frontend/
│   ├── src/                      # See "Frontend: feature-based structure"
│   ├── tailwind.config.ts
│   ├── vite.config.ts
│   └── package.json
└── docs/
    └── screenshots/              # Images used in this README
```

</details>
