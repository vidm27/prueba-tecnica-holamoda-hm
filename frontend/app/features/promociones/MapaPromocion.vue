<!-- Dispersión ventas × calificación con las medianas como cuadrantes. -->
<script setup lang="ts">
import { Scatter } from 'vue-chartjs'
import type { ChartOptions } from 'chart.js'
import { RECOMENDACIONES, type Promociones, type Recomendacion } from './usePromociones'

const props = defineProps<{ datos: Promociones }>()

const datos = computed(() => {
  const p = props.datos.productos
  const [x0, x1] = [Math.min(...p.map((d) => d.ventas)) - 5, Math.max(...p.map((d) => d.ventas)) + 5]
  const [y0, y1] = [Math.min(...p.map((d) => d.calificacion)) - 0.03, Math.max(...p.map((d) => d.calificacion)) + 0.03]
  const linea = (puntos: { x: number; y: number }[]) => ({
    label: '', data: puntos, showLine: true, borderColor: '#71717a', borderDash: [4, 4], borderWidth: 1, pointRadius: 0,
  })
  return {
    datasets: [
      ...(Object.keys(RECOMENDACIONES) as Recomendacion[]).map((r) => ({
        label: RECOMENDACIONES[r].texto,
        backgroundColor: RECOMENDACIONES[r].color,
        pointRadius: 7,
        pointHoverRadius: 9,
        data: p.filter((d) => d.recomendacion === r).map((d) => ({ x: d.ventas, y: d.calificacion, nombre: es(d.producto) })),
      })),
      linea([{ x: props.datos.mediana_ventas, y: y0 }, { x: props.datos.mediana_ventas, y: y1 }]),
      linea([{ x: x0, y: props.datos.mediana_calificacion }, { x: x1, y: props.datos.mediana_calificacion }]),
    ],
  }
})

const opciones: ChartOptions<'scatter'> = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    x: { title: { display: true, text: 'Unidades vendidas →' } },
    y: { title: { display: true, text: 'Calificación de clientes (1–5) →' } },
  },
  plugins: {
    legend: { position: 'bottom', labels: { filter: (l) => !!l.text } },
    tooltip: {
      filter: (c) => !!c.dataset.label,
      callbacks: { label: (c) => { const r = c.raw as { x: number; y: number; nombre: string }; return `${r.nombre}: ${r.x} vendidos · ${r.y} ★` } },
    },
  },
}
</script>

<template>
  <div class="relative h-96">
    <Scatter :data="datos" :options="opciones" />
    <span class="pointer-events-none absolute top-2 left-16 rounded bg-success/10 px-2 py-0.5 text-xs text-success">Gusta, se vende poco → promover</span>
  </div>
</template>
