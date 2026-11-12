<script setup lang="ts">
import type { Estacionalidad } from './useEstacionalidad'

const { data, isPending, error } = useEstacionalidad()
const ORDEN = ['Spring', 'Summer', 'Fall', 'Winter']
const COLORES_TEMPORADA: Record<string, string> = {
  Spring: '#10b981',
  Summer: '#f59e0b',
  Fall: '#ea580c',
  Winter: '#3b82f6',
}
const ICONOS: Record<string, string> = {
  Spring: 'i-lucide-flower-2',
  Summer: 'i-lucide-sun',
  Fall: 'i-lucide-leaf',
  Winter: 'i-lucide-snowflake',
}

const temporadaActiva = ref<string | null>(null)
const productoSeleccionado = ref<string | null>(null)
const vistaGrafico = ref<'calendario' | 'ranking' | 'apilado'>('calendario')
const busqueda = ref('')

const temporadas = computed(() => {
  const claves = new Set((data.value ?? []).flatMap((d) => Object.keys(d.ventas_por_temporada)))
  return [...claves].sort((a, b) => ORDEN.indexOf(a) - ORDEN.indexOf(b))
})
const valores = (e: Estacionalidad) => temporadas.value.map((t) => e.ventas_por_temporada[t] ?? 0)
const totalProducto = (e: Estacionalidad) => valores(e).reduce((a, b) => a + b, 0)
const promedioPorTemporada = (e: Estacionalidad) => Math.round(totalProducto(e) / Math.max(1, temporadas.value.length))

/** Estacional de verdad: su concentración en una temporada no se explica por azar (chi² con Bonferroni). */
const esEstacional = (e: Estacionalidad) => chiCuadradoParejo(valores(e)) > CHI2_4_TEMPORADAS_25_PRODUCTOS

/** Variación del pico sobre el promedio del producto, en %. */
const sobrePromedio = (e: Estacionalidad) => {
  const v = valores(e)
  const media = v.reduce((s, x) => s + x, 0) / v.length
  return Math.round((100 * (Math.max(...v) - media)) / media)
}

const resumenTemporadas = computed(() => {
  const d = data.value ?? []
  const totalGeneral = d.reduce((s, e) => s + totalProducto(e), 0)
  return temporadas.value.map((t) => {
    const ventas = d.reduce((s, e) => s + (e.ventas_por_temporada[t] ?? 0), 0)
    const picos = d.filter((e) => e.temporada_pico === t)
    return {
      clave: t,
      nombre: es(t),
      icono: ICONOS[t] ?? 'i-lucide-calendar',
      color: COLORES_TEMPORADA[t] ?? '#3b82f6',
      ventas,
      pct: Math.round((100 * ventas) / Math.max(1, totalGeneral)),
      picos,
    }
  })
})

/** Producto seleccionado en el inspector individual (por defecto el de mayor venta en la temporada activa o el #1 general). */
const detalleProducto = computed(() => {
  const lista = data.value ?? []
  if (!lista.length) return null
  if (productoSeleccionado.value) {
    const encontrado = lista.find((p) => p.producto === productoSeleccionado.value)
    if (encontrado) return encontrado
  }
  return [...lista].sort((a, b) => totalProducto(b) - totalProducto(a))[0] ?? null
})

const seriesProductoIndividual = computed(() => {
  const prod = detalleProducto.value
  if (!prod) return []
  return [
    {
      nombre: `Unidades vendidas de ${es(prod.producto)}`,
      datos: temporadas.value.map((t) => prod.ventas_por_temporada[t] ?? 0),
      color: temporadas.value.map((t) => COLORES_TEMPORADA[t] ?? '#3b82f6'),
    },
  ]
})

/** Si hay una temporada seleccionada, ordena los productos por ventas en esa temporada; si no, por volumen anual. */
const productosOrdenados = computed(() => {
  const lista = [...(data.value ?? [])].filter(
    (p) => !busqueda.value || es(p.producto).toLowerCase().includes(busqueda.value.toLowerCase()),
  )
  if (temporadaActiva.value) {
    const t = temporadaActiva.value
    return lista.sort((a, b) => (b.ventas_por_temporada[t] ?? 0) - (a.ventas_por_temporada[t] ?? 0))
  }
  return lista.sort((a, b) => totalProducto(b) - totalProducto(a))
})

/** Series para el gráfico comparativo (vista limpia de 1 barra por prenda o 100% apilado opcional). */
const seriesGrafico = computed(() => {
  if (temporadaActiva.value) {
    const t = temporadaActiva.value
    const colorBase = COLORES_TEMPORADA[t] ?? '#3b82f6'
    return [
      {
        nombre: `Unidades vendidas en ${es(t)}`,
        datos: productosOrdenados.value.map((p) => p.ventas_por_temporada[t] ?? 0),
        color: productosOrdenados.value.map((p) =>
          p.temporada_pico === t ? colorBase : 'rgba(148, 163, 184, 0.45)',
        ),
      },
    ]
  }
  if (vistaGrafico.value === 'ranking') {
    return [
      {
        nombre: 'Ventas anuales totales (coloreado según su estación más alta)',
        datos: productosOrdenados.value.map((p) => totalProducto(p)),
        color: productosOrdenados.value.map((p) => COLORES_TEMPORADA[p.temporada_pico] ?? '#3b82f6'),
      },
    ]
  }
  return temporadas.value.map((t) => ({
    nombre: es(t),
    color: COLORES_TEMPORADA[t] ?? '#3b82f6',
    datos: productosOrdenados.value.map((p) =>
      Math.round((100 * (p.ventas_por_temporada[t] ?? 0)) / Math.max(1, totalProducto(p))),
    ),
  }))
})
</script>

<template>
  <SeccionRespuesta :cargando="isPending" :error="error">
    <!-- Conclusión ejecutiva en lenguaje sencillo -->
    <UCard class="border-primary/30 bg-primary/5">
      <div class="flex flex-wrap items-center justify-between gap-4">
        <div class="flex items-start gap-3">
          <div class="mt-0.5 flex size-9 shrink-0 items-center justify-center rounded-lg bg-primary/15 text-primary">
            <UIcon name="i-lucide-calendar-check" class="size-5" />
          </div>
          <div>
            <div class="flex flex-wrap items-center gap-2">
              <h3 class="text-sm font-bold">Conclusión clave: Todo el catálogo se vende parejo durante las 4 estaciones</h3>
              <UBadge color="success" variant="soft" size="sm" label="Abastecimiento continuo (~25% por estación)" />
            </div>
            <p class="mt-1 text-xs text-muted">
              No necesitas acumular sobrestock para una época específica: cada temporada concentra casi exactamente la cuarta parte de las ventas (~38 a 42 unidades por prenda en cada estación).
            </p>
          </div>
        </div>
      </div>
    </UCard>

    <!-- Tarjetas interactivas de las 4 temporadas -->
    <div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
      <button
        v-for="t in resumenTemporadas"
        :key="t.clave"
        type="button"
        class="rounded-xl border p-4 text-left transition"
        :class="
          temporadaActiva === t.clave
            ? 'border-primary bg-elevated ring-2 ring-primary/40'
            : 'border-default bg-default/50 hover:bg-elevated/60'
        "
        @click="temporadaActiva = temporadaActiva === t.clave ? null : t.clave"
      >
        <div class="flex items-center justify-between gap-2">
          <div class="flex items-center gap-2">
            <span class="size-2.5 rounded-full" :style="{ background: t.color }" />
            <span class="text-sm font-semibold">{{ t.nombre }}</span>
          </div>
          <UIcon :name="t.icono" class="size-4 text-muted" />
        </div>

        <div class="mt-2.5 flex items-baseline gap-2">
          <p class="text-2xl font-bold tabular-nums">{{ entero(t.ventas) }}</p>
          <UBadge color="neutral" variant="subtle" size="sm" :label="`${t.pct}% del año`" />
        </div>

        <p class="mt-2 text-xs text-muted">
          Mejor época para <strong>{{ t.picos.length }}</strong> prendas:
        </p>
        <div class="mt-1.5 flex flex-wrap gap-1">
          <UBadge
            v-for="p in t.picos.slice(0, 4)"
            :key="p.producto"
            color="neutral"
            variant="soft"
            size="sm"
            :label="es(p.producto)"
          />
          <UBadge v-if="t.picos.length > 4" color="neutral" variant="subtle" size="sm" :label="`+${t.picos.length - 4}`" />
        </div>
      </button>
    </div>

    <!-- Inspector de prenda individual + Dona del año: súper fácil de digerir -->
    <div v-if="detalleProducto" class="grid gap-4 lg:grid-cols-[21rem_minmax(0,1fr)]">
      <UCard>
        <div class="mb-2">
          <p class="text-sm font-medium">Reparto anual de la tienda</p>
          <p class="text-xs text-muted">Las 4 estaciones pesan prácticamente lo mismo (~25%)</p>
        </div>
        <GraficoDona
          :etiquetas="resumenTemporadas.map((t) => t.nombre)"
          :valores="resumenTemporadas.map((t) => t.pct)"
          :colores="resumenTemporadas.map((t) => t.color)"
          sufijo="%"
          :alto="250"
          titulo-centro="~25%"
          subtitulo-centro="por temporada"
        />
      </UCard>

      <UCard>
        <div class="mb-3 flex flex-wrap items-center justify-between gap-2">
          <div>
            <p class="text-sm font-medium">
              Lupita por prenda: ¿Cómo se vende <strong class="text-primary">{{ es(detalleProducto.producto) }}</strong> en el año?
            </p>
            <p class="text-xs text-muted">
              Elige cualquier prenda para ver sus 4 estaciones sin ruido visual · Promedio:
              <strong>~{{ promedioPorTemporada(detalleProducto) }} uds/temporada</strong>
            </p>
          </div>
          <UBadge
            color="neutral"
            variant="subtle"
            :label="`Total anual: ${totalProducto(detalleProducto)} uds · Mejor: ${es(detalleProducto.temporada_pico)}`"
          />
        </div>

        <!-- Píldoras para elegir rápidamente una prenda -->
        <div class="mb-4 flex flex-wrap gap-1">
          <UButton
            v-for="p in data"
            :key="p.producto"
            size="xs"
            color="neutral"
            :variant="detalleProducto.producto === p.producto ? 'solid' : 'soft'"
            :label="es(p.producto)"
            @click="productoSeleccionado = p.producto"
          />
        </div>

        <GraficoBarras
          :etiquetas="temporadas.map(es)"
          :series="seriesProductoIndividual"
          sufijo=" uds"
          :alto="190"
        />
      </UCard>
    </div>

    <!-- Vista general de los 25 productos: amigable y con selector de modo -->
    <UCard>
      <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div>
          <p class="text-sm font-medium">
            {{
              temporadaActiva
                ? `Ventas en ${es(temporadaActiva)} (en color las prendas que tienen su mejor época aquí)`
                : vistaGrafico === 'calendario'
                  ? 'Guía visual por prenda: volumen en cada estación y pico anual'
                  : vistaGrafico === 'ranking'
                    ? 'Ranking anual por prenda (1 sola barra limpia por producto)'
                    : 'Proporción 100% apilada por temporada'
            }}
          </p>
          <p class="text-xs text-muted">
            {{
              temporadaActiva
                ? 'Haz clic en el botón de la derecha o en la tarjeta superior para volver a ver las 4 temporadas.'
                : vistaGrafico === 'calendario'
                  ? 'De un vistazo y sin gráficos complejos: el volumen por estación y la recomendación de stock para cada prenda.'
                  : vistaGrafico === 'ranking'
                    ? 'El color de cada barra indica en qué estación tuvo su pico anual. Haz clic en cualquier prenda de la tabla o arriba para inspeccionarla.'
                    : 'Cada barra suma 100%: los 4 bloques miden casi lo mismo (~25%), comprobando que la venta es estable todo el año.'
            }}
          </p>
        </div>

        <div class="flex flex-wrap items-center gap-2">
          <UInput
            v-model="busqueda"
            icon="i-lucide-search"
            size="xs"
            placeholder="Buscar prenda..."
            class="w-44"
          />
          <UButton
            v-if="temporadaActiva"
            size="xs"
            color="neutral"
            variant="soft"
            icon="i-lucide-x"
            label="Quitar filtro de temporada"
            @click="temporadaActiva = null"
          />
          <div v-else class="flex items-center gap-1 rounded-lg border border-default p-0.5">
            <UButton
              size="xs"
              color="neutral"
              :variant="vistaGrafico === 'calendario' ? 'soft' : 'ghost'"
              icon="i-lucide-layout-grid"
              label="Guía visual"
              @click="vistaGrafico = 'calendario'"
            />
            <UButton
              size="xs"
              color="neutral"
              :variant="vistaGrafico === 'ranking' ? 'soft' : 'ghost'"
              icon="i-lucide-bar-chart-horizontal"
              label="Ranking simple"
              @click="vistaGrafico = 'ranking'"
            />
            <UButton
              size="xs"
              color="neutral"
              :variant="vistaGrafico === 'apilado' ? 'soft' : 'ghost'"
              icon="i-lucide-layers"
              label="4 estaciones (%)"
              @click="vistaGrafico = 'apilado'"
            />
          </div>
        </div>
      </div>

      <!-- Leyenda de colores cuando estamos en Ranking simple -->
      <div v-if="!temporadaActiva && vistaGrafico === 'ranking'" class="mb-3 flex flex-wrap items-center gap-4 text-xs text-muted">
        <span class="font-medium text-default">Color = estación con más ventas de esa prenda:</span>
        <span v-for="t in resumenTemporadas" :key="t.clave" class="flex items-center gap-1.5">
          <span class="size-2.5 rounded-full" :style="{ background: t.color }" />
          {{ t.nombre }} ({{ t.picos.length }})
        </span>
      </div>

      <!-- Modo 1 y 3: Gráfico de barras (Ranking simple de 1 barra o Apilado) -->
      <GraficoBarras
        v-if="temporadaActiva || vistaGrafico !== 'calendario'"
        :etiquetas="productosOrdenados.map((p) => es(p.producto))"
        :series="seriesGrafico"
        horizontal
        :apilado="!temporadaActiva && vistaGrafico === 'apilado'"
        :sufijo="temporadaActiva || vistaGrafico === 'ranking' ? ' uds' : '%'"
        :maximo="!temporadaActiva && vistaGrafico === 'apilado' ? 100 : undefined"
        :alto="Math.max(260, productosOrdenados.length * 24 + 50)"
      />

      <!-- Modo 2: Guía visual tipo tarjetas/matriz amigable para no expertos -->
      <div v-else class="grid gap-2.5 sm:grid-cols-2 lg:grid-cols-3">
        <button
          v-for="e in productosOrdenados"
          :key="e.producto"
          type="button"
          class="flex flex-col justify-between rounded-xl border border-default p-3 text-left transition hover:bg-elevated/60"
          :class="detalleProducto?.producto === e.producto ? 'ring-2 ring-primary/40 bg-elevated/40' : ''"
          @click="productoSeleccionado = e.producto"
        >
          <div class="flex items-start justify-between gap-2">
            <div>
              <p class="font-semibold">{{ es(e.producto) }}</p>
              <p class="text-xs text-muted">
                <strong>{{ totalProducto(e) }} uds/año</strong> (~{{ promedioPorTemporada(e) }} por estación)
              </p>
            </div>
            <UBadge
              color="neutral"
              variant="soft"
              size="sm"
              :label="`Pico: ${es(e.temporada_pico)}`"
            />
          </div>

          <div class="mt-3 grid grid-cols-4 gap-1.5 text-center text-xs">
            <div
              v-for="t in temporadas"
              :key="t"
              class="rounded-md px-1.5 py-1"
              :class="t === e.temporada_pico ? 'font-bold ring-1 ring-inset' : 'bg-elevated/60 text-muted'"
              :style="
                t === e.temporada_pico
                  ? { background: `${COLORES_TEMPORADA[t]}20`, color: COLORES_TEMPORADA[t] }
                  : {}
              "
            >
              <span class="block text-[10px] opacity-80">{{ es(t).slice(0, 4) }}.</span>
              <span class="tabular-nums">{{ e.ventas_por_temporada[t] ?? 0 }}</span>
            </div>
          </div>
        </button>
      </div>
    </UCard>

    <template #confianza>
      <p>Cada producto registra ~40 ventas por temporada. A ese tamaño de muestra, variaciones de hasta ~30% sobre el promedio ocurren por azar.</p>
      <p>Mediante la prueba chi-cuadrado de bondad de ajuste con corrección de Bonferroni (25 productos), ningún producto presenta concentración estacional estadísticamente significativa.</p>
    </template>

    <template #detalle>
      <table class="w-full text-sm">
        <thead class="text-left text-muted">
          <tr>
            <th class="py-2">Producto</th>
            <th v-for="t in temporadas" :key="t" class="text-right">{{ es(t) }}</th>
            <th class="text-right">Total anual</th>
            <th class="text-right">Temporada pico</th>
            <th class="text-right">Pico vs. media</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="e in productosOrdenados" :key="e.producto" class="border-t border-default">
            <td class="py-2 font-medium">{{ es(e.producto) }}</td>
            <td
              v-for="t in temporadas"
              :key="t"
              class="text-right tabular-nums"
              :class="t === e.temporada_pico ? 'font-bold text-primary' : ''"
            >
              {{ e.ventas_por_temporada[t] ?? 0 }}
            </td>
            <td class="text-right font-medium tabular-nums">{{ totalProducto(e) }}</td>
            <td class="text-right">{{ es(e.temporada_pico) }}</td>
            <td class="text-right tabular-nums" :class="esEstacional(e) ? 'font-semibold text-primary' : 'text-muted'">
              +{{ sobrePromedio(e) }}%
            </td>
          </tr>
        </tbody>
      </table>
    </template>
  </SeccionRespuesta>
</template>
