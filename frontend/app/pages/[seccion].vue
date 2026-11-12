<!-- Cada ruta del menú muestra la respuesta de su funcionalidad (features/). -->
<script setup lang="ts">
import {
  LaboratorioHipotesis, PanelCalidad, PreguntaAbastecimiento, PreguntaAltoValor, PreguntaEnvios, PreguntaEstados,
  PreguntaPromocion, PreguntaSatisfaccion, PreguntaSuscripcion, PreguntaTallas,
} from '#components'

const COMPONENTES: Record<string, Component> = {
  promocion: PreguntaPromocion, satisfaccion: PreguntaSatisfaccion, tallas: PreguntaTallas,
  abastecimiento: PreguntaAbastecimiento, clientes: PreguntaAltoValor, 'alto-valor': PreguntaAltoValor,
  suscripcion: PreguntaSuscripcion, envios: PreguntaEnvios, estados: PreguntaEstados,
  calidad: PanelCalidad, hipotesis: LaboratorioHipotesis,
}

const slug = String(useRoute().params.seccion)
const esContrasteProductos = slug === 'promocion' || slug === 'satisfaccion'
const esModuloClientes = ['clientes', 'alto-valor', 'suscripcion', 'envios'].includes(slug)
const seccionClienteActiva = ref<'todas' | 'valor' | 'suscripcion' | 'envios'>('todas')
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

  <div v-else-if="esModuloClientes" class="mx-auto max-w-6xl space-y-10">
    <!-- Barra de navegación rápida entre las subsecciones de Clientes -->
    <div class="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-default bg-elevated/40 p-3">
      <div class="flex items-center gap-2 text-xs text-muted">
        <UIcon name="i-lucide-sliders-horizontal" class="size-4 text-primary" />
        <span>Filtrar vista de clientes:</span>
      </div>
      <div class="flex flex-wrap gap-1.5">
        <UButton size="xs" color="neutral" :variant="seccionClienteActiva === 'todas' ? 'solid' : 'ghost'" icon="i-lucide-layout-grid" label="Vista completa (3 secciones)" @click="seccionClienteActiva = 'todas'" />
        <UButton size="xs" color="neutral" :variant="seccionClienteActiva === 'valor' ? 'solid' : 'ghost'" icon="i-lucide-gem" label="1. Niveles de valor" @click="seccionClienteActiva = 'valor'" />
        <UButton size="xs" color="neutral" :variant="seccionClienteActiva === 'suscripcion' ? 'solid' : 'ghost'" icon="i-lucide-repeat" label="2. Suscripciones" @click="seccionClienteActiva = 'suscripcion'" />
        <UButton size="xs" color="neutral" :variant="seccionClienteActiva === 'envios' ? 'solid' : 'ghost'" icon="i-lucide-truck" label="3. Preferencia de envío" @click="seccionClienteActiva = 'envios'" />
      </div>
    </div>

    <section v-if="seccionClienteActiva === 'todas' || seccionClienteActiva === 'valor'" class="space-y-4">
      <div class="flex items-center gap-3 border-b border-default pb-3">
        <div class="flex size-9 items-center justify-center rounded-lg bg-primary/10 text-primary">
          <UIcon name="i-lucide-gem" class="size-5" />
        </div>
        <div>
          <h2 class="text-base font-semibold">Segmentación por valor y concentración del gasto</h2>
          <p class="text-xs text-muted">Perfil de aporte económico, ticket anual promedio y equivalencia por cuartil (Bronce, Plata, Oro y Platino)</p>
        </div>
      </div>
      <PreguntaAltoValor />
    </section>

    <section v-if="seccionClienteActiva === 'todas' || seccionClienteActiva === 'suscripcion'" class="space-y-4">
      <div class="flex items-center gap-3 border-b border-default pb-3">
        <div class="flex size-9 items-center justify-center rounded-lg bg-primary/10 text-primary">
          <UIcon name="i-lucide-repeat" class="size-5" />
        </div>
        <div>
          <h2 class="text-base font-semibold">Desempeño del programa de suscripción</h2>
          <p class="text-xs text-muted">Distribución de la base y contraste de indicadores entre clientes suscritos y no suscritos</p>
        </div>
      </div>
      <PreguntaSuscripcion />
    </section>

    <section v-if="seccionClienteActiva === 'todas' || seccionClienteActiva === 'envios'" class="space-y-4">
      <div class="flex items-center gap-3 border-b border-default pb-3">
        <div class="flex size-9 items-center justify-center rounded-lg bg-primary/10 text-primary">
          <UIcon name="i-lucide-truck" class="size-5" />
        </div>
        <div>
          <h2 class="text-base font-semibold">Preferencias de envío por segmento</h2>
          <p class="text-xs text-muted">Distribución de modalidades de entrega según nivel de valor, grupo de edad y género</p>
        </div>
      </div>
      <PreguntaEnvios />
    </section>
  </div>

  <component :is="componente" v-else />
</template>
