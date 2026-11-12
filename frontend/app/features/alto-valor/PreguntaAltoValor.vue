<script setup lang="ts">
const { data, isPending, error } = useValor()
const niveles = computed(() => data.value?.niveles ?? [])
const totalClientes = computed(() => niveles.value.reduce((s, n) => s + n.clientes, 0))
const pctClientes = (n: { clientes: number }) => Math.round((100 * n.clientes) / Math.max(1, totalClientes.value))
const top = computed(() => niveles.value.at(-1))
const series = computed(() => [
  { nombre: '% de los clientes', color: '#94a3b8', datos: niveles.value.map(pctClientes) },
  { nombre: '% del gasto anual estimado', color: '#e11d48', datos: niveles.value.map((n) => n.pct_gasto) },
])
</script>

<template>
  <SeccionRespuesta :cargando="isPending" :error="error">
    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <UCard v-for="n in niveles" :key="n.nivel" :class="n.nivel === top?.nivel ? 'ring-2 ring-primary/50' : ''">
        <div class="flex items-center justify-between">
          <span class="text-xs font-semibold tracking-wide text-muted uppercase">Nivel {{ n.nivel }}</span>
          <UBadge :color="n.nivel === top?.nivel ? 'primary' : 'neutral'" variant="subtle" size="sm" :label="`${pctClientes(n)}% clientes`" />
        </div>
        <p class="mt-2 text-2xl font-bold tabular-nums">{{ n.pct_gasto }}%</p>
        <p class="text-xs text-muted">del gasto anual ({{ moneda(n.gasto_minimo) }} – {{ moneda(n.gasto_maximo) }})</p>
      </UCard>
    </div>

    <UCard>
      <div class="mb-3 flex flex-wrap items-center justify-between gap-2">
        <div>
          <p class="text-sm font-medium">Concentración del gasto anual por cuartil de valor</p>
          <p class="text-xs text-muted">Comparativa entre la proporción de clientes (25% por cuartil) y su aporte al ingreso anual estimado</p>
        </div>
        <UBadge v-if="data" color="primary" variant="subtle" :label="`Top 20% concentra el ${data.pareto_top20_pct_gasto}% del gasto`" />
      </div>
      <GraficoBarras :etiquetas="niveles.map((n) => n.nivel)" :series="series" sufijo="%" :alto="300" />
    </UCard>

    <template #confianza>
      <p>El gasto anual estimado se calcula como `monto_compra × compras_anuales_según_frecuencia`, abarcando desde {{ moneda(niveles[0]?.gasto_minimo ?? 0) }} hasta {{ moneda(top?.gasto_maximo ?? 0) }}.</p>
      <p>La segmentación por cuartiles de valor muestra cómo el 20% superior de clientes concentra el {{ data?.pareto_top20_pct_gasto }}% del gasto anual.</p>
    </template>

    <template #detalle>
      <table class="w-full text-sm">
        <thead class="text-left text-muted">
          <tr><th class="py-2">Nivel</th><th class="text-right">Clientes</th><th class="text-right">Rango anual por cliente</th><th class="text-right">Gasto anual total</th><th class="text-right">% del gasto</th></tr>
        </thead>
        <tbody>
          <tr v-for="n in niveles" :key="n.nivel" class="border-t border-default">
            <td class="py-2 font-medium">{{ n.nivel }}</td>
            <td class="text-right tabular-nums">{{ entero(n.clientes) }}</td>
            <td class="text-right tabular-nums">{{ moneda(n.gasto_minimo) }} – {{ moneda(n.gasto_maximo) }}</td>
            <td class="text-right tabular-nums">{{ moneda(n.gasto_anual_total) }}</td>
            <td class="text-right font-semibold tabular-nums">{{ n.pct_gasto }}%</td>
          </tr>
        </tbody>
      </table>
    </template>
  </SeccionRespuesta>
</template>
