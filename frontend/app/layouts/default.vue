<script setup lang="ts">
const { salir } = useAuth()
const ruta = useRoute()

const menu = [
  [{ label: 'Inicio', icon: 'i-lucide-house', to: '/' }],
  ...GRUPOS.filter((g) => !g.oculto).map((g) => [
    { label: g.titulo, type: 'label' as const },
    ...g.secciones.filter((s) => !s.oculto).map((s) => ({ label: s.menu, icon: s.icono, to: `/${s.slug}` })),
  ]),
]
const titulo = computed(() => buscarSeccion(String(ruta.params.seccion ?? ''))?.pregunta ?? 'Inicio')
</script>

<template>
  <UDashboardGroup>
    <UDashboardSidebar collapsible :ui="{ footer: 'border-t border-default' }">
      <template #header="{ collapsed }">
        <NuxtLink to="/" class="flex items-center gap-2.5 overflow-hidden">
          <img src="/logo.png" alt="H&M" class="h-7 w-auto shrink-0 object-contain" />
          <div v-if="!collapsed" class="leading-tight truncate">
            <p class="font-semibold">Hola Moda</p>
            <p class="text-xs text-muted">Tendencias de compra</p>
          </div>
        </NuxtLink>
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
