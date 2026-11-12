<script setup lang="ts">
const { data, isPending, error } = useAuditoria()
const SEVERIDAD: Record<string, { texto: string; color: 'error' | 'warning' | 'neutral'; icono: string }> = {
  alta: { texto: 'Severidad alta', color: 'error', icono: 'i-lucide-octagon-alert' },
  media: { texto: 'Severidad media', color: 'warning', icono: 'i-lucide-triangle-alert' },
  info: { texto: 'Informativo', color: 'neutral', icono: 'i-lucide-info' },
}
/** Qué significa cada hallazgo para el negocio; si llega una regla nueva, se muestra la descripción de la API. */
const IMPACTO: Record<string, { titulo: string; efecto: string }> = {
  beneficios_por_genero: { titulo: 'Ninguna mujer tiene suscripción ni descuento.', efecto: 'Sesgo estructural por género que impide evaluar elasticidad de descuentos en el segmento femenino.' },
  columnas_redundantes: { titulo: '"Descuento aplicado" y "usó código promocional" son 100% idénticas.', efecto: 'Colinealidad perfecta entre ambas columnas en los 3,900 registros.' },
  suscripcion_implica_descuento: { titulo: 'Todo cliente suscrito tiene descuento aplicado.', efecto: 'Confusión entre el efecto de membresía y el efecto promocional.' },
  pago_preferido_aleatorio: { titulo: 'El "método de pago preferido" no guarda relación con el método utilizado.', efecto: 'Coincidencia del 15.8% frente al 16.7% esperado por azar entre 6 medios de pago.' },
  frecuencia_sin_relacion_historial: { titulo: 'La frecuencia de compra declarada es independiente de las compras previas.', efecto: 'Correlación de Spearman cercana a cero (r = 0.005).' },
  frecuencias_sinonimas: { titulo: 'Etiquetas sinónimas en frecuencia ("Quarterly" vs "Every 3 Months", "Bi-Weekly" vs "Fortnightly").', efecto: 'Normalizadas durante el proceso ETL para el cálculo de gasto anual.' },
  distribuciones_uniformes: { titulo: 'Edades y montos distribuidos de manera uniforme.', efecto: 'Coeficiente de variación por tramo de 0.07, característico de generación sintética.' },
  sin_dimension_temporal: { titulo: 'Ausencia de fecha o marca temporal de transacción.', efecto: 'Impide análisis de series temporales, cohortes o retención.' },
}
const contar = (sev: string) => data.value?.filter((h) => h.severidad === sev).length ?? 0
</script>

<template>
  <SeccionRespuesta :cargando="isPending" :error="error">
    <div class="grid gap-4 sm:grid-cols-3">
      <UCard>
        <div class="flex items-center justify-between">
          <p class="text-xs font-medium tracking-wide text-muted uppercase">Severidad alta</p>
          <UIcon name="i-lucide-octagon-alert" class="size-4 text-error" />
        </div>
        <p class="mt-2 text-2xl font-bold text-error tabular-nums">{{ contar('alta') }}</p>
        <p class="text-xs text-muted">Sesgos estructurales o variables confundidas</p>
      </UCard>
      <UCard>
        <div class="flex items-center justify-between">
          <p class="text-xs font-medium tracking-wide text-muted uppercase">Severidad media</p>
          <UIcon name="i-lucide-triangle-alert" class="size-4 text-warning" />
        </div>
        <p class="mt-2 text-2xl font-bold text-warning tabular-nums">{{ contar('media') }}</p>
        <p class="text-xs text-muted">Independencia estadística o ruido sintético</p>
      </UCard>
      <UCard>
        <div class="flex items-center justify-between">
          <p class="text-xs font-medium tracking-wide text-muted uppercase">Reglas auditadas</p>
          <UIcon name="i-lucide-shield-check" class="size-4 text-primary" />
        </div>
        <p class="mt-2 text-2xl font-bold tabular-nums">{{ data?.length ?? 0 }}</p>
        <p class="text-xs text-muted">Ejecutadas automáticamente por el ETL</p>
      </UCard>
    </div>

    <div class="grid gap-3 sm:grid-cols-2">
      <UCard v-for="h in data" :key="h.regla">
        <div class="flex h-full flex-col justify-between gap-3">
          <div class="space-y-2">
            <div class="flex items-center justify-between gap-2">
              <UBadge :color="SEVERIDAD[h.severidad]?.color ?? 'neutral'" variant="subtle" size="sm" :label="SEVERIDAD[h.severidad]?.texto ?? h.severidad" />
              <span class="font-mono text-xs text-muted">{{ h.regla }}</span>
            </div>
            <p class="font-semibold">{{ IMPACTO[h.regla]?.titulo ?? h.descripcion }}</p>
            <p v-if="IMPACTO[h.regla]" class="text-xs leading-relaxed text-muted">{{ IMPACTO[h.regla]!.efecto }}</p>
          </div>

          <div class="space-y-1.5 border-t border-default pt-2.5">
            <div class="flex justify-between text-xs">
              <span class="text-muted">Registros alcanzados</span>
              <span class="font-medium tabular-nums">{{ entero(h.filas_afectadas) }} / {{ entero(h.total_filas) }} ({{ fraccion(h.filas_afectadas / h.total_filas) }})</span>
            </div>
            <div class="h-1.5 w-full overflow-hidden rounded-full bg-elevated">
              <div
                class="h-full rounded-full"
                :class="h.severidad === 'alta' ? 'bg-error' : h.severidad === 'media' ? 'bg-warning' : 'bg-primary'"
                :style="{ width: `${Math.min(100, Math.round((100 * h.filas_afectadas) / Math.max(1, h.total_filas)))}%` }"
              />
            </div>
          </div>
        </div>
      </UCard>
    </div>

    <template #confianza>
      <p>La validación del ETL opera en dos niveles: validación de esquema fila por fila (Pydantic, 100% válido) y auditoría estadística sobre el conjunto completo (`auditar.py`).</p>
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
