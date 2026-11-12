<script setup lang="ts">
defineProps<{ icono: string; texto: string }>()
</script>

<template>
  <div class="flex h-full flex-col items-center justify-center gap-3 text-muted">
    <UIcon :name="icono" class="size-10" />
    <p>{{ texto }}</p>
  </div>
</template>
