<script setup lang="ts">
definePageMeta({ layout: false }) // sin menú lateral
</script>

<template>
  <div class="flex min-h-screen items-center justify-center bg-neutral-50 p-4 dark:bg-neutral-950">
    <div class="w-full max-w-sm space-y-4">
      <div class="flex flex-col items-center gap-2 text-center">
        <img src="/logo.png" alt="H&M Logo" class="h-12 w-auto object-contain" />
        <div>
          <h1 class="text-xl font-bold tracking-tight">Hola Moda</h1>
          <p class="text-xs text-muted">Portal de Analítica y Tendencias</p>
        </div>
      </div>
      <FormularioLogin />
    </div>
  </div>
</template>
