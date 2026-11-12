<script setup lang="ts">
import type { TopEstado } from './useTopEstados'

const { data, isPending, error } = useTopEstados()
const porEstado = computed(() => new Map((data.value ?? []).map((e) => [e.estado, e])))
const confiables = computed(() => data.value?.filter((e) => e.muestra_suficiente) ?? [])
const elegido = ref<string | null>(null)
const detalle = computed<TopEstado | undefined>(() => porEstado.value.get(elegido.value ?? '') ?? confiables.value[0] ?? data.value?.[0])
const pct = (e: TopEstado) => Math.round((100 * e.ventas_producto) / e.ventas_estado)
</script>

<template>
  <SeccionRespuesta :cargando="isPending" :error="error">
    <template #respuesta>
      Solo {{ confiables.length }} de {{ data?.length }} estados tienen un producto líder claro:
      {{ confiables.map((e) => `${es(e.producto)} en ${e.estado}`).join(', ') }}.
    </template>
    <template #accion>
      En el resto las ventas están repartidas entre muchos productos: mantener el surtido completo y no armar surtidos distintos por estado.
    </template>

    <UCard>
      <p class="mb-3 text-sm text-muted">Toca un estado para ver su producto, talla y color más vendidos.</p>
      <div class="grid gap-6 md:grid-cols-[minmax(0,1fr)_18rem]">
        <div class="grid gap-1" style="grid-template-columns: repeat(11, minmax(0, 1fr))">
          <button v-for="(pos, nombre) in CUADRICULA" :key="nombre" type="button" :disabled="!porEstado.has(nombre)"
                  :title="nombre" :aria-label="nombre" :style="{ gridColumn: pos.col + 1, gridRow: pos.fila + 1 }"
                  class="aspect-square rounded text-xs font-semibold transition disabled:opacity-20"
                  :class="[
                    porEstado.get(nombre)?.muestra_suficiente ? 'bg-primary text-white' : 'bg-accented text-muted',
                    detalle?.estado === nombre ? 'ring-2 ring-neutral-400 ring-offset-2 ring-offset-default' : '',
                  ]"
                  @click="elegido = nombre">
            {{ pos.abrev }}
          </button>
        </div>
        <div v-if="detalle" class="space-y-3 rounded-lg border border-default p-4 text-sm">
          <p class="text-base font-semibold">{{ detalle.estado }}</p>
          <dl class="space-y-1">
            <div class="flex justify-between gap-2"><dt class="text-muted">Producto líder</dt><dd class="font-medium">{{ es(detalle.producto) }}</dd></div>
            <div class="flex justify-between gap-2"><dt class="text-muted">Talla más común</dt><dd class="font-medium">{{ detalle.talla }}</dd></div>
            <div class="flex justify-between gap-2"><dt class="text-muted">Color más común</dt><dd class="font-medium">{{ es(detalle.color) }}</dd></div>
          </dl>
          <p class="text-muted">{{ detalle.ventas_producto }} de {{ detalle.ventas_estado }} ventas del estado ({{ pct(detalle) }}%).</p>
          <UAlert v-if="!detalle.muestra_suficiente" color="warning" variant="subtle" icon="i-lucide-triangle-alert"
                  :description="detalle.productos_empatados > 1
                    ? `Empata con ${detalle.productos_empatados - 1} producto(s) más: no hay un líder real.`
                    : 'Pocas ventas: el líder puede cambiar con unas pocas compras.'" />
        </div>
      </div>
      <p class="mt-4 text-xs text-muted">
        <span class="inline-block size-3 rounded bg-primary align-middle" /> líder claro (10+ ventas, sin empate) ·
        <span class="inline-block size-3 rounded bg-accented align-middle" /> sin líder claro
      </p>
    </UCard>

    <template #confianza>
      <p>Cada estado tiene entre 60 y 100 ventas repartidas en 25 productos: el líder suele tener 5 a 8 ventas, y el segundo casi lo mismo.</p>
      <p>Un líder se considera claro con al menos 10 ventas y sin empate. La talla y el color del líder salen de aún menos ventas: tómalos como referencia.</p>
    </template>

    <template #detalle>
      <table class="w-full text-sm">
        <thead class="text-left text-muted">
          <tr><th class="py-2">Estado</th><th>Producto líder</th><th class="text-right">Ventas</th><th>Talla</th><th>Color</th><th>¿Claro?</th></tr>
        </thead>
        <tbody>
          <tr v-for="e in data" :key="e.estado" class="border-t border-default">
            <td class="py-2 font-medium">{{ e.estado }}</td>
            <td>{{ es(e.producto) }}</td>
            <td class="text-right">{{ e.ventas_producto }} / {{ e.ventas_estado }}</td>
            <td class="pl-3">{{ e.talla }}</td>
            <td>{{ es(e.color) }}</td>
            <td>{{ e.muestra_suficiente ? 'Sí' : e.productos_empatados > 1 ? 'Empate' : 'Pocas ventas' }}</td>
          </tr>
        </tbody>
      </table>
    </template>
  </SeccionRespuesta>
</template>
