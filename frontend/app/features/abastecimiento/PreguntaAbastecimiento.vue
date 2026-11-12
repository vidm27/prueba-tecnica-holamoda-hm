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

const temporadas = computed(() => {
  const claves = new Set((data.value ?? []).flatMap((d) => Object.keys(d.ventas_por_temporada)))
  return [...claves].sort((a, b) => ORDEN.indexOf(a) - ORDEN.indexOf(b))
})
const valores = (e: Estacionalidad) => temporadas.value.map((t) => e.ventas_por_temporada[t] ?? 0)
const totalProducto = (e: Estacionalidad) => valores(e).reduce((a, b) => a + b, 0)

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

/** Si hay una temporada seleccionada, ordena los productos por ventas en esa temporada; si no, por nombre. */
const productosOrdenados = computed(() => {
  const lista = [...(data.value ?? [])]
  if (temporadaActiva.value) {
    const t = temporadaActiva.value
    return lista.sort((a, b) => (b.ventas_por_temporada[t] ?? 0) - (a.ventas_por_temporada[t] ?? 0))
  }
  return lista
})

/** Series del gráfico: reparto 100% apilado por temporada (vista general) o ranking de la temporada elegida. */
const seriesGrafico = computed(() => {
  if (temporadaActiva.value) {
    const t = temporadaActiva.value
    const colorBase = COLORES_TEMPORADA[t] ?? '#3b82f6'
    return [
      {
        nombre: `Unidades vendidas en ${es(t)}`,
        datos: productosOrdenados.value.map((p) => p.ventas_por_temporada[t] ?? 0),
        color: productosOrdenados.value.map((p) => (p.temporada_pico === t ? colorBase : 'rgba(148, 163, 184, 0.45)')),
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
    <!-- Tarjetas interactivas de las 4 temporadas -->
    <div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
      <button
        v-for="t in resumenTemporadas"
        :key="t.clave"
        type="button"
        class="rounded-xl border p-4 text-left transition"
        :class="temporadaActiva === t.clave ? 'border-primary bg-elevated ring-2 ring-primary/40' : 'border-default bg-default/50 hover:bg-elevated/60'"
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
          Pico anual en <strong>{{ t.picos.length }}</strong> productos:
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

    <!-- Gráfico comparativo intuitivo -->
    <UCard>
      <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div>
          <p class="text-sm font-medium">
            {{ temporadaActiva ? `Volumen de ventas en ${es(temporadaActiva)} (destacando productos en su pico)` : 'Distribución anual por temporada (cada barra suma 100%)' }}
          </p>
          <p class="text-xs text-muted">
            {{
              temporadaActiva
                ? 'En color los productos que alcanzan su mayor venta del año en esta temporada; en gris el resto del catálogo.'
                : 'Las 4 estaciones se reparten en bloques casi idénticos (~25% cada una), mostrando una demanda estable todo el año. Haz clic en una tarjeta superior para inspeccionar una temporada.'
            }}
          </p>
        </div>
        <UButton
          v-if="temporadaActiva"
          size="xs"
          color="neutral"
          variant="soft"
          icon="i-lucide-x"
          label="Ver comparativa de las 4 temporadas"
          @click="temporadaActiva = null"
        />
      </div>

      <GraficoBarras
        :etiquetas="productosOrdenados.map((p) => es(p.producto))"
        :series="seriesGrafico"
        horizontal
        :apilado="!temporadaActiva"
        :sufijo="temporadaActiva ? ' uds' : '%'"
        :maximo="temporadaActiva ? undefined : 100"
        :alto="Math.max(320, productosOrdenados.length * 24 + 60)"
      />
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
            <th class="text-right">Temporada pico</th>
            <th class="text-right">Pico vs. media</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="e in productosOrdenados" :key="e.producto" class="border-t border-default">
            <td class="py-2 font-medium">{{ es(e.producto) }}</td>
            <td v-for="t in temporadas" :key="t" class="text-right tabular-nums" :class="t === e.temporada_pico ? 'font-bold text-primary' : ''">
              {{ e.ventas_por_temporada[t] ?? 0 }}
            </td>
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
