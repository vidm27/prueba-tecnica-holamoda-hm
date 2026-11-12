<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import type { ChartOptions } from 'chart.js'

const props = defineProps<{
  etiquetas: string[]
  series: { nombre: string; datos: number[]; color?: string | string[] }[]
  horizontal?: boolean
  apilado?: boolean
  sufijo?: string
  alto?: number
  maximo?: number
  minimo?: number
}>()

const PALETA = ['#e11d48', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4']
const datos = computed(() => ({
  labels: props.etiquetas,
  datasets: props.series.map((s, i) => ({
    label: s.nombre,
    data: s.datos,
    backgroundColor: s.color ?? PALETA[i % PALETA.length],
    borderRadius: props.apilado ? 3 : 6,
    maxBarThickness: 36,
  })),
}))
const ejeValor = computed(() => ({
  stacked: props.apilado,
  beginAtZero: props.minimo === undefined,
  min: props.minimo,
  max: props.maximo,
  grid: { color: 'rgba(161, 161, 170, 0.12)' },
}))
const ejeCategoria = computed(() => ({
  stacked: props.apilado,
  grid: { display: false },
}))
const opciones = computed<ChartOptions<'bar'>>(() => ({
  indexAxis: props.horizontal ? 'y' : 'x',
  responsive: true,
  maintainAspectRatio: false,
  scales: props.horizontal
    ? { x: ejeValor.value, y: ejeCategoria.value }
    : { x: ejeCategoria.value, y: ejeValor.value },
  plugins: {
    legend: {
      display: props.series.length > 1,
      position: 'bottom',
      labels: { usePointStyle: true, pointStyle: 'rectRounded', padding: 16 },
    },
    tooltip: {
      backgroundColor: 'rgba(24, 24, 27, 0.92)',
      padding: 10,
      cornerRadius: 8,
      callbacks: { label: (c) => `${c.dataset.label}: ${c.formattedValue}${props.sufijo ?? ''}` },
    },
  },
}))
</script>

<template>
  <div :style="{ height: `${alto ?? 300}px` }"><Bar :data="datos" :options="opciones" /></div>
</template>
