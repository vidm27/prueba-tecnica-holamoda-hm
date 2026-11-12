<script setup lang="ts">
const { data: resumen, isPending, error } = useResumen()

const kpis = computed(() => resumen.value && [
  { titulo: 'Ingreso total', valor: moneda(resumen.value.ingreso_total), detalle: 'Suma de todas las compras', icono: 'i-lucide-banknote' },
  { titulo: 'Compras', valor: entero(resumen.value.compras), detalle: `${entero(resumen.value.clientes)} clientes · ${resumen.value.productos} productos`, icono: 'i-lucide-shopping-cart' },
  { titulo: 'Ticket promedio', valor: moneda(resumen.value.ticket_promedio), detalle: 'Gasto por compra', icono: 'i-lucide-receipt' },
  { titulo: 'Calificación', valor: `${resumen.value.calificacion_promedio.toFixed(1)} / 5`, detalle: 'Promedio de satisfacción', icono: 'i-lucide-star' },
])
</script>

<template>
  <UAlert v-if="error" color="error" variant="subtle" :description="mensajeAmigable(error instanceof ErrorApi ? error.estado : 0, error.message)" />
  <div v-else class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
    <template v-if="isPending">
      <USkeleton v-for="n in 4" :key="n" class="h-24" />
    </template>
    <UCard v-for="k in kpis" v-else :key="k.titulo">
      <div class="flex items-center gap-3.5">
        <div class="flex size-11 shrink-0 items-center justify-center rounded-xl bg-primary/10 text-primary">
          <UIcon :name="k.icono" class="size-5" />
        </div>
        <div>
          <p class="text-xs font-medium tracking-wide text-muted uppercase">{{ k.titulo }}</p>
          <p class="mt-0.5 text-2xl font-bold tabular-nums">{{ k.valor }}</p>
          <p class="text-xs text-muted">{{ k.detalle }}</p>
        </div>
      </div>
    </UCard>
  </div>
</template>
