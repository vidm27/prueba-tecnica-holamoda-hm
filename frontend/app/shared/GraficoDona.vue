<script setup lang="ts">
import { Doughnut } from 'vue-chartjs'
import type { ChartOptions } from 'chart.js'

const props = defineProps<{
  etiquetas: string[]
  valores: number[]
  colores?: string[]
  sufijo?: string
  alto?: number
  tituloCentro?: string
  subtituloCentro?: string
}>()

const PALETA = ['#e11d48', '#f59e0b', '#3b82f6', '#10b981', '#8b5cf6', '#06b6d4']

const datos = computed(() => ({
  labels: props.etiquetas,
  datasets: [
    {
      data: props.valores,
      backgroundColor: props.colores ?? props.etiquetas.map((_, i) => PALETA[i % PALETA.length]),
      borderWidth: 2,
      borderColor: 'rgba(24, 24, 27, 0.6)',
      hoverOffset: 6,
      borderRadius: 5,
      spacing: 2,
    },
  ],
}))

const opciones = computed<ChartOptions<'doughnut'>>(() => ({
  responsive: true,
  maintainAspectRatio: false,
  cutout: '66%',
  plugins: {
    legend: {
      position: 'bottom',
      labels: { usePointStyle: true, pointStyle: 'circle', padding: 14 },
    },
    tooltip: {
      backgroundColor: 'rgba(24, 24, 27, 0.94)',
      padding: 10,
      cornerRadius: 8,
      callbacks: {
        label: (c) => `${c.label}: ${c.formattedValue}${props.sufijo ?? ''}`,
      },
    },
  },
}))
</script>

<template>
  <div class="relative" :style="{ height: `${alto ?? 280}px` }">
    <Doughnut :data="datos" :options="opciones" />
    <div
      v-if="tituloCentro || subtituloCentro"
      class="pointer-events-none absolute inset-0 bottom-8 flex flex-col items-center justify-center text-center"
    >
      <span v-if="tituloCentro" class="text-2xl font-bold tabular-nums">{{ tituloCentro }}</span>
      <span v-if="subtituloCentro" class="text-xs text-muted">{{ subtituloCentro }}</span>
    </div>
  </div>
</template>
