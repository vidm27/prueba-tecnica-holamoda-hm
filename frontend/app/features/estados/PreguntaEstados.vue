<script setup lang="ts">
import type { TopEstado } from './useTopEstados'

const { data, isPending, error } = useTopEstados()
const busqueda = ref('')
const filtro = ref<'todos' | 'claros' | 'empates'>('todos')

const confiables = computed(() => data.value?.filter((e) => e.muestra_suficiente) ?? [])
const empatados = computed(() => data.value?.filter((e) => !e.muestra_suficiente && e.productos_empatados > 1) ?? [])
const pct = (e: TopEstado) => Math.round((100 * e.ventas_producto) / Math.max(1, e.ventas_estado))

/** Top 15 estados por volumen de ventas totales para el gráfico de barras. */
const topVolumen = computed(() =>
  [...(data.value ?? [])].sort((a, b) => b.ventas_estado - a.ventas_estado).slice(0, 15),
)

const seriesTopEstados = computed(() => [
  {
    nombre: 'Ventas totales del estado',
    datos: topVolumen.value.map((e) => e.ventas_estado),
    color: topVolumen.value.map((e) => (e.muestra_suficiente ? '#e11d48' : '#64748b')),
  },
])

const estadosFiltrados = computed(() =>
  (data.value ?? []).filter((e) => {
    const coincideTexto =
      !busqueda.value ||
      e.estado.toLowerCase().includes(busqueda.value.toLowerCase()) ||
      es(e.producto).toLowerCase().includes(busqueda.value.toLowerCase())
    if (!coincideTexto) return false
    if (filtro.value === 'claros') return e.muestra_suficiente
    if (filtro.value === 'empates') return e.productos_empatados > 1
    return true
  }),
)
</script>

<template>
  <SeccionRespuesta :cargando="isPending" :error="error">
    <!-- Indicadores generales -->
    <div class="grid gap-4 sm:grid-cols-3">
      <UCard>
        <div class="flex items-center justify-between">
          <p class="text-xs font-medium tracking-wide text-muted uppercase">Estados analizados</p>
          <UIcon name="i-lucide-map-pin" class="size-4 text-primary" />
        </div>
        <p class="mt-2 text-2xl font-bold tabular-nums">{{ data?.length ?? 0 }}</p>
        <p class="text-xs text-muted">60 a 100 compras por estado</p>
      </UCard>
      <UCard>
        <div class="flex items-center justify-between">
          <p class="text-xs font-medium tracking-wide text-muted uppercase">Con producto líder claro</p>
          <UIcon name="i-lucide-award" class="size-4 text-primary" />
        </div>
        <div class="mt-2 flex items-baseline gap-2">
          <p class="text-2xl font-bold text-primary tabular-nums">{{ confiables.length }}</p>
          <span class="text-xs text-muted">de {{ data?.length ?? 0 }} estados</span>
        </div>
        <p class="text-xs text-muted">Al menos 10 ventas del #1 y sin empate</p>
      </UCard>
      <UCard>
        <div class="flex items-center justify-between">
          <p class="text-xs font-medium tracking-wide text-muted uppercase">Con empate en el 1.er lugar</p>
          <UIcon name="i-lucide-split" class="size-4 text-warning" />
        </div>
        <p class="mt-2 text-2xl font-bold tabular-nums">{{ empatados.length }}</p>
        <p class="text-xs text-muted">Estados donde 2 o más prendas empatan</p>
      </UCard>
    </div>

    <!-- Sección protagonista: Estados con producto líder claro -->
    <div v-if="confiables.length" class="space-y-3">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <div class="flex items-center gap-2">
          <UIcon name="i-lucide-sparkles" class="size-4 text-primary" />
          <h3 class="text-sm font-semibold">Estados con producto líder claro (muestra suficiente y sin empate)</h3>
        </div>
        <span class="text-xs text-muted">Prenda, talla y color más demandados en cada uno</span>
      </div>

      <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <UCard v-for="e in confiables" :key="e.estado" class="ring-1 ring-primary/30 bg-primary/5">
          <div class="flex items-start justify-between gap-2">
            <div>
              <p class="text-base font-bold">{{ e.estado }}</p>
              <p class="text-xs text-muted">{{ e.ventas_estado }} compras totales</p>
            </div>
            <UBadge color="primary" variant="subtle" size="sm" :label="`${pct(e)}% del estado`" />
          </div>

          <div class="mt-3 rounded-lg border border-default bg-default/80 p-3">
            <p class="text-xs text-muted">Producto #1</p>
            <p class="text-lg font-bold text-primary">{{ es(e.producto) }}</p>
            <p class="text-xs text-muted">{{ e.ventas_producto }} unidades vendidas</p>
          </div>

          <div class="mt-3 grid grid-cols-2 gap-2 text-xs">
            <div class="rounded-md bg-elevated/70 px-2.5 py-1.5">
              <span class="block text-muted">Talla líder</span>
              <span class="font-semibold">{{ e.talla }} ({{ e.ventas_talla }})</span>
            </div>
            <div class="rounded-md bg-elevated/70 px-2.5 py-1.5">
              <span class="block text-muted">Color líder</span>
              <span class="font-semibold">{{ es(e.color) }} ({{ e.ventas_color }})</span>
            </div>
          </div>
        </UCard>
      </div>
    </div>

    <!-- Gráfico de barras: Top 15 estados por volumen de ventas -->
    <UCard>
      <div class="mb-3 flex flex-wrap items-center justify-between gap-2">
        <div>
          <p class="text-sm font-medium">Top 15 estados por volumen de compras y su prenda #1</p>
          <p class="text-xs text-muted">
            En color primario los estados con líder estadísticamente claro; en gris aquellos donde la demanda se fragmenta entre las 25 prendas
          </p>
        </div>
      </div>
      <GraficoBarras
        :etiquetas="topVolumen.map((e) => `${e.estado} · ${es(e.producto)}`)"
        :series="seriesTopEstados"
        horizontal
        sufijo=" compras"
        :alto="420"
      />
    </UCard>

    <!-- Explorador rápido de estados (buscador + tarjetas) -->
    <UCard>
      <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div>
          <p class="text-sm font-medium">Explorador por estado ({{ estadosFiltrados.length }})</p>
          <p class="text-xs text-muted">Filtra por nombre de estado o prenda para consultar su talla, color y nivel de concentración</p>
        </div>
        <div class="flex flex-wrap items-center gap-2">
          <UInput v-model="busqueda" icon="i-lucide-search" size="xs" placeholder="Buscar estado o prenda..." class="w-52" />
          <div class="flex items-center gap-1 rounded-lg border border-default p-0.5">
            <UButton size="xs" color="neutral" :variant="filtro === 'todos' ? 'soft' : 'ghost'" label="Todos" @click="filtro = 'todos'" />
            <UButton size="xs" color="neutral" :variant="filtro === 'claros' ? 'soft' : 'ghost'" label="Líder claro" @click="filtro = 'claros'" />
            <UButton size="xs" color="neutral" :variant="filtro === 'empates' ? 'soft' : 'ghost'" label="Con empate" @click="filtro = 'empates'" />
          </div>
        </div>
      </div>

      <div class="grid max-h-96 gap-2.5 overflow-y-auto pr-1 sm:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="e in estadosFiltrados"
          :key="e.estado"
          class="flex flex-col justify-between rounded-lg border border-default p-3 text-sm"
        >
          <div class="flex items-start justify-between gap-2">
            <div>
              <p class="font-semibold">{{ e.estado }}</p>
              <p class="text-xs text-muted">
                #1: <strong class="text-default">{{ es(e.producto) }}</strong> ({{ e.ventas_producto }}/{{ e.ventas_estado }} uds)
              </p>
            </div>
            <UBadge
              :color="e.muestra_suficiente ? 'primary' : e.productos_empatados > 1 ? 'warning' : 'neutral'"
              variant="subtle"
              size="sm"
              :label="e.muestra_suficiente ? 'Líder claro' : e.productos_empatados > 1 ? `Empate (${e.productos_empatados})` : 'Disperso'"
            />
          </div>
          <div class="mt-2 flex items-center justify-between border-t border-default pt-2 text-xs text-muted">
            <span>Talla: <strong class="text-default">{{ e.talla }}</strong></span>
            <span>Color: <strong class="text-default">{{ es(e.color) }}</strong></span>
            <span>{{ pct(e) }}% del total</span>
          </div>
        </div>
      </div>
    </UCard>

    <template #confianza>
      <p>Cada estado tiene entre 60 y 100 compras repartidas entre 25 productos (~3 a 4 ventas por producto en promedio).</p>
      <p>Un producto líder se clasifica como claro cuando alcanza al menos 10 ventas en el estado y no empata en el primer lugar.</p>
    </template>

    <template #detalle>
      <table class="w-full text-sm">
        <thead class="text-left text-muted">
          <tr><th class="py-2">Estado</th><th>Producto líder</th><th class="text-right">Ventas</th><th>Talla</th><th>Color</th><th>Clasificación</th></tr>
        </thead>
        <tbody>
          <tr v-for="e in data" :key="e.estado" class="border-t border-default">
            <td class="py-2 font-medium">{{ e.estado }}</td>
            <td>{{ es(e.producto) }}</td>
            <td class="text-right tabular-nums">{{ e.ventas_producto }} / {{ e.ventas_estado }}</td>
            <td class="pl-3">{{ e.talla }}</td>
            <td>{{ es(e.color) }}</td>
            <td>{{ e.muestra_suficiente ? 'Líder claro' : e.productos_empatados > 1 ? `Empate (${e.productos_empatados})` : 'Muestra baja' }}</td>
          </tr>
        </tbody>
      </table>
    </template>
  </SeccionRespuesta>
</template>
