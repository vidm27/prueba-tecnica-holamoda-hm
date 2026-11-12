# Arquitectura · Tendencias de compra · Hola Moda

Pipeline de datos de punta a punta: un CSV de compras se carga a PostgreSQL con un ETL, una API
FastAPI lo expone con autenticación JWT, y un dashboard Nuxt lo visualiza. Cada pregunta de negocio es
una funcionalidad completa (ruta, servicio, esquemas y tests en su propia carpeta).

## 1. Vista general

```mermaid
flowchart LR
    CSV[(datos/shopping_trends.csv)] --> ETL[ETL<br/>etl/]
    ETL -->|recarga completa<br/>en una transacción| DB[(PostgreSQL 16)]
    NAV[Navegador] -->|SPA| FE[Frontend Nuxt 4<br/>nginx :3001]
    FE -->|HTTP + Bearer JWT| API[Backend FastAPI<br/>:8000]
    API -->|ORM SQLAlchemy| DB
```

El ETL es un proceso bajo demanda; la API y el frontend son servicios permanentes. La base es el único
punto de contacto entre el ETL y la API: no se comunican de otra forma.

## 2. Contenedores (Docker Compose)

```mermaid
flowchart TB
    subgraph compose[docker-compose.yml]
        db[db<br/>postgres:16-alpine<br/>5432]
        api[api<br/>backend/<br/>uvicorn :8000]
        fe[frontend<br/>nginx :3001 → 80]
        etl[etl<br/>profile: etl<br/>ejecución puntual]
    end
    api -- depends_on healthy --> db
    etl -- depends_on healthy --> db
    fe -- depends_on --> api
    datos[(./datos)] -. solo lectura .-> etl
    env[.env] -.-> api
    env -.-> db
    env -.-> etl
```

| Servicio | Imagen | Puerto | Notas |
|---|---|---|---|
| `db` | postgres:16-alpine | 5432 | Volumen `pgdata`; healthcheck con `pg_isready` |
| `api` | `backend/` (Python 3.12) | 8000 | Espera a `db` healthy |
| `frontend` | `frontend/` (Node → nginx) | 3001 | SPA estática con fallback a `index.html` |
| `etl` | `etl/` (Python 3.12) | — | Solo con `docker compose run --rm etl` |

## 3. Pipeline ETL

```mermaid
flowchart LR
    A[extraer<br/>lee el CSV] --> B[validar<br/>Pydantic por fila]
    B -->|válidas| C[enriquecer<br/>grupo de edad,<br/>gasto anual,<br/>nivel de valor]
    B -.->|rechazadas<br/>se registran en log| X((descartadas))
    C --> D[separar<br/>clientes · productos · compras]
    C --> E[auditar<br/>8 reglas de calidad]
    D --> F[cargar<br/>recrea esquema y<br/>inserta en 1 transacción]
    E --> F
    F --> DB[(PostgreSQL)]
```

Propiedades del ETL:
- **Idempotente:** cada corrida recrea el esquema y carga todo de nuevo; repetirla da el mismo resultado.
- **Atómico:** Postgres tiene DDL transaccional, así que si algo falla la base queda como estaba.
- **Tolerante a reglas defectuosas:** si una regla de auditoría falla, se registra y la carga continúa.
- **Sin dependencias pesadas:** la correlación de Spearman se calcula con pandas (sin scipy).

## 4. Modelo de datos

```mermaid
erDiagram
    CLIENTES ||--o{ COMPRAS : realiza
    PRODUCTOS ||--o{ COMPRAS : "aparece en"
    CLIENTES {
        int id PK
        int edad
        string grupo_edad
        string genero
        string ubicacion
        bool suscrito
        int compras_previas
        string frecuencia_compras
        int compras_por_anio
        float gasto_anual_estimado
        string nivel_valor
    }
    PRODUCTOS {
        int id PK
        string nombre
        string categoria
    }
    COMPRAS {
        int id PK
        int cliente_id FK
        int producto_id FK
        float monto_usd
        string talla
        string color
        string temporada
        float calificacion
        string tipo_envio
        bool descuento
        bool codigo_promo
        string metodo_pago
    }
    AUDITORIA {
        int id PK
        string regla
        string severidad
        int filas_afectadas
        int total_filas
        json evidencia
    }
```

El dataset trae una compra por cliente, así que `compras.id` coincide con `clientes.id`. La tabla
`auditoria` no se relaciona con las demás: guarda hallazgos sobre el conjunto completo.

## 5. Backend

### 5.1 Capas de una petición

```mermaid
flowchart LR
    R[Petición HTTP] --> MW[Middleware<br/>request_id · duración]
    MW --> RT[api.py<br/>router central]
    RT --> AUTH{protegida?}
    AUTH -->|sí| JWT[usuario_actual<br/>valida Bearer]
    AUTH -->|login| LIM[limitador<br/>10/minute por IP]
    JWT --> RUTA[rutas.py<br/>contrato HTTP]
    LIM --> RUTA
    RUTA -->|Depends| DEP[dependencias.py<br/>construye el servicio]
    DEP --> SRV[servicio.py<br/>lógica y consultas]
    SRV --> ORM[nucleo/consultas.py<br/>SQLAlchemy ORM]
    ORM --> DB[(PostgreSQL)]
    SRV -. lanza .-> ERR[ErrorAplicacion<br/>con estatus y código]
    ERR --> MAN[manejo_errores.py]
    MAN --> RESP[/"error: codigo · estatus · mensaje · detalle"/]
```

Reglas de dependencia (de afuera hacia adentro):
- Las **rutas** solo conocen HTTP: parámetros, códigos y el contrato de respuesta.
- Los **servicios** no importan FastAPI: reciben una sesión y devuelven datos o lanzan errores de aplicación.
- El **núcleo** (`nucleo/`) es lo transversal: configuración, sesión, seguridad, errores, logs y modelos.
- Las funcionalidades **no dependen entre sí**; solo comparten el núcleo.

### 5.2 Estructura de carpetas

```
backend/
├── app/
│   ├── main.py                 arranque: CORS, middleware, manejadores de error
│   ├── api.py                  router central /api/v1 (público y protegido)
│   ├── funcionalidades/
│   │   └── <nombre>/
│   │       ├── rutas.py        endpoints (contrato HTTP)
│   │       ├── dependencias.py obtener_servicio (inyección)
│   │       ├── servicio.py     lógica y consultas
│   │       └── esquemas.py     modelos de respuesta
│   └── nucleo/
│       ├── config.py           variables de entorno tipadas
│       ├── db.py               engine y sesión por petición
│       ├── modelos.py          modelos ORM de lectura
│       ├── consultas.py        joins y utilidades comunes
│       ├── seguridad.py        JWT y comparación de credenciales
│       ├── errores.py          errores de aplicación (estatus + código)
│       ├── respuestas.py       formato único de error
│       ├── manejo_errores.py   convierte cualquier error en respuesta
│       ├── limitador.py        slowapi (login)
│       └── logs.py             loguru + interceptación de logging
└── tests/
    ├── conftest.py
    ├── funcionalidades/<nombre>/   pruebas de integración y unitarias
    └── nucleo/                     contrato de errores, protección, logs
```

### 5.3 Autenticación

```mermaid
sequenceDiagram
    autonumber
    actor U as Usuario
    participant FE as Frontend
    participant API as Backend
    participant LIM as Limitador
    participant SEG as Seguridad

    U->>FE: usuario y clave
    FE->>API: POST /api/v1/auth/login
    API->>LIM: ¿queda cupo para esta IP?
    alt excedido
        LIM-->>API: sin cupo
        API-->>FE: 429 + Retry-After
    else cupo disponible
        API->>SEG: credenciales_validas (tiempo constante)
        alt incorrectas
            API-->>FE: 401 credenciales_invalidas
        else correctas
            API->>SEG: crear_token (HS256, exp, sub)
            API-->>FE: 200 access_token
        end
    end
    FE->>API: GET /api/v1/... (Authorization: Bearer)
    API->>SEG: usuario_actual (decodifica y verifica exp)
    alt token válido
        API-->>FE: 200 datos
    else ausente o inválido
        API-->>FE: 401 token_invalido
        FE->>FE: cierra sesión y vuelve a /login
    end
```

- El secreto JWT tiene al menos 32 caracteres; la aplicación no arranca sin él.
- Hay un único usuario administrador, definido en `.env`.
- La protección está en un solo lugar: `api.py` aplica `usuario_actual` al router `protegida`.
  Una prueba falla si alguna ruta bajo `/api/v1` queda sin protección, salvo el login.

### 5.4 Errores

Todo error de la API responde con el mismo formato:

```json
{"error": {"codigo": "datos_insuficientes", "estatus": 422, "mensaje": "No hay variación suficiente…"}}
```

| Código | Estatus | Quién lo origina |
|---|---|---|
| `credenciales_invalidas` | 401 | Servicio de autenticación |
| `token_invalido` | 401 | Dependencia de seguridad |
| `datos_insuficientes` | 422 | Servicio de hipótesis |
| `validacion` | 422 | FastAPI (parámetros) |
| `limite_excedido` | 429 | Limitador de login |
| `no_encontrado` | 404 | Ruta inexistente |
| `servicio_no_disponible` | 503 | Error de base de datos |
| `error_interno` | 500 | Excepción no controlada (sin detalles internos) |

Cada ruta documenta estos errores en OpenAPI con el mismo esquema `ErrorRespuesta`.

### 5.5 Logs

Un único logger (loguru) para la aplicación, uvicorn, SQLAlchemy y slowapi. Cada petición lleva un
`request_id` (de la cabecera `X-Request-ID` o generado) y se registra con estatus y duración.
`LOG_NIVEL` controla el detalle.

## 6. Frontend

```mermaid
flowchart TB
    APP[app.vue<br/>UApp + NuxtLayout] --> LAY[layouts/default.vue<br/>barra y contenedor]
    APP --> PAGES[pages/<br/>login · index]
    MW[middleware/auth.global.ts<br/>sin token → /login] -.-> PAGES
    PAGES --> F1[features/autenticacion<br/>FormularioLogin · useAuth]
    PAGES --> F2[features/resumen<br/>TarjetasResumen · useResumen]
    F2 --> API_C[shared/useApi.ts<br/>Bearer · 401 → salir]
    F1 --> API_C
    F2 --> TQ[TanStack Query<br/>caché y reintentos]
    API_C --> BACK[(API /api/v1)]
    TQ --> API_C
```

- **SPA** (`ssr: false`): la app está detrás de login, así que no hay nada que renderizar en servidor.
- **Estructura por funcionalidad:** `features/<nombre>/` agrupa componentes, composables y tipos.
  `shared/` contiene lo transversal (cliente HTTP, formato). Las páginas solo componen componentes.
- **Token:** vive en memoria y en `sessionStorage` (se borra al cerrar la pestaña).
- **Caché:** TanStack Query con `staleTime` de 60 s, porque los datos solo cambian al correr el ETL.

## 7. Endpoints

Todos bajo `/api/v1`, con Bearer salvo `auth/login`.

| Ruta | Pregunta de negocio |
|---|---|
| `POST /auth/login` | Obtener token |
| `GET /resumen` | Indicadores generales |
| `GET /compras` | Listado paginado con filtros |
| `GET /productos/promocion` | ¿De qué producto lanzar una promoción? |
| `GET /productos/satisfaccion` | Calificación con margen de error |
| `GET /productos/estacionalidad` | Temporada pico y valle por producto |
| `GET /estados/top-productos` | Producto líder por estado, con talla y color |
| `GET /tallas/curva` | Curva de tallas por categoría |
| `GET /suscripcion/impacto` | ¿Vale la pena la suscripción? |
| `GET /clientes/valor` | Segmentación por valor y Pareto |
| `GET /envios/por-segmento` | Tipo de envío por segmento |
| `GET /calidad/auditoria` | Hallazgos de calidad del ETL |
| `GET /hipotesis` | Kruskal-Wallis con corrección de Bonferroni |

`GET /salud` es público y verifica el servicio y la base.

## 8. Decisiones clave

| Tema | Decisión | Motivo |
|---|---|---|
| Datos | Customer Shopping Trends | Caso cercano al retail de moda |
| ETL | Script Python, no orquestador | Dataset pequeño; Airflow sería sobreingeniería |
| Validación | Por fila (Pydantic) y por conjunto (auditoría) | Los problemas del dataset solo se ven en conjunto |
| Segmentación | Por valor (cuartiles), no K-means | La única heterogeneidad real es el gasto; K-means sobre ruido uniforme no aporta |
| Consultas | ORM SQLAlchemy | Legible y testeable; las agregaciones siguen en la base |
| Arquitectura | Vertical slicing + capa de servicios + DI | Cada funcionalidad se entiende y se prueba por separado |
| Frontend | Nuxt 4 SPA + Nuxt UI + TanStack Query | SPA detrás de login; componentes listos; caché de datos |
| Autenticación | JWT HS256 con usuario en `.env` | Un solo operador; sin tabla de usuarios |
| Límite de login | 10 por minuto por IP | Frena fuerza bruta sin bloquear el uso normal |

## 9. Limitaciones conocidas

- **Sin fechas de compra:** no hay tendencias en el tiempo ni retención.
- **Límites en memoria:** el limitador de login guarda sus contadores por proceso. Con varias réplicas
  habría que usar Redis (`storage_uri`).
- **Un solo usuario administrador.** Con más usuarios haría falta tabla de usuarios y hash de claves.
- **Dataset sintético:** la auditoría lo señala; las conclusiones se presentan con esa salvedad.
