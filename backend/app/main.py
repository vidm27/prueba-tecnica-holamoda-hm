import time
import uuid

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import literal, select
from loguru import logger
from sqlmodel import Session

from app.api import api
from app.nucleo.config import config
from app.nucleo.db import obtener_sesion
from app.nucleo.limitador import limitador
from app.nucleo.logs import configurar_logs
from app.nucleo.manejo_errores import registrar_manejadores

configurar_logs()

DESCRIPCION = """
API de analítica sobre el dataset **Customer Shopping Trends**: 3,900 compras de moda,
con sus clientes y productos. Cada grupo de rutas responde una pregunta de negocio.

## Cómo autenticarte
1. Llama a `POST /api/v1/auth/login` con `username` y `password`.
2. Copia el `access_token` y pulsa **Authorize** (arriba a la derecha).
3. Todas las rutas de `/api/v1` exigen el token, salvo el login.

El token dura 60 minutos. Si vence, la API responde `401 token_invalido` y hay que volver a iniciar sesión.

## Errores
Todo error responde con el mismo formato:

```json
{"error": {"codigo": "datos_insuficientes", "estatus": 422, "mensaje": "No hay variación suficiente…"}}
```

`codigo` es estable y sirve para que el cliente decida qué mostrar; `estatus` es el código HTTP;
`detalle` aparece solo en errores de validación y lista los campos afectados.

## Límites
- **Login:** 10 intentos por minuto por IP. Al superarlo responde `429` con la cabecera `Retry-After`.

## Limitaciones de los datos
El dataset no trae fechas de compra: no hay tendencias en el tiempo ni recompra. Las conclusiones
sobre diferencias entre grupos se corrigen por comparaciones múltiples, y los endpoints indican
cuándo una muestra es demasiado pequeña.
"""

TAGS = [
    {"name": "Sistema", "description": "Estado del servicio. No requiere autenticación."},
    {"name": "Autenticación", "description": "Emite el token JWT que usan el resto de rutas."},
    {"name": "Resumen", "description": "Indicadores generales del dataset."},
    {"name": "Compras", "description": "Listado de compras con filtros y paginación."},
    {"name": "Promociones", "description": "¿De qué producto lanzar una promoción o un descuento?"},
    {"name": "Satisfacción", "description": "Calificación por producto, con margen de error."},
    {"name": "Estacionalidad", "description": "Temporada pico y valle de cada producto."},
    {"name": "Estados", "description": "Producto líder por estado, con su talla y color."},
    {"name": "Tallas", "description": "Curva de tallas por categoría, para inventario."},
    {"name": "Suscripción", "description": "¿Vale la pena la suscripción?"},
    {"name": "Valor de clientes", "description": "Segmentación por gasto anual y regla 80/20."},
    {"name": "Envíos", "description": "Tipo de envío por segmento de clientes."},
    {"name": "Calidad de datos", "description": "Hallazgos de calidad detectados por el ETL."},
    {"name": "Hipótesis", "description": "Pruebas estadísticas con corrección por comparaciones múltiples."},
]

app = FastAPI(
    title="Tendencias de compra · Hola Moda",
    summary="Analítica de compras de moda: promociones, tallas, segmentos y calidad de datos.",
    description=DESCRIPCION,
    version="0.1.0",
    openapi_tags=TAGS,
    swagger_ui_parameters={"persistAuthorization": True, "displayRequestDuration": True},
)
app.add_middleware(CORSMiddleware, allow_origins=config.cors_origenes.split(","),
                   allow_methods=["GET", "POST"], allow_headers=["Authorization", "Content-Type"])
app.state.limitador = limitador


@app.middleware("http")
async def registrar_peticion(request: Request, call_next):
    """Cada petición lleva un request_id (cabecera X-Request-ID o uno nuevo) y se registra con su duración."""
    request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex[:12]
    inicio = time.perf_counter()
    with logger.contextualize(request_id=request_id):
        logger.debug("→ {} {}", request.method, request.url.path)
        respuesta = await call_next(request)
        ms = (time.perf_counter() - inicio) * 1000
        logger.info("{} {} → {} ({:.1f} ms)", request.method, request.url.path, respuesta.status_code, ms)
    respuesta.headers["X-Request-ID"] = request_id
    return respuesta
registrar_manejadores(app)


@app.get("/salud", tags=["Sistema"], summary="Estado del servicio")
def salud(sesion: Session = Depends(obtener_sesion)):
    """Confirma que la API responde y que la base de datos acepta consultas. Sin autenticación."""
    sesion.execute(select(literal(1)))
    return {"estado": "ok"}


app.include_router(api)
