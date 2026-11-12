<script setup lang="ts">
import { RECOMENDACIONES, type GeneroPromocion, type Recomendacion } from './usePromociones'

const genero = ref<GeneroPromocion>('Todos')
const { data, isPending, error } = usePromociones(genero)
const filtro = ref<Recomendacion | null>(null)

const GENEROS: { valor: GeneroPromocion; label: string; icono: string; nota: string }[] = [
  { valor: 'Todos', label: 'Todos los clientes', icono: 'i-lucide-users', nota: 'Catálogo general (3,900 compras)' },
  { valor: 'Female', label: 'Mujeres', icono: 'i-lucide-sparkles', nota: '0% con descuento hoy · Oportunidad virgen' },
  { valor: 'Male', label: 'Hombres', icono: 'i-lucide-user', nota: 'Concentran el 100% de descuentos actuales' },
]

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
  <SeccionRespuesta :cargando="isPending && !data" :error="error">
    <!-- Barra de filtro por género: qué productos tienen oportunidad de promoción según el público -->
    <div v-if="data" class="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-default bg-elevated/40 p-3">
      <div class="flex items-center gap-2.5">
        <div class="flex size-8 items-center justify-center rounded-lg bg-primary/10 text-primary">
          <UIcon name="i-lucide-venus-and-mars" class="size-4" />
        </div>
        <div>
          <p class="text-xs font-semibold">Oportunidades de promoción y posicionamiento por género</p>
          <p class="text-[11px] text-muted">
            {{ GENEROS.find((g) => g.valor === genero)?.nota }}
            <span v-if="genero === 'Female'" class="font-medium text-primary">
              — Ideal para lanzar primeras campañas de visibilidad y descuento
            </span>
          </p>
        </div>
      </div>

      <div class="flex flex-wrap items-center gap-1.5">
        <UButton
          v-for="g in GENEROS"
          :key="g.valor"
          size="xs"
          :color="genero === g.valor ? 'primary' : 'neutral'"
          :variant="genero === g.valor ? 'solid' : 'soft'"
          :icon="g.icono"
          :label="g.label"
          @click="genero = g.valor"
        />
      </div>
    </div>

    <!-- Tarjetas de cuadrantes (clicables como filtros) -->
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

    <!-- Matriz con tags interactivos dentro del gráfico y en la cabecera -->
    <UCard v-if="data">
      <div class="mb-3 flex flex-wrap items-center justify-between gap-2">
        <div>
          <p class="text-sm font-medium">
            Matriz de posicionamiento: Ventas vs. Calificación
            <span v-if="genero !== 'Todos'" class="text-primary">({{ genero === 'Female' ? 'Mujeres' : 'Hombres' }})</span>
          </p>
          <p class="text-xs text-muted">
            Corte por medianas ({{ data.mediana_ventas }} unidades vendidas · {{ data.mediana_calificacion.toFixed(2) }} ★). Haz clic en las etiquetas dentro del gráfico o arriba para filtrar.
          </p>
        </div>

        <div class="flex flex-wrap items-center gap-1.5">
          <UBadge
            v-if="genero === 'Female'"
            color="primary"
            variant="subtle"
            size="sm"
            icon="i-lucide-tag"
            label="0% descuentos previos en mujeres"
          />
          <UButton
            v-if="filtro || genero !== 'Todos'"
            size="xs"
            color="neutral"
            variant="soft"
            icon="i-lucide-rotate-ccw"
            label="Restablecer filtros"
            @click="filtro = null; genero = 'Todos'"
          />
        </div>
      </div>

      <MapaPromocion :datos="data" :filtro="filtro" @filtrar="filtro = $event" />
    </UCard>

    <template #confianza>
      <p>Las calificaciones entre productos varían en décimas (±0.1): la matriz permite segmentar prioridades de exposición comercial y revisión de catálogo por género.</p>
      <p>{{ data?.advertencia }}</p>
      <p>Compras de mujeres con descuento registrado en el dataset: {{ data?.compras_mujeres_con_descuento }} (el 100% de los descuentos históricos se concentró en hombres).</p>
    </template>

    <template #detalle>
      <table class="w-full text-sm">
        <thead class="text-left text-muted">
          <tr>
            <th class="py-2">Producto</th>
            <th>Categoría</th>
            <th class="text-right">Vendidos</th>
            <th class="text-right">Calificación</th>
            <th class="text-right">% Mujeres</th>
            <th class="text-right">% con desc.</th>
            <th class="pl-4">Cuadrante</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in productosFiltrados" :key="p.producto" class="border-t border-default">
            <td class="py-2 font-medium">{{ es(p.producto) }}</td>
            <td>{{ es(p.categoria) }}</td>
            <td class="text-right tabular-nums">{{ p.ventas }}</td>
            <td class="text-right tabular-nums">{{ p.calificacion.toFixed(2) }} ★</td>
            <td class="text-right tabular-nums">{{ fraccion(p.pct_mujeres, 0) }}</td>
            <td class="text-right tabular-nums">{{ fraccion(p.pct_descuento, 0) }}</td>
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
