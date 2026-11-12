<!-- Dispersión ventas × calificación con las medianas como cuadrantes y etiquetas clicables para filtrar. -->
<script setup lang="ts">
import { Scatter } from 'vue-chartjs'
import type { ChartOptions } from 'chart.js'
import { RECOMENDACIONES, type Promociones, type Recomendacion } from './usePromociones'

const props = defineProps<{ datos: Promociones; filtro?: Recomendacion | null }>()
const emit = defineEmits<{ (e: 'filtrar', r: Recomendacion | null): void }>()

const alternar = (r: Recomendacion) => {
  emit('filtrar', props.filtro === r ? null : r)
}

const ORDEN_CUADRANTES: Recomendacion[] = ['promocion_exposicion', 'riesgo_reputacion', 'revisar_producto', 'mantener']

const datos = computed(() => {
  const p = props.datos.productos
  const [x0, x1] = [Math.min(...p.map((d) => d.ventas)) - 6, Math.max(...p.map((d) => d.ventas)) + 6]
  const [y0, y1] = [Math.min(...p.map((d) => d.calificacion)) - 0.04, Math.max(...p.map((d) => d.calificacion)) + 0.04]
  const linea = (puntos: { x: number; y: number }[]) => ({
    label: '',
    data: puntos,
    showLine: true,
    borderColor: 'rgba(161, 161, 170, 0.45)',
    borderDash: [6, 4],
    borderWidth: 1.5,
    pointRadius: 0,
  })
  return {
    datasets: [
      ...ORDEN_CUADRANTES.map((r) => {
        const activo = !props.filtro || props.filtro === r
        return {
          label: RECOMENDACIONES[r].texto,
          backgroundColor: activo ? RECOMENDACIONES[r].color : 'rgba(161, 161, 170, 0.2)',
          borderColor: activo ? '#ffffff' : 'transparent',
          borderWidth: activo ? 1.5 : 0,
          pointRadius: activo ? 8 : 5,
          pointHoverRadius: 11,
          data: p
            .filter((d) => d.recomendacion === r)
            .map((d) => ({
              x: d.ventas,
              y: d.calificacion,
              nombre: es(d.producto),
              categoria: es(d.categoria),
              accion: RECOMENDACIONES[r].texto,
            })),
        }
      }),
      linea([{ x: props.datos.mediana_ventas, y: y0 }, { x: props.datos.mediana_ventas, y: y1 }]),
      linea([{ x: x0, y: props.datos.mediana_calificacion }, { x: x1, y: props.datos.mediana_calificacion }]),
    ],
  }
})

const opciones: ChartOptions<'scatter'> = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    x: {
      title: { display: true, text: 'Unidades vendidas →' },
      grid: { color: 'rgba(161, 161, 170, 0.1)' },
    },
    y: {
      title: { display: true, text: 'Calificación promedio (1–5 ★) →' },
      grid: { color: 'rgba(161, 161, 170, 0.1)' },
    },
  },
  plugins: {
    legend: {
      position: 'bottom',
      labels: { filter: (l) => !!l.text, usePointStyle: true, padding: 16 },
    },
    tooltip: {
      backgroundColor: 'rgba(24, 24, 27, 0.94)',
      padding: 12,
      cornerRadius: 8,
      filter: (c) => !!c.dataset.label,
      callbacks: {
        label: (c) => {
          const r = c.raw as { x: number; y: number; nombre: string; categoria: string; accion: string }
          return `${r.nombre} (${r.categoria}): ${r.x} uds · ${r.y.toFixed(2)} ★ [${r.accion}]`
        },
      },
    },
  },
}
</script>

<template>
  <div class="relative h-96">
    <Scatter :data="datos" :options="opciones" />
    <button
      type="button"
      class="absolute top-2 left-14 cursor-pointer rounded-md border px-2.5 py-1 text-xs font-medium transition select-none"
      :class="
        filtro === 'promocion_exposicion'
          ? 'border-success bg-success text-white shadow-sm ring-2 ring-success/40'
          : 'border-success/30 bg-success/10 text-success hover:bg-success/20'
      "
      @click="alternar('promocion_exposicion')"
    >
      ↖ Alta calificación · Bajas ventas (Promover)
    </button>
    <button
      type="button"
      class="absolute top-2 right-3 hidden cursor-pointer rounded-md border px-2.5 py-1 text-xs font-medium transition select-none sm:inline-block"
      :class="
        filtro === 'mantener'
          ? 'border-primary bg-primary text-white shadow-sm ring-2 ring-primary/40'
          : 'border-default bg-elevated/90 text-muted hover:bg-elevated hover:text-default'
      "
      @click="alternar('mantener')"
    >
      ↗ Alta calificación · Altas ventas (Mantener)
    </button>
    <button
      type="button"
      class="absolute bottom-12 left-14 hidden cursor-pointer rounded-md border px-2.5 py-1 text-xs font-medium transition select-none sm:inline-block"
      :class="
        filtro === 'revisar_producto'
          ? 'border-warning bg-warning text-white shadow-sm ring-2 ring-warning/40'
          : 'border-warning/30 bg-warning/10 text-warning hover:bg-warning/20'
      "
      @click="alternar('revisar_producto')"
    >
      ↙ Baja calificación · Bajas ventas (Revisar)
    </button>
    <button
      type="button"
      class="absolute right-3 bottom-12 hidden cursor-pointer rounded-md border px-2.5 py-1 text-xs font-medium transition select-none sm:inline-block"
      :class="
        filtro === 'riesgo_reputacion'
          ? 'border-error bg-error text-white shadow-sm ring-2 ring-error/40'
          : 'border-error/30 bg-error/10 text-error hover:bg-error/20'
      "
      @click="alternar('riesgo_reputacion')"
    >
      ↘ Baja calificación · Altas ventas (Cuidar)
    </button>
  </div>
</template>
