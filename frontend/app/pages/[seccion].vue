<!-- Cada ruta del menú muestra la respuesta de su funcionalidad (features/). -->
<script setup lang="ts">
import {
  LaboratorioHipotesis, PanelCalidad, PreguntaAbastecimiento, PreguntaAltoValor, PreguntaEnvios, PreguntaEstados,
  PreguntaPromocion, PreguntaSatisfaccion, PreguntaSuscripcion, PreguntaTallas,
} from '#components'

const COMPONENTES: Record<string, Component> = {
  promocion: PreguntaPromocion, satisfaccion: PreguntaSatisfaccion, tallas: PreguntaTallas,
  abastecimiento: PreguntaAbastecimiento, 'alto-valor': PreguntaAltoValor, suscripcion: PreguntaSuscripcion,
  envios: PreguntaEnvios, estados: PreguntaEstados, calidad: PanelCalidad, hipotesis: LaboratorioHipotesis,
}

const slug = String(useRoute().params.seccion)
const componente = COMPONENTES[slug]
if (!componente) throw createError({ statusCode: 404, statusMessage: 'Página no encontrada', fatal: true })
</script>

<template>
  <component :is="componente" />
</template>
