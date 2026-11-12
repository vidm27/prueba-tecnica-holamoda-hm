"""Textos de la documentación de Swagger: descripción general y tags."""

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
