<script setup lang="ts">
const { data, isPending, error } = useTallas()
const ORDEN = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
const COLORES = ['#f43f5e', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4']

const tallas = computed(() => [...new Set((data.value ?? []).map((d) => d.talla))].sort((a, b) => ORDEN.indexOf(a) - ORDEN.indexOf(b)))
const categorias = computed(() => [...new Set((data.value ?? []).map((d) => d.categoria))])
const pct = (c: string, t: string) => data.value?.find((d) => d.categoria === c && d.talla === t)?.pct ?? 0

/** Curva general: % y compras de todas las categorías por talla. */
const curva = computed(() => {
  const total = (data.value ?? []).reduce((s, d) => s + d.compras, 0)
  return tallas.value.map((t, i) => {
    const compras = (data.value ?? []).filter((d) => d.talla === t).reduce((s, d) => s + d.compras, 0)
    return {
      talla: t,
      compras,
      color: COLORES[i % COLORES.length],
      pct: Math.round((100 * compras) / Math.max(1, total)),
    }
  })
})
/** Mayor diferencia entre categorías para una misma talla, en puntos porcentuales. */
const diferencia = computed(() => Math.max(0, ...tallas.value.map((t) => {
  const v = categorias.value.map((c) => pct(c, t))
  return Math.max(...v) - Math.min(...v)
})))

const series = computed(() => tallas.value.map((t, i) => ({
  nombre: `Talla ${t}`, color: COLORES[i % COLORES.length], datos: categorias.value.map((c) => pct(c, t)),
})))
</script>

<template>
  <SeccionRespuesta :cargando="isPending" :error="error">
    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <UCard v-for="c in curva" :key="c.talla">
        <div class="flex items-center justify-between">
          <span class="text-xs font-medium tracking-wide text-muted uppercase">Talla {{ c.talla }}</span>
          <span class="size-3 rounded-full" :style="{ background: c.color }" />
        </div>
        <p class="mt-2 text-2xl font-bold tabular-nums">{{ c.pct }}%</p>
        <p class="text-xs text-muted">{{ entero(c.compras) }} unidades vendidas</p>
      </UCard>
    </div>

    <UCard>
      <div class="mb-3 flex flex-wrap items-center justify-between gap-2">
        <div>
          <p class="text-sm font-medium">Distribución porcentual de tallas por categoría</p>
          <p class="text-xs text-muted">Proporción sobre el 100% de las compras de cada categoría</p>
        </div>
        <UBadge color="neutral" variant="subtle" :label="`Variación máx. entre categorías: ±${diferencia.toFixed(1)} pts`" />
      </div>
      <GraficoBarras :etiquetas="categorias.map(es)" :series="series" horizontal apilado sufijo="%" :maximo="100" :alto="280" />
    </UCard>

    <template #confianza>
      <p>Muestra total de {{ entero((data ?? []).reduce((s, d) => s + d.compras, 0)) }} compras; la variación máxima entre categorías para una misma talla es de {{ diferencia.toFixed(1) }} puntos porcentuales.</p>
      <p>El dataset registra tallas S, M, L y XL (no incluye registros de XS ni XXL).</p>
    </template>

    <template #detalle>
      <table class="w-full text-sm">
        <thead class="text-left text-muted">
          <tr><th class="py-2">Categoría</th><th v-for="t in tallas" :key="t" class="text-right">{{ t }}</th></tr>
        </thead>
        <tbody>
          <tr v-for="c in categorias" :key="c" class="border-t border-default">
            <td class="py-2 font-medium">{{ es(c) }}</td>
            <td v-for="t in tallas" :key="t" class="text-right tabular-nums">{{ pct(c, t) }}%</td>
          </tr>
        </tbody>
      </table>
    </template>
  </SeccionRespuesta>
</template>
