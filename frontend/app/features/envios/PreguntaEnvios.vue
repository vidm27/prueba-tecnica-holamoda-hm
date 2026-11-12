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
/** Un líder cuenta si supera el reparto parejo por al menos 5 puntos. */
const hayPreferencia = computed(() => maximo.value - parejo.value >= 5)
</script>

<template>
  <SeccionRespuesta :cargando="isPending && !data" :error="error">
    <template #respuesta>
      <template v-if="!hayPreferencia">
        Ningún segmento tiene un envío preferido: cada uno de los {{ tipos.length }} tipos se usa en ~{{ Math.round(parejo) }}% de las compras.
      </template>
      <template v-else>Hay segmentos con un envío claramente preferido: revisa el gráfico.</template>
    </template>
    <template #accion>
      No conviene diseñar ofertas de envío por segmento con estos datos. Si se quiere reducir costo, se puede probar quitar opciones caras sin esperar rechazo de un grupo específico.
    </template>

    <UCard>
      <div class="mb-3 flex flex-wrap items-center justify-between gap-3">
        <p class="text-sm text-muted">Reparto de los tipos de envío dentro de cada segmento (cada barra suma 100%).</p>
        <USelect v-model="segmento" :items="OPCIONES" class="w-48" />
      </div>
      <GraficoBarras :etiquetas="segmentos.map(es)" :series="series" horizontal apilado sufijo="%" :maximo="100"
                     :alto="Math.max(220, segmentos.length * 48 + 80)" />
    </UCard>

    <template #confianza>
      <p>Si los clientes eligieran al azar, cada tipo tendría {{ Math.round(parejo) }}%. El tipo más usado en cualquier segmento llega a {{ maximo.toFixed(1) }}%: una diferencia que entra en el azar.</p>
    </template>

    <template #detalle>
      <table class="w-full text-sm">
        <thead class="text-left text-muted">
          <tr><th class="py-2">Segmento</th><th v-for="t in tipos" :key="t" class="text-right">{{ es(t) }}</th></tr>
        </thead>
        <tbody>
          <tr v-for="(s, i) in segmentos" :key="s" class="border-t border-default">
            <td class="py-2 font-medium">{{ es(s) }}</td>
            <td v-for="(serie, j) in series" :key="j" class="text-right">{{ serie.datos[i] }}%</td>
          </tr>
        </tbody>
      </table>
    </template>
  </SeccionRespuesta>
</template>
