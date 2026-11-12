<script setup lang="ts">
const { data, isPending, error } = useTallas()
const ORDEN = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
const COLORES: Record<string, string> = {
  XS: '#06b6d4',
  S: '#10b981',
  M: '#e11d48',
  L: '#3b82f6',
  XL: '#f59e0b',
  XXL: '#8b5cf6',
}
const ICONOS_CAT: Record<string, string> = {
  Clothing: 'i-lucide-shirt',
  Footwear: 'i-lucide-footprints',
  Accessories: 'i-lucide-watch',
  Outerwear: 'i-lucide-cloud-snow',
}

const categoriaSeleccionada = ref<string>('Todas')
const modoGrafico = ref<'agrupado' | 'apilado' | 'unidades'>('agrupado')

const tallas = computed(() =>
  [...new Set((data.value ?? []).map((d) => d.talla))].sort((a, b) => ORDEN.indexOf(a) - ORDEN.indexOf(b)),
)
const categorias = computed(() => [...new Set((data.value ?? []).map((d) => d.categoria))])

const pct = (c: string, t: string) => data.value?.find((d) => d.categoria === c && d.talla === t)?.pct ?? 0
const comprasDe = (c: string, t: string) => data.value?.find((d) => d.categoria === c && d.talla === t)?.compras ?? 0

/** Curva según el filtro activo (toda la tienda o una categoría específica). */
const curva = computed(() => {
  const filas = (data.value ?? []).filter(
    (d) => categoriaSeleccionada.value === 'Todas' || d.categoria === categoriaSeleccionada.value,
  )
  const total = filas.reduce((s, d) => s + d.compras, 0)
  return tallas.value.map((t) => {
    const compras = filas.filter((d) => d.talla === t).reduce((s, d) => s + d.compras, 0)
    const porcentaje = Math.round((100 * compras) / Math.max(1, total))
    return {
      talla: t,
      compras,
      color: COLORES[t] ?? '#3b82f6',
      pct: porcentaje,
      porCada10: Math.max(1, Math.round(porcentaje / 10)),
    }
  })
})

const tallaLider = computed(() => [...curva.value].sort((a, b) => b.pct - a.pct)[0])
const dosLideres = computed(() => [...curva.value].sort((a, b) => b.pct - a.pct).slice(0, 2))
const sumaDosLideres = computed(() => dosLideres.value.reduce((s, x) => s + x.pct, 0))

/** Mayor diferencia entre categorías para una misma talla, en puntos porcentuales. */
const diferencia = computed(() =>
  Math.max(
    0,
    ...tallas.value.map((t) => {
      const v = categorias.value.map((c) => pct(c, t))
      return Math.max(...v) - Math.min(...v)
    }),
  ),
)

const series = computed(() =>
  tallas.value.map((t) => ({
    nombre: `Talla ${t}`,
    color: COLORES[t] ?? '#3b82f6',
    datos: categorias.value.map((c) => (modoGrafico.value === 'unidades' ? comprasDe(c, t) : pct(c, t))),
  })),
)
</script>

<template>
  <SeccionRespuesta :cargando="isPending" :error="error">
    <!-- Guía rápida en lenguaje sencillo: ¿Cómo pedir inventario sin complicarse? -->
    <UCard class="border-primary/30 bg-primary/5">
      <div class="flex flex-wrap items-center justify-between gap-4">
        <div class="flex items-start gap-3">
          <div class="mt-0.5 flex size-9 shrink-0 items-center justify-center rounded-lg bg-primary/15 text-primary">
            <UIcon name="i-lucide-package-check" class="size-5" />
          </div>
          <div>
            <div class="flex flex-wrap items-center gap-2">
              <h3 class="text-sm font-bold">Regla práctica de compra (por cada 10 prendas que pidas al proveedor)</h3>
              <UBadge color="primary" variant="soft" size="sm" label="La misma proporción sirve para todas las categorías" />
            </div>
            <p class="mt-1 text-xs text-muted">
              Las tallas <strong>{{ dosLideres.map((x) => x.talla).join(' y ') }}</strong> concentran el
              <strong>{{ sumaDosLideres }}%</strong> de todas las ventas. Sea ropa, calzado o abrigos, la proporción casi no cambia (varía menos de ±{{ diferencia.toFixed(1) }}%).
            </p>
          </div>
        </div>

        <!-- Selector rápido de categoría para recalcular las tarjetas -->
        <div class="flex flex-wrap items-center gap-1 rounded-lg border border-default bg-default/70 p-1">
          <UButton
            size="xs"
            color="neutral"
            :variant="categoriaSeleccionada === 'Todas' ? 'solid' : 'ghost'"
            label="Toda la tienda"
            @click="categoriaSeleccionada = 'Todas'"
          />
          <UButton
            v-for="cat in categorias"
            :key="cat"
            size="xs"
            color="neutral"
            :variant="categoriaSeleccionada === cat ? 'solid' : 'ghost'"
            :icon="ICONOS_CAT[cat]"
            :label="es(cat)"
            @click="categoriaSeleccionada = cat"
          />
        </div>
      </div>
    </UCard>

    <!-- Tarjetas de las 4 tallas con equivalencia humana ("X de cada 10") -->
    <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <UCard
        v-for="c in curva"
        :key="c.talla"
        :class="c.talla === tallaLider?.talla ? 'ring-2 ring-primary/40 bg-elevated/40' : ''"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="size-3 rounded-full" :style="{ background: c.color }" />
            <span class="text-sm font-bold uppercase">Talla {{ c.talla }}</span>
          </div>
          <UBadge
            v-if="c.talla === tallaLider?.talla"
            color="primary"
            variant="subtle"
            size="sm"
            label="#1 Más vendida"
          />
        </div>

        <div class="mt-3 flex items-baseline justify-between">
          <p class="text-3xl font-bold tabular-nums">{{ c.pct }}%</p>
          <span class="rounded-md bg-elevated px-2 py-0.5 text-xs font-medium">
            ~{{ c.porCada10 }} de cada 10 uds.
          </span>
        </div>

        <!-- Barra de proporción visual -->
        <div class="mt-3 h-2 w-full overflow-hidden rounded-full bg-elevated">
          <div class="h-full rounded-full transition-all" :style="{ width: `${c.pct}%`, background: c.color }" />
        </div>

        <p class="mt-2.5 text-xs text-muted">
          <strong>{{ entero(c.compras) }}</strong> unidades vendidas en
          {{ categoriaSeleccionada === 'Todas' ? 'total' : es(categoriaSeleccionada).toLowerCase() }}
        </p>
      </UCard>
    </div>

    <!-- Dona general vs Comparativa por categoría con selector de vista amigable -->
    <div class="grid gap-4 lg:grid-cols-[21rem_minmax(0,1fr)]">
      <UCard>
        <div class="mb-2">
          <p class="text-sm font-medium">
            Proporción en {{ categoriaSeleccionada === 'Todas' ? 'toda la tienda' : es(categoriaSeleccionada) }}
          </p>
          <p class="text-xs text-muted">De un vistazo: qué tajada se lleva cada talla</p>
        </div>
        <GraficoDona
          :etiquetas="curva.map((c) => `Talla ${c.talla}`)"
          :valores="curva.map((c) => c.pct)"
          :colores="curva.map((c) => c.color)"
          sufijo="%"
          :alto="265"
          :titulo-centro="`${tallaLider?.pct ?? 0}%`"
          :subtitulo-centro="tallaLider ? `Talla ${tallaLider.talla} (#1)` : ''"
        />
      </UCard>

      <UCard>
        <div class="mb-3 flex flex-wrap items-center justify-between gap-2">
          <div>
            <p class="text-sm font-medium">¿Cambia la talla según el tipo de prenda?</p>
            <p class="text-xs text-muted">
              Compara las 4 categorías lado a lado: verás la misma escalera (M domina, luego L, S y XL) en todas
            </p>
          </div>

          <div class="flex items-center gap-1 rounded-lg border border-default p-0.5">
            <UButton
              size="xs"
              color="neutral"
              :variant="modoGrafico === 'agrupado' ? 'soft' : 'ghost'"
              icon="i-lucide-bar-chart-3"
              label="Barras lado a lado (%)"
              @click="modoGrafico = 'agrupado'"
            />
            <UButton
              size="xs"
              color="neutral"
              :variant="modoGrafico === 'unidades' ? 'soft' : 'ghost'"
              icon="i-lucide-hash"
              label="En unidades"
              @click="modoGrafico = 'unidades'"
            />
            <UButton
              size="xs"
              color="neutral"
              :variant="modoGrafico === 'apilado' ? 'soft' : 'ghost'"
              icon="i-lucide-layers"
              label="100% apilado"
              @click="modoGrafico = 'apilado'"
            />
          </div>
        </div>

        <GraficoBarras
          :etiquetas="categorias.map(es)"
          :series="series"
          :horizontal="modoGrafico === 'apilado'"
          :apilado="modoGrafico === 'apilado'"
          :sufijo="modoGrafico === 'unidades' ? ' uds' : '%'"
          :maximo="modoGrafico === 'apilado' ? 100 : modoGrafico === 'agrupado' ? 50 : undefined"
          :alto="265"
        />
      </UCard>
    </div>

    <template #confianza>
      <p>Muestra total de {{ entero((data ?? []).reduce((s, d) => s + d.compras, 0)) }} compras; la variación máxima entre categorías para una misma talla es de apenas {{ diferencia.toFixed(1) }} puntos porcentuales.</p>
      <p>El dataset registra tallas S, M, L y XL (no incluye registros de XS ni XXL).</p>
    </template>

    <template #detalle>
      <table class="w-full text-sm">
        <thead class="text-left text-muted">
          <tr>
            <th class="py-2">Categoría</th>
            <th v-for="t in tallas" :key="t" class="text-right">Talla {{ t }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in categorias" :key="c" class="border-t border-default">
            <td class="py-2 font-medium">{{ es(c) }}</td>
            <td v-for="t in tallas" :key="t" class="text-right tabular-nums">
              <span class="font-semibold">{{ pct(c, t) }}%</span>
              <span class="ml-1 text-xs text-muted">({{ entero(comprasDe(c, t)) }})</span>
            </td>
          </tr>
        </tbody>
      </table>
    </template>
  </SeccionRespuesta>
</template>
