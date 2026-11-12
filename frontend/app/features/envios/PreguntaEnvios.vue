<script setup lang="ts">
import type { Segmento } from './useEnvios'

const segmento = ref<Segmento>('nivel_valor')
const subsegmentoActivo = ref<string>('Todos')
const { data, isPending, error } = useEnvios(segmento)

watch(segmento, () => {
  subsegmentoActivo.value = 'Todos'
})

const OPCIONES: { label: string; value: Segmento }[] = [
  { label: 'Nivel de valor', value: 'nivel_valor' },
  { label: 'Grupo de edad', value: 'grupo_edad' },
  { label: 'Género', value: 'genero' },
]

const COLORES_ENVIO = ['#e11d48', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4']
const ORDEN = ['Bronce', 'Plata', 'Oro', 'Platino', '<=24', '25-34', '35-44', '45-54', '55-64', '65+']

const segmentos = computed(() => [...new Set((data.value ?? []).map((d) => d.segmento))].sort((a, b) => ORDEN.indexOf(a) - ORDEN.indexOf(b)))
const tipos = computed(() => [...new Set((data.value ?? []).map((d) => d.tipo_envio))].sort())

const series = computed(() => tipos.value.map((t, i) => ({
  nombre: es(t),
  color: COLORES_ENVIO[i % COLORES_ENVIO.length],
  datos: segmentos.value.map((s) => data.value?.find((d) => d.segmento === s && d.tipo_envio === t)?.pct_segmento ?? 0),
})))

/** Distribución para el gráfico de dona según el sub-segmento filtrado (o promedio global). */
const distribucionDona = computed(() => {
  const filas = (data.value ?? []).filter((d) => subsegmentoActivo.value === 'Todos' || d.segmento === subsegmentoActivo.value)
  const totalCompras = filas.reduce((s, d) => s + d.compras, 0)
  return tipos.value.map((t, i) => {
    const compras = filas.filter((d) => d.tipo_envio === t).reduce((s, d) => s + d.compras, 0)
    return {
      tipo: es(t),
      color: COLORES_ENVIO[i % COLORES_ENVIO.length]!,
      compras,
      pct: +(100 * compras / Math.max(1, totalCompras)).toFixed(1),
    }
  })
})

const envioLider = computed(() => [...distribucionDona.value].sort((a, b) => b.pct - a.pct)[0])
const parejo = computed(() => 100 / Math.max(1, tipos.value.length))
const maximo = computed(() => Math.max(0, ...(data.value ?? []).map((d) => d.pct_segmento)))
</script>

<template>
  <SeccionRespuesta :cargando="isPending && !data" :error="error">
    <!-- 4 KPIs de la sección -->
    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <UCard>
        <div class="flex items-center justify-between">
          <p class="text-xs font-medium tracking-wide text-muted uppercase">Modalidades de envío</p>
          <UIcon name="i-lucide-truck" class="size-4 text-primary" />
        </div>
        <p class="mt-2 text-2xl font-bold tabular-nums">{{ tipos.length }}</p>
        <p class="text-xs text-muted">Opciones activas en tienda</p>
      </UCard>
      <UCard>
        <div class="flex items-center justify-between">
          <p class="text-xs font-medium tracking-wide text-muted uppercase">Reparto uniforme esperado</p>
          <UIcon name="i-lucide-scale" class="size-4 text-primary" />
        </div>
        <p class="mt-2 text-2xl font-bold tabular-nums">{{ parejo.toFixed(1) }}%</p>
        <p class="text-xs text-muted">Si la elección es equiprobable (1/{{ tipos.length }})</p>
      </UCard>
      <UCard>
        <div class="flex items-center justify-between">
          <p class="text-xs font-medium tracking-wide text-muted uppercase">Mayor concentración</p>
          <UIcon name="i-lucide-trending-up" class="size-4 text-primary" />
        </div>
        <div class="mt-2 flex items-baseline gap-2">
          <p class="text-2xl font-bold tabular-nums">{{ maximo.toFixed(1) }}%</p>
          <UBadge color="neutral" variant="subtle" size="sm" :label="`+${(maximo - parejo).toFixed(1)} pts`" />
        </div>
        <p class="text-xs text-muted">Máximo en cualquier segmento</p>
      </UCard>
      <UCard>
        <div class="flex items-center justify-between">
          <p class="text-xs font-medium tracking-wide text-muted uppercase">Envío #1 ({{ subsegmentoActivo === 'Todos' ? 'Global' : es(subsegmentoActivo) }})</p>
          <UIcon name="i-lucide-package-check" class="size-4 text-primary" />
        </div>
        <p class="mt-2 truncate text-xl font-bold text-primary">{{ envioLider?.tipo ?? '—' }}</p>
        <p class="text-xs text-muted">{{ envioLider ? `${envioLider.pct}% (${entero(envioLider.compras)} envíos)` : '' }}</p>
      </UCard>
    </div>

    <!-- Barra de filtros interactivos: Dimensión + Sub-segmento -->
    <UCard>
      <div class="mb-4 flex flex-wrap items-center justify-between gap-3 border-b border-default pb-3">
        <div class="flex flex-wrap items-center gap-2">
          <span class="text-xs font-medium text-muted uppercase">Agrupar por:</span>
          <div class="flex items-center gap-1 rounded-lg border border-default p-0.5">
            <UButton
              v-for="op in OPCIONES"
              :key="op.value"
              size="xs"
              color="neutral"
              :variant="segmento === op.value ? 'solid' : 'ghost'"
              :label="op.label"
              @click="segmento = op.value"
            />
          </div>
        </div>

        <div class="flex flex-wrap items-center gap-1.5">
          <span class="text-xs text-muted">Inspeccionar en dona:</span>
          <UButton
            size="xs"
            color="neutral"
            :variant="subsegmentoActivo === 'Todos' ? 'soft' : 'ghost'"
            label="Todos"
            @click="subsegmentoActivo = 'Todos'"
          />
          <UButton
            v-for="s in segmentos"
            :key="s"
            size="xs"
            color="neutral"
            :variant="subsegmentoActivo === s ? 'soft' : 'ghost'"
            :label="es(s)"
            @click="subsegmentoActivo = s"
          />
        </div>
      </div>

      <!-- Dona del segmento elegido + Barras apiladas de todos los segmentos -->
      <div class="grid gap-6 lg:grid-cols-[21rem_minmax(0,1fr)]">
        <div>
          <p class="mb-2 text-sm font-medium">
            Distribución en {{ subsegmentoActivo === 'Todos' ? 'toda la base' : es(subsegmentoActivo) }}
          </p>
          <p class="mb-2 text-xs text-muted">Cada tajada ronda ~{{ parejo.toFixed(1) }}%, evidenciando reparto uniforme</p>
          <GraficoDona
            :etiquetas="distribucionDona.map((d) => d.tipo)"
            :valores="distribucionDona.map((d) => d.pct)"
            :colores="distribucionDona.map((d) => d.color)"
            sufijo="%"
            :alto="260"
            :titulo-centro="`${envioLider?.pct ?? 0}%`"
            :subtitulo-centro="envioLider?.tipo"
          />
        </div>

        <div>
          <p class="mb-2 text-sm font-medium">Comparativa entre segmentos (cada barra suma 100%)</p>
          <p class="mb-2 text-xs text-muted">Contraste simultáneo de las {{ tipos.length }} modalidades a través de cada grupo</p>
          <GraficoBarras
            :etiquetas="segmentos.map(es)"
            :series="series"
            horizontal
            apilado
            sufijo="%"
            :maximo="100"
            :alto="Math.max(250, segmentos.length * 42 + 70)"
          />
        </div>
      </div>
    </UCard>

    <template #confianza>
      <p>Bajo una distribución uniforme entre {{ tipos.length }} modalidades, cada opción concentraría el {{ parejo.toFixed(1) }}% de los envíos; el máximo observado en cualquier segmento es {{ maximo.toFixed(1) }}%.</p>
    </template>

    <template #detalle>
      <table class="w-full text-sm">
        <thead class="text-left text-muted">
          <tr><th class="py-2">Segmento</th><th v-for="t in tipos" :key="t" class="text-right">{{ es(t) }}</th></tr>
        </thead>
        <tbody>
          <tr v-for="(s, i) in segmentos" :key="s" class="border-t border-default">
            <td class="py-2 font-medium">{{ es(s) }}</td>
            <td v-for="(serie, j) in series" :key="j" class="text-right tabular-nums">{{ serie.datos[i] }}%</td>
          </tr>
        </tbody>
      </table>
    </template>
  </SeccionRespuesta>
</template>
