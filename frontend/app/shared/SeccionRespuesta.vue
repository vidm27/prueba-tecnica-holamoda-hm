<!--
  Contenedor visual de cada módulo analítico:
  1) visualizaciones e indicadores principales, 2) nota metodológica/estadística, 3) tabla de datos desplegable.
-->
<script setup lang="ts">
defineProps<{ cargando?: boolean; error?: Error | null }>()
</script>

<template>
  <UAlert v-if="error" color="error" variant="subtle" icon="i-lucide-circle-alert" title="No se pudieron cargar los datos" :description="mensajeAmigable(error instanceof ErrorApi ? error.estado : 0, error.message)" />
  <div v-else-if="cargando" class="mx-auto max-w-6xl space-y-6">
    <div class="grid gap-4 sm:grid-cols-3">
      <USkeleton v-for="n in 3" :key="n" class="h-24" />
    </div>
    <USkeleton class="h-80" />
  </div>
  <div v-else class="mx-auto max-w-6xl space-y-6">
    <slot />
    <UAlert v-if="$slots.confianza" color="neutral" variant="subtle" icon="i-lucide-chart-no-axes-combined" title="Contexto estadístico y metodológico">
      <template #description><div class="space-y-1 text-xs leading-relaxed"><slot name="confianza" /></div></template>
    </UAlert>
    <details v-if="$slots.detalle" class="group rounded-xl border border-default bg-default/40">
      <summary class="flex cursor-pointer list-none items-center justify-between px-4 py-3 text-sm font-medium select-none">
        <span class="flex items-center gap-2">
          <UIcon name="i-lucide-table" class="size-4 text-muted" />
          Ver tabla de datos
        </span>
        <UIcon name="i-lucide-chevron-down" class="size-4 text-muted transition-transform group-open:rotate-180" />
      </summary>
      <div class="overflow-x-auto border-t border-default px-4 py-3"><slot name="detalle" /></div>
    </details>
  </div>
</template>
