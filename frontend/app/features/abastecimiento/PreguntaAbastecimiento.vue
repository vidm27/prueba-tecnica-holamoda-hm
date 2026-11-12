<script setup lang="ts">
import type { Estacionalidad } from './useEstacionalidad'

const { data, isPending, error } = useEstacionalidad()
const ORDEN = ['Spring', 'Summer', 'Fall', 'Winter']

const temporadas = computed(() => {
  const claves = new Set((data.value ?? []).flatMap((d) => Object.keys(d.ventas_por_temporada)))
  return [...claves].sort((a, b) => ORDEN.indexOf(a) - ORDEN.indexOf(b))
})
const valores = (e: Estacionalidad) => temporadas.value.map((t) => e.ventas_por_temporada[t] ?? 0)
/** Estacional de verdad: su concentración en una temporada no se explica por azar (chi² con Bonferroni). */
const esEstacional = (e: Estacionalidad) => chiCuadradoParejo(valores(e)) > CHI2_4_TEMPORADAS_25_PRODUCTOS
const estacionales = computed(() => data.value?.filter(esEstacional) ?? [])
/** Variación del pico sobre el promedio del producto, en %. */
const sobrePromedio = (e: Estacionalidad) => {
  const v = valores(e)
  const media = v.reduce((s, x) => s + x, 0) / v.length
  return Math.round((100 * (Math.max(...v) - media)) / media)
}

const celda = (e: Estacionalidad, t: string) => {
  const v = valores(e)
  const [min, max] = [Math.min(...v), Math.max(...v)]
  const x = max === min ? 0 : ((e.ventas_por_temporada[t] ?? 0) - min) / (max - min)
  return { background: `color-mix(in oklab, #2563eb ${Math.round(10 + x * 60)}%, transparent)` }
}
</script>

<template>
  <SeccionRespuesta :cargando="isPending" :error="error">
    <template #respuesta>
      <template v-if="estacionales.length">
        Solo {{ estacionales.map((e) => `${es(e.producto)} (pico en ${es(e.temporada_pico).toLowerCase()})`).join(', ') }}
        tiene{{ estacionales.length > 1 ? 'n' : '' }} una temporada claramente más fuerte. El resto se vende parejo todo el año.
      </template>
      <template v-else>Ningún producto tiene una temporada claramente más fuerte: se venden parejo todo el año.</template>
    </template>
    <template #accion>
      Abastece de forma constante en las cuatro temporadas. Los picos que se ven en la tabla son de pocas unidades y pueden ser azar.
    </template>

    <UCard>
      <p class="mb-3 text-sm text-muted">
        Unidades vendidas por temporada. Más oscuro = mejor temporada de ese producto; <strong>negrita</strong> = pico.
      </p>
      <div class="overflow-x-auto">
        <table class="w-full border-separate border-spacing-1 text-center text-sm">
          <thead class="text-muted">
            <tr>
              <th class="text-left font-normal">Producto</th>
              <th v-for="t in temporadas" :key="t" class="font-normal">{{ es(t) }}</th>
              <th class="font-normal">Pico vs. promedio</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="e in data" :key="e.producto">
              <td class="pr-2 text-left">{{ es(e.producto) }}</td>
              <td v-for="t in temporadas" :key="t" class="rounded px-2 py-1 tabular-nums" :style="celda(e, t)"
                  :class="t === e.temporada_pico ? 'font-bold' : ''">
                {{ e.ventas_por_temporada[t] ?? 0 }}
              </td>
              <td class="text-muted tabular-nums" :class="esEstacional(e) ? 'font-semibold text-primary' : ''">+{{ sobrePromedio(e) }}%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </UCard>

    <template #confianza>
      <p>Cada producto vende unas 40 unidades por temporada. A ese volumen, un pico de hasta ~30% sobre el promedio aparece por azar.</p>
      <p>Para marcar un producto como estacional se usa una prueba estadística (chi-cuadrado) corregida por revisar 25 productos a la vez.</p>
      <p>El dataset no tiene fechas: no se puede ver la tendencia año a año ni el momento exacto del pico.</p>
    </template>
  </SeccionRespuesta>
</template>
