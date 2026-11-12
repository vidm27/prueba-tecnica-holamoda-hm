# Frontend — Hola Moda (Tendencias de Compra)

Aplicación web desarrollada en **Nuxt 4 (SPA)** sobre **Tailwind CSS 4** y **Nuxt UI v4**, orientada al análisis comercial y gerencial de hábitos de compra en retail.

---

## 🏛️ Arquitectura y Principios de Diseño

El frontend sigue el patrón **Vertical Slicing** (rebanadas verticales por funcionalidad de negocio) en lugar de una organización tradicional por capas técnicas:

```
frontend/app/
├── features/                  # Rebanadas verticales de negocio
│   ├── autenticacion/         # Inicio de sesión con JWT y sesión segura
│   ├── resumen/               # Tarjetas KPI principales de la tienda
│   ├── promociones/           # Matriz ventas vs. calificación y sesgos
│   ├── satisfaccion/          # Ranking de calificaciones e intervalos ±95%
│   ├── tallas/                # Curva de tallas por categoría
│   ├── abastecimiento/        # Estabilidad estacional y guía visual anual
│   ├── alto-valor/            # Segmentación por cuartiles de valor (Pareto)
│   ├── suscripcion/           # Impacto de membresía en ticket y recompra
│   ├── envios/                # Distribución de modalidades de entrega
│   ├── estados/               # Ventas geográficas y detección de líderes
│   ├── calidad/               # Auditoría estructural y metodológica
│   └── hipotesis/             # Pruebas estadísticas con corrección múltiple
├── shared/                    # Infraestructura transversal
│   ├── useApi.ts              # Cliente HTTP autenticado con Bearer token
│   ├── navegacion.ts          # Configuración del menú y permisos por rol
│   ├── formato.ts             # Formateadores monetarios y porcentuales (es-PA)
│   ├── traduccion.ts          # Diccionario de dominio EN -> ES
│   ├── estadistica.ts         # Funciones de bondad de ajuste chi-cuadrado
│   ├── SeccionRespuesta.vue   # Contenedor estándar de módulo analítico
│   ├── GraficoBarras.vue      # Envoltorio responsivo Chart.js (Barras)
│   └── GraficoDona.vue        # Envoltorio responsivo Chart.js (Dona/Donut)
├── layouts/                   # Layout dashboard colapsable y barra superior
├── pages/                     # Páginas delgadas que componen los features
├── plugins/                   # Registro de Chart.js y TanStack Query
└── middleware/                # Protección de rutas mediante auth.global.ts
```

---

## 🚀 Tecnologías Clave

- **Nuxt 4 (SPA, `ssr: false`):** Todo el procesamiento analítico se ejecuta de forma reactiva en el cliente, manteniendo el token JWT en memoria y `sessionStorage`.
- **Nuxt UI v4 + Tailwind CSS 4:** Componentes de interfaz adaptables con soporte nativo de modo claro/oscuro.
- **TanStack Query (`@tanstack/vue-query`):** Caché inteligente de consultas analíticas (`staleTime: 60s`, deduplicación de peticiones y control de reintentos).
- **Chart.js (`vue-chartjs`):** Renderizado acelerado de gráficos (dispersión, barras apiladas, barras agrupadas y gráficos de dona).

---

## 📦 Módulos de Negocio

### 1. Promoción y Satisfacción (`/promocion`)
- **Matriz de Cuadrantes (Ventas vs. Calificación):** Identifica productos con alta satisfacción pero baja visibilidad (*Promover*) frente a riesgos de reputación (*Cuidar*).
- **Alerta de Oportunidad por Sesgo de Género:** Destaca que el 100% de los descuentos históricos se aplicó al segmento masculino, identificando un 32% de mercado femenino inexplorado.
- **Ranking de Satisfacción e Intervalos de Confianza (±95%):** Semáforo estadístico que separa variaciones aleatorias de problemas reales de calidad.

### 2. Curva de Tallas (`/tallas`)
- Demuestra que la distribución de tallas es idéntica en todas las categorías (`M: ~44%`, `L: ~27%`, `S: ~18%`, `XL: ~11%`), permitiendo una política unificada de compras.

### 3. Abastecimiento (`/abastecimiento`)
- **Guía Visual por Temporada:** Presentación interactiva por prendas que evidencia una demanda uniforme en las cuatro estaciones (`~25%` por temporada), descartando la necesidad de sobrestock estacional.

### 4. Clientes: Valor, Suscripción y Envíos
- **Más Valiosos (`/alto-valor`):** Segmentación en 4 cuartiles (Bronce, Plata, Oro, Platino). Platino (25% de la base) concentra el 65% del ingreso estimado. Incluye equivalencia frente al cuartil Bronce.
- **Suscripciones (`/suscripcion`):** Evaluación de membresía; constata que los clientes suscritos no generan un ticket superior significativo pero reciben descuento obligatorio.
- **Preferencia de Envío (`/envios`):** Demuestra reparto uniforme (`~16.7%` en cada una de las 6 modalidades) sin preferencias intrínsecas por segmento demográfico.

### 5. Ventas por Estado (`/estados`)
- Ranking de volumen por estado e identificación de los 4 únicos estados con liderazgo estadístico claro (≥10 compras del producto líder y sin empates).

---

## 🛠️ Comandos de Desarrollo y Testing

Ejecutar desde el directorio del frontend o mediante pnpm:

```bash
# Instalar dependencias
pnpm install

# Modo desarrollo (puerto 3001)
pnpm dev

# Compilar para producción (SPA estática)
pnpm generate

# Ejecutar pruebas unitarias de utilidades y navegación
pnpm test
```
