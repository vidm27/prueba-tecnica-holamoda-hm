<script setup lang="ts">
const { salir } = useAuth()
const ruta = useRoute()

const menu = [
  [{ label: 'Inicio', icon: 'i-lucide-house', to: '/' }],
  ...GRUPOS.map((g) => [
    { label: g.titulo, type: 'label' as const },
    ...g.secciones.map((s) => ({ label: s.menu, icon: s.icono, to: `/${s.slug}` })),
  ]),
]
const titulo = computed(() => buscarSeccion(String(ruta.params.seccion ?? ''))?.pregunta ?? 'Inicio')
</script>

<template>
  <UDashboardGroup>
    <UDashboardSidebar collapsible :ui="{ footer: 'border-t border-default' }">
      <template #header="{ collapsed }">
        <UIcon name="i-lucide-shopping-bag" class="size-6 shrink-0 text-primary" />
        <div v-if="!collapsed" class="leading-tight">
          <p class="font-semibold">Hola Moda</p>
          <p class="text-xs text-muted">Tendencias de compra</p>
        </div>
      </template>
      <template #default="{ collapsed }">
        <UNavigationMenu :items="menu" orientation="vertical" :collapsed="collapsed" tooltip />
      </template>
      <template #footer="{ collapsed }">
        <UButton icon="i-lucide-log-out" :label="collapsed ? undefined : 'Salir'" color="neutral" variant="ghost" block :square="collapsed" @click="salir" />
      </template>
    </UDashboardSidebar>
    <UDashboardPanel>
      <template #header>
        <UDashboardNavbar :title="titulo">
          <template #leading><UDashboardSidebarCollapse /></template>
        </UDashboardNavbar>
      </template>
      <template #body><slot /></template>
    </UDashboardPanel>
  </UDashboardGroup>
</template>
