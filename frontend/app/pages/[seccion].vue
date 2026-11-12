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
  <div v-if="esContrasteProductos" class="mx-auto max-w-6xl space-y-12">
    <section class="space-y-4">
      <div class="flex items-center gap-3 border-b border-default pb-3">
        <div class="flex size-9 items-center justify-center rounded-lg bg-primary/10 text-primary">
          <UIcon name="i-lucide-megaphone" class="size-5" />
        </div>
        <div>
          <h2 class="text-base font-semibold">Oportunidades de promoción y posicionamiento</h2>
          <p class="text-xs text-muted">Segmentación por cuadrantes de volumen de ventas frente a calificación de clientes</p>
        </div>
      </div>
      <PreguntaPromocion />
    </section>

    <section class="space-y-4">
      <div class="flex items-center gap-3 border-b border-default pb-3">
        <div class="flex size-9 items-center justify-center rounded-lg bg-error/10 text-error">
          <UIcon name="i-lucide-thumbs-down" class="size-5" />
        </div>
        <div>
          <h2 class="text-base font-semibold">Productos que menos gustan y brecha de satisfacción</h2>
          <p class="text-xs text-muted">Ranking de calificación promedio e intervalos de confianza (±95%) frente a la media del catálogo</p>
        </div>
      </div>
      <PreguntaSatisfaccion />
    </section>
  </div>
  <component :is="componente" v-else />
</template>
