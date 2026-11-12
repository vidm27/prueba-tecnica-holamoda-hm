<script setup lang="ts">
import type { Satisfaccion } from './useSatisfaccion'

const { data, isPending, error } = useSatisfaccion()
const categoriaActiva = ref<string>('Todas')
const vista = ref<'barras' | 'intervalos'>('barras')

const categorias = computed(() => ['Todas', ...new Set((data.value ?? []).map((p) => p.categoria))])

const promedio = computed(() => {
  const d = data.value ?? []
  return d.reduce((s, p) => s + p.calificacion * p.compras, 0) / Math.max(1, d.reduce((s, p) => s + p.compras, 0))
})

/** "Peor" de verdad solo si, incluso sumando su margen de error, queda bajo el promedio. */
const claramentePeor = (p: Satisfaccion) => p.calificacion + p.margen_error_95 < promedio.value
const bajoPromedio = (p: Satisfaccion) => p.calificacion < promedio.value

const filtrados = computed(() =>
  (data.value ?? []).filter((p) => categoriaActiva.value === 'Todas' || p.categoria === categoriaActiva.value),
)

/** Top 5 productos que menos gustan para destacar visualmente arriba. */
const menosGustan = computed(() => filtrados.value.slice(0, 5))

const brecha = (p: Satisfaccion) => {
  const diff = p.calificacion - promedio.value
  return `${diff >= 0 ? '+' : ''}${diff.toFixed(2)}`
}

const colorEstado = (p: Satisfaccion) => {
  if (claramentePeor(p)) return '#ef4444' // Rojo: bajo el promedio fuera del margen de error
  if (bajoPromedio(p)) return '#f59e0b' // Ámbar: bajo el promedio dentro del margen
  return '#10b981' // Verde: sobre el promedio
}

const seriesBarras = computed(() => [
  {
    nombre: 'Calificación promedio (★)',
    datos: filtrados.value.map((p) => +p.calificacion.toFixed(2)),
    color: filtrados.value.map(colorEstado),
  },
])

// Escala del gráfico de intervalos: rango enfocado para apreciar diferencias e intervalos.
const [MIN, MAX] = [3.4, 4.1]
const pos = (v: number) => `${((Math.min(MAX, Math.max(MIN, v)) - MIN) / (MAX - MIN)) * 100}%`
</script>

<template>
  <SeccionRespuesta :cargando="isPending" :error="error">
    <!-- Tarjetas destacadas: Los 5 productos que menos gustan -->
    <div v-if="menosGustan.length" class="space-y-3">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <div class="flex items-center gap-2">
          <UIcon name="i-lucide-flame" class="size-4 text-error" />
          <h3 class="text-sm font-semibold">Top 5 productos con menor calificación</h3>
        </div>
        <span class="text-xs text-muted">Promedio global del catálogo: <strong class="text-default">{{ promedio.toFixed(2) }} ★</strong></span>
      </div>

      <div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
        <UCard
          v-for="(p, idx) in menosGustan"
          :key="p.producto"
          :class="claramentePeor(p) ? 'ring-2 ring-error/50 bg-error/5' : ''"
        >
          <div class="flex items-start justify-between gap-2">
            <span class="rounded-md px-1.5 py-0.5 text-xs font-bold" :class="claramentePeor(p) ? 'bg-error text-white' : 'bg-elevated text-muted'">
              #{{ idx + 1 }}
            </span>
            <UBadge
              :color="claramentePeor(p) ? 'error' : bajoPromedio(p) ? 'warning' : 'success'"
              variant="subtle"
              size="sm"
              :label="claramentePeor(p) ? 'Crítico (bajo media)' : 'En margen (±)'"
            />
          </div>

          <p class="mt-2.5 truncate text-base font-semibold">{{ es(p.producto) }}</p>
          <p class="text-xs text-muted">{{ es(p.categoria) }} · {{ p.compras }} compras</p>

          <div class="mt-3 flex items-baseline justify-between border-t border-default pt-2.5">
            <div class="flex items-baseline gap-1">
              <span class="text-xl font-bold tabular-nums" :class="claramentePeor(p) ? 'text-error' : ''">{{ p.calificacion.toFixed(2) }}</span>
              <span class="text-xs text-warning">★</span>
            </div>
            <span class="text-xs font-medium tabular-nums" :class="p.calificacion < promedio ? 'text-error' : 'text-success'">
              {{ brecha(p) }} vs. media
            </span>
          </div>
        </UCard>
      </div>
    </div>

    <!-- Visualización comparativa completa con filtro por categoría y selector de vista -->
    <UCard>
      <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div class="flex flex-wrap items-center gap-1.5">
          <UButton
            v-for="cat in categorias"
            :key="cat"
            size="xs"
            color="neutral"
            :variant="categoriaActiva === cat ? 'solid' : 'ghost'"
            :label="cat === 'Todas' ? 'Todas las categorías' : es(cat)"
            @click="categoriaActiva = cat"
          />
        </div>

        <div class="flex items-center gap-1 rounded-lg border border-default p-0.5">
          <UButton
            size="xs"
            color="neutral"
            :variant="vista === 'barras' ? 'soft' : 'ghost'"
            icon="i-lucide-bar-chart-horizontal"
            label="Ranking de barras"
            @click="vista = 'barras'"
          />
          <UButton
            size="xs"
            color="neutral"
            :variant="vista === 'intervalos' ? 'soft' : 'ghost'"
            icon="i-lucide-git-commit-horizontal"
            label="Intervalos de confianza (±)"
            @click="vista = 'intervalos'"
          />
        </div>
      </div>

      <div class="mb-4 flex flex-wrap items-center gap-4 text-xs text-muted">
        <span class="flex items-center gap-1.5">
          <span class="size-2.5 rounded-full bg-error" /> Bajo el promedio incluso con margen de error
        </span>
        <span class="flex items-center gap-1.5">
          <span class="size-2.5 rounded-full bg-warning" /> Bajo el promedio (dentro del margen ±)
        </span>
        <span class="flex items-center gap-1.5">
          <span class="size-2.5 rounded-full bg-success" /> Igual o superior al promedio ({{ promedio.toFixed(2) }} ★)
        </span>
      </div>

      <!-- Vista 1: Gráfico de barras horizontales con semáforo de satisfacción -->
      <GraficoBarras
        v-if="vista === 'barras'"
        :etiquetas="filtrados.map((p) => es(p.producto))"
        :series="seriesBarras"
        horizontal
        sufijo=" ★"
        :minimo="3.3"
        :maximo="4.1"
        :alto="Math.max(260, filtrados.length * 26 + 40)"
      />

      <!-- Vista 2: Bandas de error al 95% contra línea del promedio -->
      <div v-else>
        <ul class="space-y-2.5 text-sm">
          <li v-for="p in filtrados" :key="p.producto" class="grid grid-cols-[9rem_1fr_6.5rem] items-center gap-3">
            <div class="truncate">
              <span :class="claramentePeor(p) ? 'font-semibold text-error' : 'font-medium'">{{ es(p.producto) }}</span>
            </div>
            <div class="relative h-6 rounded bg-elevated/50 px-1">
              <div class="absolute inset-y-0 z-10 w-0.5 bg-primary/70" :style="{ left: pos(promedio) }" title="Promedio global" />
              <div
                class="absolute top-1/2 h-2 -translate-y-1/2 rounded-full"
                :class="claramentePeor(p) ? 'bg-error/35' : bajoPromedio(p) ? 'bg-warning/35' : 'bg-success/35'"
                :style="{
                  left: pos(p.calificacion - p.margen_error_95),
                  width: `calc(${pos(p.calificacion + p.margen_error_95)} - ${pos(p.calificacion - p.margen_error_95)})`,
                }"
              />
              <div
                class="absolute top-1/2 z-20 size-3.5 -translate-x-1/2 -translate-y-1/2 rounded-full border-2 border-white shadow-sm"
                :class="claramentePeor(p) ? 'bg-error' : bajoPromedio(p) ? 'bg-warning' : 'bg-success'"
                :style="{ left: pos(p.calificacion) }"
              />
            </div>
            <div class="flex items-center justify-end gap-1.5 text-right tabular-nums">
              <span class="font-semibold">{{ p.calificacion.toFixed(2) }}</span>
              <span class="text-xs text-muted">±{{ p.margen_error_95.toFixed(2) }}</span>
            </div>
          </li>
        </ul>
        <div class="mt-2 grid grid-cols-[9rem_1fr_6.5rem] gap-3 text-xs text-muted">
          <span />
          <div class="flex justify-between">
            <span>{{ MIN }} ★</span>
            <span>Media: {{ promedio.toFixed(2) }} ★</span>
            <span>{{ MAX }} ★</span>
          </div>
          <span />
        </div>
      </div>
    </UCard>

    <template #confianza>
      <p>Cada producto cuenta con entre 120 y 170 calificaciones, lo que genera un margen de error de ~±0.1 puntos al 95% de confianza.</p>
      <p>Un producto se clasifica como crítico (rojo) cuando incluso el extremo superior de su intervalo de confianza queda por debajo del promedio general ({{ promedio.toFixed(2) }} ★).</p>
    </template>

    <template #detalle>
      <table class="w-full text-sm">
        <thead class="text-left text-muted">
          <tr>
            <th class="py-2">Producto</th>
            <th>Categoría</th>
            <th class="text-right">Compras</th>
            <th class="text-right">Promedio</th>
            <th class="text-right">Brecha vs. media</th>
            <th class="text-right">Margen ± (95%)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in filtrados" :key="p.producto" class="border-t border-default">
            <td class="py-2 font-medium">{{ es(p.producto) }}</td>
            <td>{{ es(p.categoria) }}</td>
            <td class="text-right tabular-nums">{{ p.compras }}</td>
            <td class="text-right font-medium tabular-nums">{{ p.calificacion.toFixed(2) }} ★</td>
            <td class="text-right tabular-nums" :class="p.calificacion < promedio ? 'text-error' : 'text-success'">{{ brecha(p) }}</td>
            <td class="text-right tabular-nums">±{{ p.margen_error_95.toFixed(2) }}</td>
          </tr>
        </tbody>
      </table>
    </template>
  </SeccionRespuesta>
</template>
