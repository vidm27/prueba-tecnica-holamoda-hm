<script setup lang="ts">
import { Bar } from 'vue-chartjs'
import type { ChartOptions } from 'chart.js'

const props = defineProps<{
  etiquetas: string[]
  series: { nombre: string; datos: number[]; color?: string }[]
  horizontal?: boolean
  apilado?: boolean
  sufijo?: string
  alto?: number
  maximo?: number
}>()

const PALETA = ['#dc2626', '#2563eb', '#16a34a', '#d97706', '#7c3aed', '#0891b2']
const datos = computed(() => ({
  labels: props.etiquetas,
  datasets: props.series.map((s, i) => ({ label: s.nombre, data: s.datos, backgroundColor: s.color ?? PALETA[i % PALETA.length] })),
}))
const eje = computed(() => ({ stacked: props.apilado, beginAtZero: true, max: props.maximo }))
const opciones = computed<ChartOptions<'bar'>>(() => ({
  indexAxis: props.horizontal ? 'y' : 'x',
  responsive: true,
  maintainAspectRatio: false,
  scales: props.horizontal ? { x: eje.value, y: { stacked: props.apilado } } : { x: { stacked: props.apilado }, y: eje.value },
  plugins: {
    legend: { display: props.series.length > 1, position: 'bottom' },
    tooltip: { callbacks: { label: (c) => `${c.dataset.label}: ${c.formattedValue}${props.sufijo ?? ''}` } },
  },
}))
</script>

<template>
  <div :style="{ height: `${alto ?? 300}px` }"><Bar :data="datos" :options="opciones" /></div>
</template>
