<script setup lang="ts">
const { data, isPending, error } = useValor()
const niveles = computed(() => data.value?.niveles ?? [])
const totalClientes = computed(() => niveles.value.reduce((s, n) => s + n.clientes, 0))
const pctClientes = (n: { clientes: number }) => Math.round((100 * n.clientes) / Math.max(1, totalClientes.value))
const top = computed(() => niveles.value.at(-1))
const series = computed(() => [
  { nombre: '% de los clientes', color: '#a1a1aa', datos: niveles.value.map(pctClientes) },
  { nombre: '% del gasto anual', color: '#dc2626', datos: niveles.value.map((n) => n.pct_gasto) },
])
</script>

<template>
  <SeccionRespuesta :cargando="isPending" :error="error">
    <template #respuesta>
      <template v-if="top">
        Los clientes {{ top.nivel }} ({{ pctClientes(top) }}% de la base) generan el {{ top.pct_gasto }}% del gasto anual:
        son los que gastan más de {{ moneda(top.gasto_minimo) }} al año.
      </template>
    </template>
    <template #accion>
      Retener a un cliente {{ top?.nivel }} vale tanto como retener a unos {{ top && niveles[0] ? Math.round(top.gasto_anual_total / top.clientes / (niveles[0].gasto_anual_total / niveles[0].clientes)) : '—' }} clientes Bronce.
      Enfoca fidelización y atención preferente en ellos.
    </template>

    <UCard>
      <p class="mb-2 text-sm text-muted">Cada nivel agrupa al 25% de los clientes, pero su aporte al gasto es muy distinto.</p>
      <GraficoBarras :etiquetas="niveles.map((n) => n.nivel)" :series="series" sufijo="%" :alto="300" />
    </UCard>

    <template #confianza>
      <p>Alta para describir la base actual: el gasto anual va de {{ moneda(niveles[0]?.gasto_minimo ?? 0) }} a {{ moneda(top?.gasto_maximo ?? 0) }} y la concentración es clara.</p>
      <p>
        El gasto anual es una estimación: monto de su compra × cuántas veces al año dice comprar. El 20% de clientes que más gasta aporta el
        {{ data?.pareto_top20_pct_gasto }}%.
      </p>
    </template>

    <template #detalle>
      <table class="w-full text-sm">
        <thead class="text-left text-muted">
          <tr><th class="py-2">Nivel</th><th class="text-right">Clientes</th><th class="text-right">Gasto anual por cliente</th><th class="text-right">Gasto anual total</th><th class="text-right">% del gasto</th></tr>
        </thead>
        <tbody>
          <tr v-for="n in niveles" :key="n.nivel" class="border-t border-default">
            <td class="py-2 font-medium">{{ n.nivel }}</td>
            <td class="text-right">{{ entero(n.clientes) }}</td>
            <td class="text-right">{{ moneda(n.gasto_minimo) }} – {{ moneda(n.gasto_maximo) }}</td>
            <td class="text-right">{{ moneda(n.gasto_anual_total) }}</td>
            <td class="text-right">{{ n.pct_gasto }}%</td>
          </tr>
        </tbody>
      </table>
    </template>
  </SeccionRespuesta>
</template>
