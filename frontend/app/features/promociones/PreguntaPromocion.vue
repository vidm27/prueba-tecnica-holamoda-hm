<script setup lang="ts">
import { RECOMENDACIONES, type Recomendacion } from './usePromociones'

const { data, isPending, error } = usePromociones()
const filtro = ref<Recomendacion | null>(null)

const CUADRANTES: { clave: Recomendacion; icono: string; subtitulo: string; badge: 'success' | 'error' | 'warning' | 'neutral' }[] = [
  { clave: 'promocion_exposicion', icono: 'i-lucide-megaphone', subtitulo: 'Alta calificación · Bajas ventas', badge: 'success' },
  { clave: 'riesgo_reputacion', icono: 'i-lucide-shield-alert', subtitulo: 'Baja calificación · Altas ventas', badge: 'error' },
  { clave: 'revisar_producto', icono: 'i-lucide-wrench', subtitulo: 'Baja calificación · Bajas ventas', badge: 'warning' },
  { clave: 'mantener', icono: 'i-lucide-check-circle-2', subtitulo: 'Alta calificación · Altas ventas', badge: 'neutral' },
]

const porCuadrante = (r: Recomendacion) => data.value?.productos.filter((p) => p.recomendacion === r) ?? []
const productosFiltrados = computed(() =>
  (data.value?.productos ?? []).filter((p) => !filtro.value || p.recomendacion === filtro.value),
)
</script>

<template>
  <SeccionRespuesta :cargando="isPending" :error="error">
    <div v-if="data" class="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
      <button
        v-for="c in CUADRANTES"
        :key="c.clave"
        type="button"
        class="rounded-xl border p-4 text-left transition"
        :class="filtro === c.clave ? 'border-primary bg-elevated ring-2 ring-primary/40' : 'border-default bg-default/50 hover:bg-elevated/60'"
        @click="filtro = filtro === c.clave ? null : c.clave"
      >
        <div class="flex items-center justify-between gap-2">
          <div class="flex items-center gap-2">
            <span class="size-2.5 rounded-full" :style="{ background: RECOMENDACIONES[c.clave].color }" />
            <span class="text-sm font-semibold">{{ RECOMENDACIONES[c.clave].texto }}</span>
          </div>
          <UBadge :color="c.badge" variant="subtle" size="sm" :label="`${porCuadrante(c.clave).length} prod.`" />
        </div>
        <p class="mt-1 text-xs text-muted">{{ c.subtitulo }}</p>
        <div class="mt-3 flex flex-wrap gap-1">
          <UBadge
            v-for="p in porCuadrante(c.clave).slice(0, 4)"
            :key="p.producto"
            color="neutral"
            variant="soft"
            size="sm"
            :label="es(p.producto)"
          />
          <UBadge
            v-if="porCuadrante(c.clave).length > 4"
            color="neutral"
            variant="subtle"
            size="sm"
            :label="`+${porCuadrante(c.clave).length - 4}`"
          />
        </div>
      </button>
    </div>

    <UCard v-if="data">
      <div class="mb-3 flex flex-wrap items-center justify-between gap-2">
        <div>
          <p class="text-sm font-medium">Matriz de posicionamiento: Ventas vs. Calificación</p>
          <p class="text-xs text-muted">
            Corte por medianas ({{ data.mediana_ventas }} unidades vendidas · {{ data.mediana_calificacion.toFixed(2) }} ★). Haz clic en una tarjeta superior para filtrar cuadrantes.
          </p>
        </div>
        <UButton v-if="filtro" size="xs" color="neutral" variant="soft" icon="i-lucide-x" label="Ver todos los cuadrantes" @click="filtro = null" />
      </div>
      <MapaPromocion :datos="data" :filtro="filtro" />
    </UCard>

    <template #confianza>
      <p>Las calificaciones entre productos varían en décimas (±0.1): la matriz permite segmentar prioridades de exposición comercial y revisión de catálogo.</p>
      <p>{{ data?.advertencia }}</p>
      <p>Compras de mujeres con descuento registrado en el dataset: {{ data?.compras_mujeres_con_descuento }}.</p>
    </template>

    <template #detalle>
      <table class="w-full text-sm">
        <thead class="text-left text-muted">
          <tr>
            <th class="py-2">Producto</th>
            <th>Categoría</th>
            <th class="text-right">Vendidos</th>
            <th class="text-right">Calificación</th>
            <th class="pl-4">Cuadrante</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in productosFiltrados" :key="p.producto" class="border-t border-default">
            <td class="py-2 font-medium">{{ es(p.producto) }}</td>
            <td>{{ es(p.categoria) }}</td>
            <td class="text-right tabular-nums">{{ p.ventas }}</td>
            <td class="text-right tabular-nums">{{ p.calificacion.toFixed(2) }} ★</td>
            <td class="pl-4">
              <span class="mr-2 inline-block size-2.5 rounded-full" :style="{ background: RECOMENDACIONES[p.recomendacion].color }" />
              <span class="font-medium">{{ RECOMENDACIONES[p.recomendacion].texto }}</span>
              <span class="ml-1 text-xs text-muted">— {{ RECOMENDACIONES[p.recomendacion].accion }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </template>
  </SeccionRespuesta>
</template>
