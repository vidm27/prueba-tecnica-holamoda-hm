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
const esContrasteProductos = slug === 'promocion' || slug === 'satisfaccion'
const componente = COMPONENTES[slug]
if (!componente) throw createError({ statusCode: 404, statusMessage: 'Página no encontrada', fatal: true })
</script>

<template>
  <div v-if="esContrasteProductos" class="mx-auto max-w-5xl space-y-12">
    <section class="space-y-4">
      <div class="flex items-center gap-2.5 border-b border-default pb-3">
        <UIcon name="i-lucide-megaphone" class="size-5 text-primary" />
        <div>
          <h2 class="text-base font-semibold">Oportunidades de promoción</h2>
          <p class="text-xs text-muted">Productos con buena calificación pero bajas ventas que necesitan mayor visibilidad</p>
        </div>
      </div>
      <PreguntaPromocion />
    </section>

    <section class="space-y-4">
      <div class="flex items-center gap-2.5 border-b border-default pb-3">
        <UIcon name="i-lucide-thumbs-down" class="size-5 text-error" />
        <div>
          <h2 class="text-base font-semibold">Productos que gustan menos</h2>
          <p class="text-xs text-muted">Contraste de satisfacción promedio y margen de error para distinguir problemas reales del azar</p>
        </div>
      </div>
      <PreguntaSatisfaccion />
    </section>
  </div>
  <component :is="componente" v-else />
</template>
