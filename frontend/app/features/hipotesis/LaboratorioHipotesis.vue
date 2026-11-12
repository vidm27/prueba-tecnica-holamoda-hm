<script setup lang="ts">
const metrica = ref('monto_usd')
const variable = ref('temporada') // caso de ejemplo: p crudo < 0.05 pero no supera corrección de Bonferroni
const { data, isPending, error } = useHipotesis(metrica, variable)

const METRICAS = [
  { label: 'Gasto por compra (USD)', value: 'monto_usd' },
  { label: 'Calificación del producto (1–5 ★)', value: 'calificacion' },
]
const VARIABLES = [
  { label: 'Temporada', value: 'temporada' }, { label: 'Categoría', value: 'categoria' }, { label: 'Producto', value: 'producto' },
  { label: 'Talla', value: 'talla' }, { label: 'Color', value: 'color' }, { label: 'Estado', value: 'estado' },
  { label: 'Género', value: 'genero' }, { label: 'Grupo de edad', value: 'grupo_edad' }, { label: 'Nivel de valor', value: 'nivel_valor' },
  { label: 'Suscripción', value: 'suscrito' }, { label: 'Descuento', value: 'descuento' }, { label: 'Tipo de envío', value: 'tipo_envio' },
  { label: 'Método de pago', value: 'metodo_pago' }, { label: 'Frecuencia de compra', value: 'frecuencia' },
]
const nombre = (lista: { label: string; value: string }[], v: string) => lista.find((x) => x.value === v)?.label ?? v

const pareceReal = computed(() => !!data.value && data.value.p_valor < 0.05)
const resultado = computed(() => {
  if (!data.value) return null
  if (data.value.significativo) return { texto: 'Diferencia estadísticamente significativa', color: 'success' as const, icono: 'i-lucide-check-circle' }
  if (pareceReal.value) return { texto: 'Falso positivo sin corrección (ruido tras Bonferroni)', color: 'warning' as const, icono: 'i-lucide-triangle-alert' }
  return { texto: 'Sin diferencia significativa (variación por azar)', color: 'neutral' as const, icono: 'i-lucide-equal' }
})
const ordenados = computed(() => [...(data.value?.grupos ?? [])].sort((a, b) => b.media - a.media))
const formato = (v: number) => (metrica.value === 'monto_usd' ? moneda(v) : v.toFixed(2))
</script>

<template>
  <SeccionRespuesta :error="error">
    <!-- Barra de control interactiva -->
    <UCard>
      <div class="flex flex-wrap items-end justify-between gap-4">
        <div class="flex flex-wrap items-center gap-4">
          <div class="space-y-1">
            <label class="block text-xs font-medium tracking-wide text-muted uppercase">Métrica objetivo</label>
            <USelect v-model="metrica" :items="METRICAS" class="w-64" />
          </div>
          <div class="space-y-1">
            <label class="block text-xs font-medium tracking-wide text-muted uppercase">Variable de agrupación</label>
            <USelect v-model="variable" :items="VARIABLES" class="w-60" />
          </div>
        </div>
        <UBadge v-if="resultado" :color="resultado.color" variant="subtle" size="lg" class="gap-1.5 py-1.5">
          <UIcon :name="resultado.icono" class="size-4" />
          {{ resultado.texto }}
        </UBadge>
      </div>
    </UCard>

    <!-- Indicadores estadísticos de la prueba -->
    <div v-if="data" class="grid gap-4 sm:grid-cols-4">
      <UCard>
        <p class="text-xs font-medium tracking-wide text-muted uppercase">Estadístico ({{ data.prueba }})</p>
        <p class="mt-2 text-2xl font-bold tabular-nums">{{ data.estadistico.toFixed(3) }}</p>
        <p class="text-xs text-muted">{{ data.grupos.length }} grupos comparados</p>
      </UCard>
      <UCard>
        <p class="text-xs font-medium tracking-wide text-muted uppercase">p-valor sin corregir</p>
        <p class="mt-2 text-2xl font-bold tabular-nums" :class="data.p_valor < 0.05 ? 'text-warning' : ''">{{ data.p_valor.toFixed(4) }}</p>
        <p class="text-xs text-muted">{{ (data.p_valor * 100).toFixed(2) }}% prob. de azar individual</p>
      </UCard>
      <UCard>
        <p class="text-xs font-medium tracking-wide text-muted uppercase">p-valor Bonferroni (×28)</p>
        <p class="mt-2 text-2xl font-bold tabular-nums" :class="data.significativo ? 'text-success' : ''">{{ data.p_ajustado.toFixed(4) }}</p>
        <p class="text-xs text-muted">Ajustado por comparaciones múltiples</p>
      </UCard>
      <UCard>
        <p class="text-xs font-medium tracking-wide text-muted uppercase">Rango entre grupos</p>
        <p class="mt-2 text-2xl font-bold tabular-nums">
          {{ ordenados.length ? `${formato(ordenados.at(-1)!.media)} – ${formato(ordenados[0]!.media)}` : '—' }}
        </p>
        <p class="text-xs text-muted">Mínimo vs. máximo grupal</p>
      </UCard>
    </div>

    <USkeleton v-if="isPending" class="h-80" />
    <UCard v-else-if="data">
      <div class="mb-3">
        <p class="text-sm font-medium">Promedio de {{ nombre(METRICAS, metrica) }} por {{ nombre(VARIABLES, variable) }}</p>
        <p class="text-xs text-muted">Grupos ordenados de mayor a menor media muestral</p>
      </div>
      <GraficoBarras
        :etiquetas="ordenados.map((g) => es(g.grupo))"
        :series="[{ nombre: nombre(METRICAS, metrica), datos: ordenados.map((g) => +g.media.toFixed(2)), color: '#3b82f6' }]"
        horizontal
        :alto="Math.max(200, ordenados.length * 24 + 50)"
      />
    </UCard>

    <template #confianza>
      <p>Se ejecuta la prueba no paramétrica de Kruskal-Wallis y se aplica corrección de Bonferroni sobre las 28 combinaciones posibles (2 métricas × 14 variables) con umbral α = 0.05.</p>
    </template>

    <template v-if="data" #detalle>
      <table class="w-full text-sm">
        <thead class="text-left text-muted"><tr><th class="py-2">Grupo</th><th class="text-right">Registros (n)</th><th class="text-right">Promedio</th></tr></thead>
        <tbody>
          <tr v-for="g in ordenados" :key="g.grupo" class="border-t border-default">
            <td class="py-2 font-medium">{{ es(g.grupo) }}</td>
            <td class="text-right tabular-nums">{{ entero(g.n) }}</td>
            <td class="text-right tabular-nums">{{ formato(g.media) }}</td>
          </tr>
        </tbody>
      </table>
    </template>
  </SeccionRespuesta>
</template>
