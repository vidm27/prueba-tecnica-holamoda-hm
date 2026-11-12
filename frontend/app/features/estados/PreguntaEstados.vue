<script setup lang="ts">
import type { TopEstado } from './useTopEstados'

const { data, isPending, error } = useTopEstados()
const porEstado = computed(() => new Map((data.value ?? []).map((e) => [e.estado, e])))
const confiables = computed(() => data.value?.filter((e) => e.muestra_suficiente) ?? [])
const empatados = computed(() => data.value?.filter((e) => !e.muestra_suficiente && e.productos_empatados > 1) ?? [])
const elegido = ref<string | null>(null)
const detalle = computed<TopEstado | undefined>(() => porEstado.value.get(elegido.value ?? '') ?? confiables.value[0] ?? data.value?.[0])
const pct = (e: TopEstado) => Math.round((100 * e.ventas_producto) / e.ventas_estado)
</script>

<template>
  <SeccionRespuesta :cargando="isPending" :error="error">
    <div class="grid gap-4 sm:grid-cols-3">
      <UCard>
        <p class="text-xs font-medium tracking-wide text-muted uppercase">Estados cubiertos</p>
        <p class="mt-2 text-2xl font-bold tabular-nums">{{ data?.length ?? 0 }}</p>
        <p class="text-xs text-muted">Cobertura geográfica en EE. UU.</p>
      </UCard>
      <UCard>
        <p class="text-xs font-medium tracking-wide text-muted uppercase">Con producto líder claro</p>
        <div class="mt-2 flex items-baseline gap-2">
          <p class="text-2xl font-bold text-primary tabular-nums">{{ confiables.length }}</p>
          <span class="text-xs text-muted">estados (≥10 uds, sin empate)</span>
        </div>
        <p class="mt-1 truncate text-xs text-muted">{{ confiables.map((e) => e.estado).join(', ') }}</p>
      </UCard>
      <UCard>
        <p class="text-xs font-medium tracking-wide text-muted uppercase">Con empate en el 1.er lugar</p>
        <p class="mt-2 text-2xl font-bold tabular-nums">{{ empatados.length }}</p>
        <p class="text-xs text-muted">Estados con múltiples productos empatados</p>
      </UCard>
    </div>

    <UCard>
      <div class="mb-4 flex flex-wrap items-center justify-between gap-2">
        <div>
          <p class="text-sm font-medium">Mapa interactivo de demanda por estado</p>
          <p class="text-xs text-muted">Selecciona cualquier estado para inspeccionar su producto más vendido, talla, color y tamaño de muestra</p>
        </div>
      </div>
      <div class="grid gap-6 md:grid-cols-[minmax(0,1fr)_19rem]">
        <div class="grid gap-1.5" style="grid-template-columns: repeat(11, minmax(0, 1fr))">
          <button v-for="(pos, nombre) in CUADRICULA" :key="nombre" type="button" :disabled="!porEstado.has(nombre)"
                  :title="nombre" :aria-label="nombre" :style="{ gridColumn: pos.col + 1, gridRow: pos.fila + 1 }"
                  class="aspect-square rounded-md text-xs font-semibold transition disabled:opacity-20"
                  :class="[
                    porEstado.get(nombre)?.muestra_suficiente ? 'bg-primary text-white shadow-sm' : 'bg-accented/80 text-muted hover:bg-accented',
                    detalle?.estado === nombre ? 'ring-2 ring-primary ring-offset-2 ring-offset-default' : '',
                  ]"
                  @click="elegido = nombre">
            {{ pos.abrev }}
          </button>
        </div>
        <div v-if="detalle" class="space-y-3 rounded-xl border border-default bg-elevated/40 p-4 text-sm">
          <div class="flex items-center justify-between gap-2">
            <p class="text-base font-bold">{{ detalle.estado }}</p>
            <UBadge :color="detalle.muestra_suficiente ? 'primary' : 'neutral'" variant="subtle" size="sm"
                    :label="detalle.muestra_suficiente ? 'Líder claro' : 'Muestra dispersa'" />
          </div>
          <dl class="space-y-2 border-t border-default pt-3">
            <div class="flex justify-between gap-2"><dt class="text-muted">Producto líder</dt><dd class="font-semibold">{{ es(detalle.producto) }}</dd></div>
            <div class="flex justify-between gap-2"><dt class="text-muted">Talla más común</dt><dd class="font-medium">{{ detalle.talla }}</dd></div>
            <div class="flex justify-between gap-2"><dt class="text-muted">Color más común</dt><dd class="font-medium">{{ es(detalle.color) }}</dd></div>
            <div class="flex justify-between gap-2"><dt class="text-muted">Participación</dt><dd class="font-medium tabular-nums">{{ detalle.ventas_producto }} / {{ detalle.ventas_estado }} ({{ pct(detalle) }}%)</dd></div>
          </dl>
          <UAlert v-if="!detalle.muestra_suficiente" color="warning" variant="subtle" icon="i-lucide-triangle-alert"
                  :description="detalle.productos_empatados > 1
                    ? `Empata con ${detalle.productos_empatados - 1} producto(s) adicional(es) en el primer lugar.`
                    : 'Menos de 10 unidades del producto líder en el estado.'" />
        </div>
      </div>
      <p class="mt-4 flex items-center gap-4 text-xs text-muted">
        <span class="flex items-center gap-1.5"><span class="inline-block size-3 rounded bg-primary" /> Líder estadísticamente claro (≥10 ventas, sin empate)</span>
        <span class="flex items-center gap-1.5"><span class="inline-block size-3 rounded bg-accented" /> Ventas fragmentadas entre múltiples productos</span>
      </p>
    </UCard>

    <template #confianza>
      <p>Cada estado registra entre 60 y 100 compras distribuidas entre 25 productos (promedio de 3 a 4 unidades por producto y estado).</p>
      <p>Se exige un umbral mínimo de 10 ventas del producto líder y ausencia de empates para clasificar un estado con liderazgo claro.</p>
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
