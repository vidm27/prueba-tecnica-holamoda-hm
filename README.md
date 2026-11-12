# Tendencias de compra · Hola Moda

Prueba técnica (Analista de Desarrollo e Integración). Pipeline ETL + API + dashboard sobre el dataset
*Customer Shopping Trends* (Kaggle, ~3.9k filas).

| Capa | Tecnología | Puerto |
|---|---|---|
| Base de datos | PostgreSQL 16 | 5432 |
| ETL | Python (pandas, Pydantic, SQLModel), ejecución bajo demanda | — |
| Backend | FastAPI + JWT | 8000 |
| Frontend | Nuxt 4 (SPA) + Nuxt UI + TanStack Query + Chart.js, servido por nginx | 3001 |

## Estructura del repositorio

```
.
├── backend/              Proyecto FastAPI
│   ├── app/
│   │   ├── main.py       Arranque: registra las funcionalidades
│   │   ├── funcionalidades/   Una carpeta por pregunta de negocio (rutas, servicio, esquemas)
│   │   └── nucleo/       Configuración, modelos ORM, sesión, seguridad y limitador
│   ├── tests/            Pruebas espejo de app/: de integración y unitarias
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/             Proyecto Nuxt (SPA)
│   └── app/
│       ├── features/     Una carpeta por funcionalidad (componentes, composables, tipos)
│       ├── shared/       Cliente de la API y utilidades comunes
│       └── pages/, layouts/, plugins/, middleware/   Convenciones de Nuxt
├── etl/                  Carga del CSV a PostgreSQL (extraer, validar, transformar, cargar)
├── datos/                Dataset de origen (shopping_trends.csv)
├── docs/                 Notas técnicas
└── docker-compose.yml    db + backend + frontend + etl
```

## Requisitos

- Docker + Docker Compose (suficiente para levantar todo)
- Opcional, para desarrollo local: Python 3.12 y Node 22 con pnpm 10

## Levantar el proyecto

```bash
# 1. Variables de entorno
cp .env.example .env
#    editar .env: POSTGRES_PASSWORD, JWT_SECRETO (>= 32 caracteres), ADMIN_USUARIO, ADMIN_CLAVE

# 2. Dataset: incluido en datos/shopping_trends.csv (ver "Fuente de datos" abajo)

# 3. Levantar base de datos, backend y frontend
docker compose up --build -d

# 4. Cargar los datos (ETL bajo demanda; es idempotente, se puede repetir)
docker compose run --rm etl
```

Después del paso 4 la base tiene 3,900 clientes, 25 productos y 3,900 compras.

## URLs

| Qué | URL |
|---|---|
| Dashboard | http://localhost:3001 |
| Swagger / OpenAPI | http://localhost:8000/docs |
| Salud del backend | http://localhost:8000/salud |

Para entrar al dashboard usa `ADMIN_USUARIO` y `ADMIN_CLAVE` de tu `.env`.

En Swagger: `POST /api/v1/auth/login` → copiar el `access_token` → botón **Authorize**.

```bash
# ejemplo con curl
TOKEN=$(curl -s -X POST localhost:8000/api/v1/auth/login \
  -d "username=$ADMIN_USUARIO&password=$ADMIN_CLAVE" | jq -r .access_token)
curl -H "Authorization: Bearer $TOKEN" localhost:8000/api/v1/resumen
```

## Endpoints (`/api/v1`, todos con Bearer excepto `/auth/login`)

`/resumen`, `/compras` (paginado y filtros), `/productos/promocion`, `/productos/satisfaccion`,
`/productos/estacionalidad`, `/estados/top-productos`, `/tallas/curva`, `/suscripcion/impacto`,
`/clientes/valor`, `/envios/por-segmento`, `/calidad/auditoria`, `/hipotesis`.

## Tests

```bash
# Backend (requiere Postgres arriba y el ETL ya corrido; con la base vacía los tests de datos se omiten)
docker compose run --rm --no-deps api pytest -q

# ETL
docker compose run --rm --no-deps etl pytest -q

# Frontend
cd frontend && pnpm install && pnpm test
```

## Desarrollo local (sin Docker para backend y frontend)

```bash
docker compose up -d db                       # solo Postgres

# Backend: las variables del .env, pero con el host local
cd backend && pip install -r requirements.txt
set -a && . ../.env && set +a && export POSTGRES_HOST=localhost
uvicorn app.main:app --reload --port 8000

# Frontend (en otra terminal)
cd frontend && pnpm install && NUXT_PUBLIC_API_BASE=http://localhost:8000 pnpm dev
```

## Operación

```bash
docker compose logs -f api        # ver logs del backend
docker compose down               # parar (conserva los datos)
docker compose down -v            # parar y borrar la base
```

## Notas

- `NUXT_PUBLIC_API_BASE` se incorpora al **compilar** el frontend, porque lo usa el navegador. Si cambia, ejecuta `docker compose build frontend`.
- CORS acepta los orígenes de `CORS_ORIGENES`.
- El login tiene límite de intentos por IP (`LOGIN_LIMITE`, por defecto 5 cada 5 minutos). Al superarlo responde 429 con `Retry-After`.

## Fuente de datos

- **Dataset:** *Customer Shopping Trends Dataset*, publicado en Kaggle:
  https://www.kaggle.com/datasets/iamsouravbanerjee/customer-shopping-trends-dataset
- **Autor y licencia:** pendientes de confirmar. La página del dataset no muestra el autor ni la licencia en la
  versión consultada, así que hay que revisarlas antes de hacer público el repositorio.
- **Uso en el proyecto:** el archivo se versiona en `datos/shopping_trends.csv` para que el ETL funcione sin
  pasos adicionales. Si la licencia lo exige, se puede dejar de versionar y documentar la descarga.
