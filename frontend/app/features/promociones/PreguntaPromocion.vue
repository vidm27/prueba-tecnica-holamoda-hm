<script setup lang="ts">
import { RECOMENDACIONES } from './usePromociones'

const { data, isPending, error } = usePromociones()
const candidatos = computed(() => data.value?.productos.filter((p) => p.recomendacion === 'promocion_exposicion') ?? [])
const nombres = computed(() => candidatos.value.slice(0, 3).map((p) => es(p.producto)))
</script>

<template>
  <SeccionRespuesta :cargando="isPending" :error="error">
    <template #respuesta>
      Promociona {{ nombres.join(', ') }}<span v-if="candidatos.length > 3"> y {{ candidatos.length - 3 }} más</span>:
      gustan a los clientes, pero se venden menos que la mayoría.
    </template>
    <template #accion>
      El problema de estos productos es la <strong>visibilidad</strong>, no el precio: priorízalos en vitrina, campañas y recomendaciones.
    </template>

    <UCard>
      <p class="mb-2 text-sm text-muted">Cada punto es un producto. Arriba a la izquierda están los que gustan pero se venden poco.</p>
      <MapaPromocion v-if="data" :datos="data" />
    </UCard>

    <template #confianza>
      <p>Las calificaciones entre productos difieren en décimas (±0.1): úsalo para <strong>priorizar</strong>, no como veredicto.</p>
      <p>{{ data?.advertencia }}</p>
      <p>Hoy ninguna mujer recibe descuento ({{ data?.compras_mujeres_con_descuento }} compras), así que no hay base para promociones por género.</p>
    </template>

    <template #detalle>
      <table class="w-full text-sm">
        <thead class="text-left text-muted">
          <tr><th class="py-2">Producto</th><th>Categoría</th><th class="text-right">Vendidos</th><th class="text-right">Calificación</th><th class="pl-4">Recomendación</th></tr>
        </thead>
        <tbody>
          <tr v-for="p in data?.productos" :key="p.producto" class="border-t border-default">
            <td class="py-2 font-medium">{{ es(p.producto) }}</td>
            <td>{{ es(p.categoria) }}</td>
            <td class="text-right">{{ p.ventas }}</td>
            <td class="text-right">{{ p.calificacion.toFixed(2) }}</td>
            <td class="pl-4">
              <span class="mr-2 inline-block size-2.5 rounded-full" :style="{ background: RECOMENDACIONES[p.recomendacion].color }" />
              {{ RECOMENDACIONES[p.recomendacion].accion }}
            </td>
          </tr>
        </tbody>
      </table>
    </template>
  </SeccionRespuesta>
</template>
