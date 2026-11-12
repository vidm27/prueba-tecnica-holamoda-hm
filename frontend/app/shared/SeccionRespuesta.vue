<!--
  Forma común de cada pregunta, pensada para gerentes no técnicos:
  1) la respuesta en una frase, 2) el gráfico que la muestra, 3) qué tan segura es, 4) el detalle plegado.
-->
<script setup lang="ts">
defineProps<{ cargando?: boolean; error?: Error | null }>()
</script>

<template>
  <UAlert v-if="error" color="error" variant="subtle" icon="i-lucide-circle-alert" title="No se pudo cargar la respuesta" :description="error.message" />
  <div v-else-if="cargando" class="mx-auto max-w-5xl space-y-6">
    <USkeleton class="h-24" />
    <USkeleton class="h-80" />
  </div>
  <div v-else class="mx-auto max-w-5xl space-y-6">
    <div class="rounded-xl border-l-4 border-primary bg-elevated p-5">
      <p class="text-xs font-medium tracking-wide text-muted uppercase">Respuesta</p>
      <p class="mt-1 text-xl leading-snug font-semibold"><slot name="respuesta" /></p>
      <p v-if="$slots.accion" class="mt-2 text-sm"><slot name="accion" /></p>
    </div>
    <slot />
    <UAlert v-if="$slots.confianza" color="neutral" variant="subtle" icon="i-lucide-info" title="¿Qué tan seguro es esto?">
      <template #description><div class="space-y-1"><slot name="confianza" /></div></template>
    </UAlert>
    <details v-if="$slots.detalle" class="rounded-lg border border-default">
      <summary class="cursor-pointer px-4 py-3 text-sm font-medium">Ver el detalle</summary>
      <div class="overflow-x-auto px-4 pb-4"><slot name="detalle" /></div>
    </details>
  </div>
</template>
