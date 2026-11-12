<script setup lang="ts">
const { data, isPending, error } = useAuditoria()
const SEVERIDAD: Record<string, { texto: string; color: 'error' | 'warning' | 'neutral' }> = {
  alta: { texto: 'Importante', color: 'error' },
  media: { texto: 'A tener en cuenta', color: 'warning' },
  info: { texto: 'Informativo', color: 'neutral' },
}
/** Qué significa cada hallazgo para el negocio; si llega una regla nueva, se muestra la descripción de la API. */
const IMPACTO: Record<string, { titulo: string; efecto: string }> = {
  beneficios_por_genero: { titulo: 'Ninguna mujer tiene suscripción ni descuento.', efecto: 'No se puede comparar el efecto del descuento o la suscripción entre hombres y mujeres.' },
  columnas_redundantes: { titulo: '"Descuento aplicado" y "usó código promocional" son el mismo dato.', efecto: 'No se puede separar el efecto de un código del de un descuento.' },
  suscripcion_implica_descuento: { titulo: 'Todo cliente suscrito tiene descuento.', efecto: 'No se puede saber si un resultado se debe a la suscripción o al descuento.' },
  pago_preferido_aleatorio: { titulo: 'El "método de pago preferido" no coincide con el que el cliente usa.', efecto: 'Ese dato no sirve para decisiones de medios de pago.' },
  frecuencia_sin_relacion_historial: { titulo: 'La frecuencia de compra declarada no coincide con el historial.', efecto: 'El gasto anual estimado es una aproximación, no un dato medido.' },
  frecuencias_sinonimas: { titulo: 'Había frecuencias repetidas con otro nombre (p. ej. "trimestral" y "cada 3 meses").', efecto: 'Ya se unificaron; no afecta los resultados.' },
  distribuciones_uniformes: { titulo: 'Edades y montos están repartidos de forma demasiado pareja.', efecto: 'Indicio de datos simulados: por eso casi no hay diferencias entre grupos.' },
  sin_dimension_temporal: { titulo: 'No hay fecha de compra.', efecto: 'No se pueden ver tendencias en el tiempo, recompra ni el efecto de una promoción.' },
}
const importantes = computed(() => data.value?.filter((h) => h.severidad === 'alta').length ?? 0)
</script>

<template>
  <SeccionRespuesta :cargando="isPending" :error="error">
    <template #respuesta>
      Los datos sirven para describir a los clientes de hoy, no para predecir: hay {{ data?.length }} problemas detectados,
      {{ importantes }} de ellos importante{{ importantes === 1 ? '' : 's' }}.
    </template>
    <template #accion>
      Cada respuesta del tablero ya tiene en cuenta estos problemas en su sección "¿Qué tan seguro es esto?".
    </template>

    <ul class="space-y-3">
      <li v-for="h in data" :key="h.regla">
        <UCard>
          <div class="flex flex-wrap items-start gap-3">
            <UBadge :color="SEVERIDAD[h.severidad]?.color ?? 'neutral'" variant="subtle" :label="SEVERIDAD[h.severidad]?.texto ?? h.severidad" />
            <div class="min-w-0 flex-1 space-y-1">
              <p class="font-medium">{{ IMPACTO[h.regla]?.titulo ?? h.descripcion }}</p>
              <p v-if="IMPACTO[h.regla]" class="text-sm">{{ IMPACTO[h.regla]!.efecto }}</p>
              <p class="text-sm text-muted">Afecta {{ entero(h.filas_afectadas) }} de {{ entero(h.total_filas) }} registros ({{ fraccion(h.filas_afectadas / h.total_filas) }}).</p>
            </div>
          </div>
        </UCard>
      </li>
    </ul>

    <template #confianza>
      <p>Los datos pasan todas las validaciones registro por registro (tipos, rangos, duplicados). Estos problemas solo aparecen al mirar el conjunto completo.</p>
      <p>Faltan además fechas de compra: no hay tendencias en el tiempo, recompra ni efecto de promociones.</p>
    </template>

    <template #detalle>
      <div class="space-y-3">
        <div v-for="h in data" :key="h.regla" class="text-sm">
          <p class="font-mono text-xs text-muted">{{ h.regla }} · {{ h.descripcion }}</p>
          <pre class="mt-1 overflow-x-auto rounded bg-elevated p-2 text-xs">{{ JSON.stringify(h.evidencia, null, 2) }}</pre>
        </div>
      </div>
    </template>
  </SeccionRespuesta>
</template>
