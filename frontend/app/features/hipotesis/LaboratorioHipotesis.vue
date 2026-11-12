<script setup lang="ts">
const metrica = ref('monto_usd')
const variable = ref('temporada') // caso de ejemplo: parece significativo y no lo es
const { data, isPending, error } = useHipotesis(metrica, variable)

const METRICAS = [{ label: 'el gasto por compra', value: 'monto_usd' }, { label: 'la calificación', value: 'calificacion' }]
const VARIABLES = [
  { label: 'la temporada', value: 'temporada' }, { label: 'la categoría', value: 'categoria' }, { label: 'el producto', value: 'producto' },
  { label: 'la talla', value: 'talla' }, { label: 'el color', value: 'color' }, { label: 'el estado', value: 'estado' },
  { label: 'el género', value: 'genero' }, { label: 'el grupo de edad', value: 'grupo_edad' }, { label: 'el nivel de valor', value: 'nivel_valor' },
  { label: 'la suscripción', value: 'suscrito' }, { label: 'el descuento', value: 'descuento' }, { label: 'el tipo de envío', value: 'tipo_envio' },
  { label: 'el método de pago', value: 'metodo_pago' }, { label: 'la frecuencia de compra', value: 'frecuencia' },
]
const nombre = (lista: { label: string; value: string }[], v: string) => lista.find((x) => x.value === v)?.label ?? v

const pareceReal = computed(() => !!data.value && data.value.p_valor < 0.05)
const resultado = computed(() => {
  if (!data.value) return null
  if (data.value.significativo) return { texto: 'Sí, la diferencia es real.', color: 'success' as const, icono: 'i-lucide-check-circle' }
  if (pareceReal.value) return { texto: 'Parece real, pero es probablemente azar.', color: 'warning' as const, icono: 'i-lucide-triangle-alert' }
  return { texto: 'No hay diferencia: es azar.', color: 'neutral' as const, icono: 'i-lucide-equal' }
})
const ordenados = computed(() => [...(data.value?.grupos ?? [])].sort((a, b) => b.media - a.media))
const formato = (v: number) => (metrica.value === 'monto_usd' ? moneda(v) : v.toFixed(2))
</script>

<template>
  <SeccionRespuesta :error="error">
    <template #respuesta>
      <span class="text-base font-normal text-muted">¿Cambia</span>
      <USelect v-model="metrica" :items="METRICAS" class="mx-1 w-52 align-middle" />
      <span class="text-base font-normal text-muted">según</span>
      <USelect v-model="variable" :items="VARIABLES" class="mx-1 w-56 align-middle" />
      <span class="text-base font-normal text-muted">?</span>
      <span v-if="resultado" class="mt-3 flex items-center gap-2" :class="{ 'text-success': resultado.color === 'success', 'text-warning': resultado.color === 'warning' }">
        <UIcon :name="resultado.icono" class="size-6 shrink-0" /> {{ resultado.texto }}
      </span>
    </template>
    <template v-if="data && ordenados.length" #accion>
      El grupo más alto ({{ es(ordenados[0]!.grupo) }}: {{ formato(ordenados[0]!.media) }}) y el más bajo
      ({{ es(ordenados.at(-1)!.grupo) }}: {{ formato(ordenados.at(-1)!.media) }})
      {{ data.significativo ? 'son distintos de verdad.' : 'no son distintos de verdad: no tomes decisiones con esa diferencia.' }}
    </template>

    <USkeleton v-if="isPending" class="h-80" />
    <UCard v-else-if="data">
      <p class="mb-2 text-sm text-muted">Promedio de {{ nombre(METRICAS, metrica) }} por {{ nombre(VARIABLES, variable).replace(/^(el|la) /, '') }}. Las barras parten de cero para ver el tamaño real de la diferencia.</p>
      <GraficoBarras :etiquetas="ordenados.map((g) => es(g.grupo))" :series="[{ nombre: 'Promedio', datos: ordenados.map((g) => +g.media.toFixed(2)), color: '#dc2626' }]"
                     horizontal :alto="Math.max(180, ordenados.length * 22 + 40)" />
    </UCard>

    <template #confianza>
      <p>Se usa una prueba estadística (Kruskal-Wallis). Como en este tablero se pueden probar 28 combinaciones, 1 de cada 20 saldría "diferente" solo por suerte; por eso el resultado se corrige (Bonferroni).</p>
      <p v-if="data">Probabilidad de que sea azar: {{ (data.p_valor * 100).toFixed(1) }}% sin corregir, {{ (data.p_ajustado * 100).toFixed(1) }}% corregida. Cuenta como real si la corregida es menor a 5%.</p>
    </template>

    <template v-if="data" #detalle>
      <table class="w-full text-sm">
        <thead class="text-left text-muted"><tr><th class="py-2">Grupo</th><th class="text-right">Registros</th><th class="text-right">Promedio</th></tr></thead>
        <tbody>
          <tr v-for="g in ordenados" :key="g.grupo" class="border-t border-default">
            <td class="py-2">{{ es(g.grupo) }}</td><td class="text-right">{{ entero(g.n) }}</td><td class="text-right">{{ formato(g.media) }}</td>
          </tr>
        </tbody>
      </table>
    </template>
  </SeccionRespuesta>
</template>
