<script setup lang="ts">
import type { Satisfaccion } from './useSatisfaccion'

const { data, isPending, error } = useSatisfaccion()
const promedio = computed(() => {
  const d = data.value ?? []
  return d.reduce((s, p) => s + p.calificacion * p.compras, 0) / Math.max(1, d.reduce((s, p) => s + p.compras, 0))
})
/** "Peor" de verdad solo si, incluso sumando su margen de error, queda bajo el promedio. */
const claramentePeor = (p: Satisfaccion) => p.calificacion + p.margen_error_95 < promedio.value
const peores = computed(() => data.value?.filter(claramentePeor) ?? [])
const todos = ref(false)
const visibles = computed(() => (todos.value ? data.value : data.value?.slice(0, 10)) ?? [])
// Escala del gráfico: solo el rango donde están los datos, para que las diferencias se vean.
const [MIN, MAX] = [3.4, 4.1]
const pos = (v: number) => `${((Math.min(MAX, Math.max(MIN, v)) - MIN) / (MAX - MIN)) * 100}%`
</script>

<template>
  <SeccionRespuesta :cargando="isPending" :error="error">
    <template #respuesta>
      <template v-if="peores.length">
        {{ peores.map((p) => es(p.producto)).join(', ') }} {{ peores.length === 1 ? 'es el único producto' : 'son los productos' }}
        con satisfacción claramente por debajo del promedio ({{ promedio.toFixed(2) }} / 5).
      </template>
      <template v-else>Ningún producto está claramente por debajo del promedio ({{ promedio.toFixed(2) }} / 5).</template>
    </template>
    <template #accion>
      El resto de productos está dentro del margen de error: sus diferencias pueden ser azar. Revisa primero los marcados en rojo.
    </template>

    <UCard>
      <p class="mb-4 text-sm text-muted">
        Calificación promedio de cada producto (punto) con su margen de error (barra). La línea vertical es el promedio general.
        Peor primero.
      </p>
      <ul class="space-y-2 text-sm">
        <li v-for="p in visibles" :key="p.producto" class="grid grid-cols-[8rem_1fr_4rem] items-center gap-3">
          <span class="truncate" :class="claramentePeor(p) ? 'font-semibold text-error' : ''">{{ es(p.producto) }}</span>
          <div class="relative h-6">
            <div class="absolute inset-y-0 w-px bg-neutral-400" :style="{ left: pos(promedio) }" />
            <div class="absolute top-1/2 h-1.5 -translate-y-1/2 rounded-full" :class="claramentePeor(p) ? 'bg-error/40' : 'bg-neutral-400/30'"
                 :style="{ left: pos(p.calificacion - p.margen_error_95), width: `calc(${pos(p.calificacion + p.margen_error_95)} - ${pos(p.calificacion - p.margen_error_95)})` }" />
            <div class="absolute top-1/2 size-3 -translate-x-1/2 -translate-y-1/2 rounded-full" :class="claramentePeor(p) ? 'bg-error' : 'bg-neutral-400'"
                 :style="{ left: pos(p.calificacion) }" />
          </div>
          <span class="text-right tabular-nums">{{ p.calificacion.toFixed(2) }}</span>
        </li>
      </ul>
      <div class="mt-1 grid grid-cols-[8rem_1fr_4rem] gap-3 text-xs text-muted">
        <span /><div class="flex justify-between"><span>{{ MIN }}</span><span>{{ MAX }}</span></div><span />
      </div>
      <UButton class="mt-3" variant="link" size="sm" :label="todos ? 'Ver solo los 10 peores' : `Ver los ${data?.length} productos`" @click="todos = !todos" />
    </UCard>

    <template #confianza>
      <p>Cada producto tiene entre 120 y 170 calificaciones; con eso, el margen de error es de ±0.1 puntos.</p>
      <p>Si la barra de un producto toca la línea del promedio, no se puede afirmar que gusta menos que el resto.</p>
    </template>

    <template #detalle>
      <table class="w-full text-sm">
        <thead class="text-left text-muted">
          <tr><th class="py-2">Producto</th><th>Categoría</th><th class="text-right">Calificaciones</th><th class="text-right">Promedio</th><th class="text-right">Margen ±</th></tr>
        </thead>
        <tbody>
          <tr v-for="p in data" :key="p.producto" class="border-t border-default">
            <td class="py-2 font-medium">{{ es(p.producto) }}</td>
            <td>{{ es(p.categoria) }}</td>
            <td class="text-right">{{ p.compras }}</td>
            <td class="text-right">{{ p.calificacion.toFixed(2) }}</td>
            <td class="text-right">{{ p.margen_error_95.toFixed(2) }}</td>
          </tr>
        </tbody>
      </table>
    </template>
  </SeccionRespuesta>
</template>
