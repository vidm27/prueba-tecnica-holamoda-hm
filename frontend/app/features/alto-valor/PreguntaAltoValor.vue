<script setup lang="ts">
import type { NivelValor } from './useValor'

const { data, isPending, error } = useValor()
const nivelSeleccionado = ref<string | null>(null)
const metricaBarras = ref<'porcentaje' | 'promedio' | 'total'>('porcentaje')

const COLORES_NIVEL: Record<string, string> = {
  Bronce: '#94a3b8',
  Plata: '#38bdf8',
  Oro: '#f59e0b',
  Platino: '#e11d48',
}

const DESCRIPCION_NIVEL: Record<string, string> = {
  Bronce: 'Compradores ocasionales de bajo volumen anual',
  Plata: 'Compradores regulares con ticket moderado',
  Oro: 'Clientes frecuentes con alto potencial de desarrollo',
  Platino: 'Núcleo VIP que sostiene la mayor parte del ingreso anual',
}

const niveles = computed(() => data.value?.niveles ?? [])
const totalClientes = computed(() => niveles.value.reduce((s, n) => s + n.clientes, 0))
const gastoTotalEmpresa = computed(() => niveles.value.reduce((s, n) => s + n.gasto_anual_total, 0))
const gastoPromedioEmpresa = computed(() => gastoTotalEmpresa.value / Math.max(1, totalClientes.value))

const pctClientes = (n: NivelValor) => Math.round((100 * n.clientes) / Math.max(1, totalClientes.value))
const gastoPromedio = (n: NivelValor) => n.gasto_anual_total / Math.max(1, n.clientes)

const baseBronce = computed(() => (niveles.value[0] ? gastoPromedio(niveles.value[0]) : 1))
const multiplicadorBronce = (n: NivelValor) => (gastoPromedio(n) / Math.max(1, baseBronce.value)).toFixed(1)

const top = computed(() => niveles.value.at(-1))
const detalleNivel = computed(() => niveles.value.find((n) => n.nivel === nivelSeleccionado.value) ?? top.value)

const seriesBarras = computed(() => {
  if (metricaBarras.value === 'promedio') {
    return [
      {
        nombre: 'Gasto anual promedio por cliente (USD)',
        datos: niveles.value.map((n) => Math.round(gastoPromedio(n))),
        color: niveles.value.map((n) => COLORES_NIVEL[n.nivel] ?? '#e11d48'),
      },
    ]
  }
  if (metricaBarras.value === 'total') {
    return [
      {
        nombre: 'Ingreso anual total del nivel (USD)',
        datos: niveles.value.map((n) => Math.round(n.gasto_anual_total)),
        color: niveles.value.map((n) => COLORES_NIVEL[n.nivel] ?? '#e11d48'),
      },
    ]
  }
  return [
    { nombre: '% de los clientes', color: '#94a3b8', datos: niveles.value.map(pctClientes) },
    { nombre: '% del gasto anual estimado', color: '#e11d48', datos: niveles.value.map((n) => n.pct_gasto) },
  ]
})
</script>

<template>
  <SeccionRespuesta :cargando="isPending" :error="error">
    <!-- Tarjetas enriquecidas por nivel de valor (clicables para inspeccionar) -->
    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <button
        v-for="n in niveles"
        :key="n.nivel"
        type="button"
        class="rounded-xl border p-4 text-left transition"
        :class="
          (nivelSeleccionado ?? top?.nivel) === n.nivel
            ? 'border-primary bg-elevated ring-2 ring-primary/40'
            : 'border-default bg-default/50 hover:bg-elevated/60'
        "
        @click="nivelSeleccionado = nivelSeleccionado === n.nivel ? null : n.nivel"
      >
        <div class="flex items-center justify-between gap-2">
          <div class="flex items-center gap-2">
            <span class="size-3 rounded-full" :style="{ background: COLORES_NIVEL[n.nivel] }" />
            <span class="text-sm font-bold uppercase">{{ n.nivel }}</span>
          </div>
          <UBadge :color="n.nivel === top?.nivel ? 'primary' : 'neutral'" variant="subtle" size="sm" :label="`${multiplicadorBronce(n)}× vs Bronce`" />
        </div>

        <div class="mt-3 flex items-baseline justify-between">
          <div>
            <p class="text-2xl font-bold tabular-nums">{{ n.pct_gasto }}%</p>
            <p class="text-xs text-muted">del ingreso anual</p>
          </div>
          <div class="text-right">
            <p class="text-base font-bold text-primary tabular-nums">{{ moneda(gastoPromedio(n)) }}</p>
            <p class="text-xs text-muted">prom. / cliente</p>
          </div>
        </div>

        <!-- Barra de peso en el gasto -->
        <div class="mt-3 h-1.5 w-full overflow-hidden rounded-full bg-elevated">
          <div class="h-full rounded-full" :style="{ width: `${n.pct_gasto}%`, background: COLORES_NIVEL[n.nivel] }" />
        </div>

        <dl class="mt-3 space-y-1 border-t border-default pt-2.5 text-xs">
          <div class="flex justify-between">
            <dt class="text-muted">Clientes ({{ pctClientes(n) }}%)</dt>
            <dd class="font-medium tabular-nums">{{ entero(n.clientes) }}</dd>
          </div>
          <div class="flex justify-between">
            <dt class="text-muted">Ingreso del nivel</dt>
            <dd class="font-medium tabular-nums">{{ moneda(n.gasto_anual_total) }}</dd>
          </div>
          <div class="flex justify-between">
            <dt class="text-muted">Rango anual</dt>
            <dd class="font-medium tabular-nums">{{ moneda(n.gasto_minimo) }} – {{ moneda(n.gasto_maximo) }}</dd>
          </div>
        </dl>
      </button>
    </div>

    <!-- Radiografía detallada del nivel activo -->
    <UCard v-if="detalleNivel" class="border-primary/30 bg-elevated/30">
      <div class="flex flex-wrap items-center justify-between gap-4">
        <div class="flex items-center gap-3">
          <span class="size-4 rounded-full" :style="{ background: COLORES_NIVEL[detalleNivel.nivel] }" />
          <div>
            <div class="flex items-center gap-2">
              <p class="text-base font-bold">Radiografía del nivel {{ detalleNivel.nivel }}</p>
              <UBadge color="primary" variant="soft" size="sm" :label="`Top 20% general genera el ${data?.pareto_top20_pct_gasto}% del gasto`" />
            </div>
            <p class="text-xs text-muted">{{ DESCRIPCION_NIVEL[detalleNivel.nivel] }}</p>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4 sm:grid-cols-4">
          <div>
            <p class="text-xs text-muted">Gasto anual / cliente</p>
            <p class="text-sm font-bold tabular-nums">{{ moneda(gastoPromedio(detalleNivel)) }}</p>
          </div>
          <div>
            <p class="text-xs text-muted">vs. Promedio empresa ({{ moneda(gastoPromedioEmpresa) }})</p>
            <p class="text-sm font-bold tabular-nums" :class="gastoPromedio(detalleNivel) >= gastoPromedioEmpresa ? 'text-success' : 'text-warning'">
              {{ gastoPromedio(detalleNivel) >= gastoPromedioEmpresa ? '+' : '' }}{{ Math.round((100 * (gastoPromedio(detalleNivel) - gastoPromedioEmpresa)) / Math.max(1, gastoPromedioEmpresa)) }}%
            </p>
          </div>
          <div>
            <p class="text-xs text-muted">Equivalencia vs. Bronce</p>
            <p class="text-sm font-bold tabular-nums">1 {{ detalleNivel.nivel }} = {{ multiplicadorBronce(detalleNivel) }} Bronce</p>
          </div>
          <div>
            <p class="text-xs text-muted">Volumen anual del cuartil</p>
            <p class="text-sm font-bold tabular-nums">{{ moneda(detalleNivel.gasto_anual_total) }}</p>
          </div>
        </div>
      </div>
    </UCard>

    <!-- Gráficos combinados: Dona de concentración + Barras con filtro de métrica -->
    <div class="grid gap-4 lg:grid-cols-[22rem_minmax(0,1fr)]">
      <UCard>
        <div class="mb-2">
          <p class="text-sm font-medium">Distribución del gasto anual</p>
          <p class="text-xs text-muted">Peso de cada nivel sobre el 100% del ingreso estimado</p>
        </div>
        <GraficoDona
          :etiquetas="niveles.map((n) => n.nivel)"
          :valores="niveles.map((n) => n.pct_gasto)"
          :colores="niveles.map((n) => COLORES_NIVEL[n.nivel] ?? '#e11d48')"
          sufijo="%"
          :alto="270"
          :titulo-centro="`${detalleNivel?.pct_gasto ?? 0}%`"
          :subtitulo-centro="`Nivel ${detalleNivel?.nivel ?? ''}`"
        />
      </UCard>

      <UCard>
        <div class="mb-3 flex flex-wrap items-center justify-between gap-2">
          <div>
            <p class="text-sm font-medium">Comparativa entre cuartiles de clientes</p>
            <p class="text-xs text-muted">Cambia la métrica para contrastar proporción, ticket anual promedio o ingreso total</p>
          </div>
          <div class="flex items-center gap-1 rounded-lg border border-default p-0.5">
            <UButton size="xs" color="neutral" :variant="metricaBarras === 'porcentaje' ? 'soft' : 'ghost'" label="% Clientes vs. % Gasto" @click="metricaBarras = 'porcentaje'" />
            <UButton size="xs" color="neutral" :variant="metricaBarras === 'promedio' ? 'soft' : 'ghost'" label="Gasto / cliente ($)" @click="metricaBarras = 'promedio'" />
            <UButton size="xs" color="neutral" :variant="metricaBarras === 'total' ? 'soft' : 'ghost'" label="Ingreso total ($)" @click="metricaBarras = 'total'" />
          </div>
        </div>
        <GraficoBarras
          :etiquetas="niveles.map((n) => n.nivel)"
          :series="seriesBarras"
          :sufijo="metricaBarras === 'porcentaje' ? '%' : ' USD'"
          :alto="270"
        />
      </UCard>
    </div>

    <template #confianza>
      <p>El gasto anual estimado se calcula como `monto_compra × compras_anuales_según_frecuencia`, abarcando desde {{ moneda(niveles[0]?.gasto_minimo ?? 0) }} hasta {{ moneda(top?.gasto_maximo ?? 0) }}.</p>
      <p>La segmentación en cuartiles (25% de clientes por nivel) muestra que el 20% superior de clientes concentra el {{ data?.pareto_top20_pct_gasto }}% del ingreso anual.</p>
    </template>

    <template #detalle>
      <table class="w-full text-sm">
        <thead class="text-left text-muted">
          <tr>
            <th class="py-2">Nivel</th>
            <th class="text-right">Clientes</th>
            <th class="text-right">Gasto prom. / cliente</th>
            <th class="text-right">Equivalencia vs. Bronce</th>
            <th class="text-right">Rango anual</th>
            <th class="text-right">Gasto anual total</th>
            <th class="text-right">% del gasto</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="n in niveles" :key="n.nivel" class="border-t border-default">
            <td class="py-2 font-medium">{{ n.nivel }}</td>
            <td class="text-right tabular-nums">{{ entero(n.clientes) }}</td>
            <td class="text-right font-medium tabular-nums">{{ moneda(gastoPromedio(n)) }}</td>
            <td class="text-right tabular-nums">{{ multiplicadorBronce(n) }}×</td>
            <td class="text-right tabular-nums">{{ moneda(n.gasto_minimo) }} – {{ moneda(n.gasto_maximo) }}</td>
            <td class="text-right tabular-nums">{{ moneda(n.gasto_anual_total) }}</td>
            <td class="text-right font-semibold tabular-nums">{{ n.pct_gasto }}%</td>
          </tr>
        </tbody>
      </table>
    </template>
  </SeccionRespuesta>
</template>
