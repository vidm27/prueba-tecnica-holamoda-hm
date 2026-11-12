<script setup lang="ts">
const { data, isPending, error } = useSuscripcion()
const si = computed(() => data.value?.find((d) => d.suscrito))
const no = computed(() => data.value?.find((d) => !d.suscrito))
const UMBRAL = 0.05 // diferencias menores al 5% se tratan como "igual"

const metricas = computed(() => si.value && no.value ? [
  { nombre: 'Gasto por compra', a: si.value.ticket_promedio, b: no.value.ticket_promedio, fmt: moneda },
  { nombre: 'Gasto anual estimado', a: si.value.gasto_anual_promedio, b: no.value.gasto_anual_promedio, fmt: moneda },
  { nombre: 'Compras previas', a: si.value.compras_previas_promedio, b: no.value.compras_previas_promedio, fmt: (n: number) => n.toFixed(1) },
  { nombre: 'Calificación', a: si.value.calificacion_promedio, b: no.value.calificacion_promedio, fmt: (n: number) => n.toFixed(2) },
].map((m) => ({ ...m, delta: m.a / m.b - 1 })) : [])
const sinEfecto = computed(() => metricas.value.every((m) => Math.abs(m.delta) < UMBRAL))
</script>

<template>
  <SeccionRespuesta :cargando="isPending" :error="error">
    <template #respuesta>
      <template v-if="sinEfecto">
        Hoy no: los suscritos gastan lo mismo que el resto ({{ moneda(si!.ticket_promedio) }} vs. {{ moneda(no!.ticket_promedio) }} por compra),
        y todos reciben descuento.
      </template>
      <template v-else>Los suscritos se comportan distinto al resto: revisa las diferencias abajo.</template>
    </template>
    <template #accion>
      La suscripción hoy regala descuento sin un gasto mayor a cambio. Antes de ampliarla, rediseñar el beneficio y medirlo con un piloto.
    </template>

    <div class="grid gap-4 sm:grid-cols-2">
      <UCard v-for="m in metricas" :key="m.nombre">
        <p class="text-sm text-muted">{{ m.nombre }}</p>
        <div class="mt-2 flex items-end justify-between gap-4">
          <div>
            <p class="text-xs text-muted">Suscritos</p>
            <p class="text-2xl font-semibold tabular-nums">{{ m.fmt(m.a) }}</p>
          </div>
          <div class="text-right">
            <p class="text-xs text-muted">No suscritos</p>
            <p class="text-2xl tabular-nums">{{ m.fmt(m.b) }}</p>
          </div>
        </div>
        <UBadge class="mt-3" variant="subtle" :color="Math.abs(m.delta) < UMBRAL ? 'neutral' : m.delta > 0 ? 'success' : 'error'"
                :label="Math.abs(m.delta) < UMBRAL ? `Prácticamente igual (${m.delta > 0 ? '+' : ''}${fraccion(m.delta, 1)})` : `${m.delta > 0 ? '+' : ''}${fraccion(m.delta, 1)}`" />
      </UCard>
    </div>

    <template #confianza>
      <p>Comparación entre {{ entero(si?.clientes ?? 0) }} suscritos y {{ entero(no?.clientes ?? 0) }} no suscritos; diferencias menores al 5% se consideran iguales.</p>
      <p>Ojo: todo suscrito tiene descuento y ninguna mujer está suscrita. La comparación mezcla suscripción, descuento y género: no prueba causa y efecto.</p>
    </template>
  </SeccionRespuesta>
</template>
