<script setup lang="ts">
const { data, isPending, error } = useSuscripcion()
const si = computed(() => data.value?.find((d) => d.suscrito))
const no = computed(() => data.value?.find((d) => !d.suscrito))
const UMBRAL = 0.05 // diferencias menores al 5% se tratan como "igual"

const metricas = computed(() => si.value && no.value ? [
  { nombre: 'Gasto por compra', icono: 'i-lucide-receipt', a: si.value.ticket_promedio, b: no.value.ticket_promedio, fmt: moneda },
  { nombre: 'Gasto anual estimado', icono: 'i-lucide-wallet', a: si.value.gasto_anual_promedio, b: no.value.gasto_anual_promedio, fmt: moneda },
  { nombre: 'Compras previas', icono: 'i-lucide-repeat', a: si.value.compras_previas_promedio, b: no.value.compras_previas_promedio, fmt: (n: number) => n.toFixed(1) },
  { nombre: 'Calificación promedio', icono: 'i-lucide-star', a: si.value.calificacion_promedio, b: no.value.calificacion_promedio, fmt: (n: number) => `${n.toFixed(2)} ★` },
].map((m) => ({ ...m, delta: m.a / m.b - 1 })) : [])

const seriesComparativas = computed(() => si.value && no.value ? [
  {
    nombre: `Suscritos (${entero(si.value.clientes)})`,
    color: '#e11d48',
    datos: [
      +si.value.ticket_promedio.toFixed(1),
      +si.value.compras_previas_promedio.toFixed(1),
      +(si.value.calificacion_promedio * 10).toFixed(1),
    ],
  },
  {
    nombre: `No suscritos (${entero(no.value.clientes)})`,
    color: '#64748b',
    datos: [
      +no.value.ticket_promedio.toFixed(1),
      +no.value.compras_previas_promedio.toFixed(1),
      +(no.value.calificacion_promedio * 10).toFixed(1),
    ],
  },
] : [])
</script>

<template>
  <SeccionRespuesta :cargando="isPending" :error="error">
    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <UCard v-for="m in metricas" :key="m.nombre">
        <div class="flex items-center justify-between">
          <p class="text-xs font-medium tracking-wide text-muted uppercase">{{ m.nombre }}</p>
          <UIcon :name="m.icono" class="size-4 text-primary" />
        </div>
        <div class="mt-3 flex items-end justify-between gap-3">
          <div>
            <p class="text-xs text-muted">Suscritos</p>
            <p class="text-xl font-bold tabular-nums">{{ m.fmt(m.a) }}</p>
          </div>
          <div class="text-right">
            <p class="text-xs text-muted">No suscritos</p>
            <p class="text-xl font-semibold text-muted tabular-nums">{{ m.fmt(m.b) }}</p>
          </div>
        </div>
        <div class="mt-3 border-t border-default pt-2.5">
          <UBadge
            variant="subtle"
            size="sm"
            :color="Math.abs(m.delta) < UMBRAL ? 'neutral' : m.delta > 0 ? 'success' : 'error'"
            :label="`Diferencia: ${m.delta > 0 ? '+' : ''}${fraccion(m.delta, 1)}`"
          />
        </div>
      </UCard>
    </div>

    <UCard v-if="seriesComparativas.length">
      <div class="mb-3">
        <p class="text-sm font-medium">Comparativa directa: Suscritos vs. No suscritos</p>
        <p class="text-xs text-muted">Contraste de ticket promedio (USD), compras previas y calificación (escala ×10 para visualización conjunta)</p>
      </div>
      <GraficoBarras
        :etiquetas="['Ticket promedio (USD)', 'Compras previas', 'Calificación (×10)']"
        :series="seriesComparativas"
        :alto="260"
      />
    </UCard>

    <template #confianza>
      <p>Muestra compuesta por {{ entero(si?.clientes ?? 0) }} clientes suscritos y {{ entero(no?.clientes ?? 0) }} no suscritos; variaciones inferiores al 5% se encuentran dentro del ruido muestral.</p>
      <p>En el conjunto de datos, el 100% de los clientes suscritos tiene descuento aplicado y ninguna mujer figura como suscrita (variables confundidas).</p>
    </template>
  </SeccionRespuesta>
</template>
