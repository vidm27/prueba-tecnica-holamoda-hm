<script setup lang="ts">
import type { Segmento } from './useEnvios'

const segmento = ref<Segmento>('nivel_valor')
const { data, isPending, error } = useEnvios(segmento)
const OPCIONES: { label: string; value: Segmento }[] = [
  { label: 'Nivel de valor', value: 'nivel_valor' },
  { label: 'Grupo de edad', value: 'grupo_edad' },
  { label: 'Género', value: 'genero' },
]

const ORDEN = ['Bronce', 'Plata', 'Oro', 'Platino', '<=24', '25-34', '35-44', '45-54', '55-64', '65+']
const segmentos = computed(() => [...new Set((data.value ?? []).map((d) => d.segmento))].sort((a, b) => ORDEN.indexOf(a) - ORDEN.indexOf(b)))
const tipos = computed(() => [...new Set((data.value ?? []).map((d) => d.tipo_envio))].sort())
const series = computed(() => tipos.value.map((t) => ({
  nombre: es(t),
  datos: segmentos.value.map((s) => data.value?.find((d) => d.segmento === s && d.tipo_envio === t)?.pct_segmento ?? 0),
})))
const parejo = computed(() => 100 / Math.max(1, tipos.value.length))
const maximo = computed(() => Math.max(0, ...(data.value ?? []).map((d) => d.pct_segmento)))
</script>

<template>
  <SeccionRespuesta :cargando="isPending && !data" :error="error">
    <div class="grid gap-4 sm:grid-cols-3">
      <UCard>
        <p class="text-xs font-medium tracking-wide text-muted uppercase">Modalidades de envío</p>
        <p class="mt-2 text-2xl font-bold tabular-nums">{{ tipos.length }}</p>
        <p class="text-xs text-muted">Opciones activas en tienda</p>
      </UCard>
      <UCard>
        <p class="text-xs font-medium tracking-wide text-muted uppercase">Reparto uniforme esperado</p>
        <p class="mt-2 text-2xl font-bold tabular-nums">{{ parejo.toFixed(1) }}%</p>
        <p class="text-xs text-muted">Si la elección es equiprobable (1/{{ tipos.length }})</p>
      </UCard>
      <UCard>
        <p class="text-xs font-medium tracking-wide text-muted uppercase">Participación máxima</p>
        <div class="mt-2 flex items-baseline gap-2">
          <p class="text-2xl font-bold tabular-nums">{{ maximo.toFixed(1) }}%</p>
          <UBadge color="neutral" variant="subtle" size="sm" :label="`+${(maximo - parejo).toFixed(1)} pts vs. uniforme`" />
        </div>
        <p class="text-xs text-muted">Mayor concentración en un segmento</p>
      </UCard>
    </div>

    <UCard>
      <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div>
          <p class="text-sm font-medium">Distribución de tipos de envío por segmento</p>
          <p class="text-xs text-muted">Proporción de cada modalidad dentro del segmento seleccionado (suma 100%)</p>
        </div>
        <div class="flex items-center gap-1.5 rounded-lg border border-default p-1">
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
      <GraficoBarras :etiquetas="segmentos.map(es)" :series="series" horizontal apilado sufijo="%" :maximo="100"
                     :alto="Math.max(240, segmentos.length * 48 + 80)" />
    </UCard>

    <template #confianza>
      <p>Bajo una distribución uniforme entre {{ tipos.length }} modalidades, cada opción concentraría el {{ parejo.toFixed(1) }}% de los envíos; el máximo observado es {{ maximo.toFixed(1) }}%.</p>
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
