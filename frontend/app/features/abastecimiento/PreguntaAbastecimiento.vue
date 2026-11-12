<script setup lang="ts">
import type { Estacionalidad } from './useEstacionalidad'

const { data, isPending, error } = useEstacionalidad()
const ORDEN = ['Spring', 'Summer', 'Fall', 'Winter']
const ICONOS: Record<string, string> = {
  Spring: 'i-lucide-flower-2',
  Summer: 'i-lucide-sun',
  Fall: 'i-lucide-leaf',
  Winter: 'i-lucide-snowflake',
}

const temporadas = computed(() => {
  const claves = new Set((data.value ?? []).flatMap((d) => Object.keys(d.ventas_por_temporada)))
  return [...claves].sort((a, b) => ORDEN.indexOf(a) - ORDEN.indexOf(b))
})
const valores = (e: Estacionalidad) => temporadas.value.map((t) => e.ventas_por_temporada[t] ?? 0)
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
  const totalGeneral = d.reduce((s, e) => s + valores(e).reduce((a, b) => a + b, 0), 0)
  return temporadas.value.map((t) => {
    const ventas = d.reduce((s, e) => s + (e.ventas_por_temporada[t] ?? 0), 0)
    const lider = [...d].sort((a, b) => (b.ventas_por_temporada[t] ?? 0) - (a.ventas_por_temporada[t] ?? 0))[0]
    return {
      clave: t,
      nombre: es(t),
      icono: ICONOS[t] ?? 'i-lucide-calendar',
      ventas,
      pct: Math.round((100 * ventas) / Math.max(1, totalGeneral)),
      lider: lider ? es(lider.producto) : '—',
    }
  })
})

const celda = (e: Estacionalidad, t: string) => {
  const v = valores(e)
  const [min, max] = [Math.min(...v), Math.max(...v)]
  const x = max === min ? 0 : ((e.ventas_por_temporada[t] ?? 0) - min) / (max - min)
  return { background: `color-mix(in oklab, #3b82f6 ${Math.round(12 + x * 55)}%, transparent)` }
}
</script>

<template>
  <SeccionRespuesta :cargando="isPending" :error="error">
    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <UCard v-for="t in resumenTemporadas" :key="t.clave">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium tracking-wide text-muted uppercase">{{ t.nombre }}</span>
          <UIcon :name="t.icono" class="size-4 text-primary" />
        </div>
        <div class="mt-2 flex items-baseline gap-2">
          <p class="text-2xl font-bold tabular-nums">{{ entero(t.ventas) }}</p>
          <UBadge color="neutral" variant="subtle" size="sm" :label="`${t.pct}%`" />
        </div>
        <p class="mt-1 text-xs text-muted">Mayor volumen: <strong class="text-default">{{ t.lider }}</strong></p>
      </UCard>
    </div>

    <UCard>
      <div class="mb-3 flex flex-wrap items-center justify-between gap-2">
        <div>
          <p class="text-sm font-medium">Mapa de calor: Unidades vendidas por producto y temporada</p>
          <p class="text-xs text-muted">Intensidad de color según el volumen de cada producto; en negrita su temporada pico</p>
        </div>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full border-separate border-spacing-1 text-center text-sm">
          <thead class="text-xs text-muted uppercase">
            <tr>
              <th class="py-1.5 text-left font-medium">Producto</th>
              <th v-for="t in temporadas" :key="t" class="py-1.5 font-medium">{{ es(t) }}</th>
              <th class="py-1.5 text-right font-medium">Pico vs. media</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="e in data" :key="e.producto">
              <td class="pr-2 text-left font-medium">{{ es(e.producto) }}</td>
              <td
                v-for="t in temporadas"
                :key="t"
                class="rounded-md px-2.5 py-1.5 tabular-nums"
                :style="celda(e, t)"
                :class="t === e.temporada_pico ? 'font-bold ring-1 ring-primary/40' : ''"
              >
                {{ e.ventas_por_temporada[t] ?? 0 }}
              </td>
              <td class="pl-2 text-right tabular-nums" :class="esEstacional(e) ? 'font-semibold text-primary' : 'text-muted'">
                +{{ sobrePromedio(e) }}%
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </UCard>

    <template #confianza>
      <p>Cada producto promedia ~40 unidades por temporada; a ese tamaño de muestra, desviaciones de hasta ~30% sobre la media ocurren dentro de la variación aleatoria esperada.</p>
      <p>Se evalúa la estacionalidad mediante bondad de ajuste chi-cuadrado con corrección de Bonferroni para las 25 pruebas simultáneas.</p>
    </template>
  </SeccionRespuesta>
</template>
