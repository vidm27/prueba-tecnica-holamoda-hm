<script setup lang="ts">
const { data, isPending, error } = useTallas()
const ORDEN = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
const COLORES = ['#fca5a5', '#f87171', '#dc2626', '#991b1b', '#450a0a', '#000000']

const tallas = computed(() => [...new Set((data.value ?? []).map((d) => d.talla))].sort((a, b) => ORDEN.indexOf(a) - ORDEN.indexOf(b)))
const categorias = computed(() => [...new Set((data.value ?? []).map((d) => d.categoria))])
const pct = (c: string, t: string) => data.value?.find((d) => d.categoria === c && d.talla === t)?.pct ?? 0

/** Curva general: % de todas las compras por talla. */
const curva = computed(() => {
  const total = (data.value ?? []).reduce((s, d) => s + d.compras, 0)
  return tallas.value.map((t) => ({
    talla: t,
    pct: Math.round((100 * (data.value ?? []).filter((d) => d.talla === t).reduce((s, d) => s + d.compras, 0)) / Math.max(1, total)),
  }))
})
/** Mayor diferencia entre categorías para una misma talla, en puntos porcentuales. */
const diferencia = computed(() => Math.max(0, ...tallas.value.map((t) => {
  const v = categorias.value.map((c) => pct(c, t))
  return Math.max(...v) - Math.min(...v)
})))

const series = computed(() => tallas.value.map((t, i) => ({
  nombre: t, color: COLORES[i], datos: categorias.value.map((c) => pct(c, t)),
})))
</script>

<template>
  <SeccionRespuesta :cargando="isPending" :error="error">
    <template #respuesta>
      Compra con la misma curva en todas las categorías:
      <span v-for="(c, i) in curva" :key="c.talla">{{ c.talla }} {{ c.pct }}%<span v-if="i < curva.length - 1">, </span></span>.
    </template>
    <template #accion>
      De cada 10 unidades: unas {{ Math.round((curva.find((c) => c.talla === 'M')?.pct ?? 0) / 10) }} en talla M.
      No hacen falta curvas distintas por categoría.
    </template>

    <UCard>
      <p class="mb-2 text-sm text-muted">Cómo se reparten las compras de cada categoría entre tallas (cada barra suma 100%).</p>
      <GraficoBarras :etiquetas="categorias.map(es)" :series="series" horizontal apilado sufijo="%" :maximo="100" :alto="260" />
    </UCard>

    <template #confianza>
      <p>Alta. Son {{ entero((data ?? []).reduce((s, d) => s + d.compras, 0)) }} compras y la curva cambia como máximo {{ diferencia.toFixed(1) }} puntos entre categorías.</p>
      <p>El dataset no tiene tallas XS ni XXL: no hay datos para decidir si conviene ofrecerlas.</p>
    </template>

    <template #detalle>
      <table class="w-full text-sm">
        <thead class="text-left text-muted">
          <tr><th class="py-2">Categoría</th><th v-for="t in tallas" :key="t" class="text-right">{{ t }}</th></tr>
        </thead>
        <tbody>
          <tr v-for="c in categorias" :key="c" class="border-t border-default">
            <td class="py-2 font-medium">{{ es(c) }}</td>
            <td v-for="t in tallas" :key="t" class="text-right">{{ pct(c, t) }}%</td>
          </tr>
        </tbody>
      </table>
    </template>
  </SeccionRespuesta>
</template>
