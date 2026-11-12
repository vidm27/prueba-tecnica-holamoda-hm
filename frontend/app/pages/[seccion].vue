<script setup lang="ts">
const seccion = buscarSeccion(String(useRoute().params.seccion))
if (!seccion) throw createError({ statusCode: 404, statusMessage: 'Página no encontrada', fatal: true })
</script>

<template>
  <SinContenido :icono="seccion!.icono" texto="Esta respuesta todavía está en construcción." />
</template>
