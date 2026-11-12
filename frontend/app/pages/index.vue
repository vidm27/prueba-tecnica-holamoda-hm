<!-- Inicio: indicadores generales y acceso directo a cada pregunta, filtrable por rol. -->
<script setup lang="ts">
import { AUDIENCIAS, seccionesPara, type Audiencia } from '~/shared/navegacion'

const rol = ref<Audiencia | undefined>()
const preguntas = computed(() => seccionesPara(rol.value))
</script>

<template>
  <div class="space-y-8">
    <TarjetasResumen />

    <section class="space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <h2 class="text-lg font-semibold">¿Qué necesitas saber?</h2>
        <div class="flex flex-wrap gap-2">
          <UButton size="sm" color="neutral" :variant="!rol ? 'solid' : 'outline'" label="Todas" @click="rol = undefined" />
          <UButton v-for="a in AUDIENCIAS" :key="a" size="sm" color="neutral" :variant="rol === a ? 'solid' : 'outline'" :label="a" @click="rol = a" />
        </div>
      </div>
      <div class="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        <NuxtLink v-for="s in preguntas" :key="s.slug" :to="`/${s.slug}`" class="group">
          <UCard class="h-full transition group-hover:ring-2 group-hover:ring-primary">
            <div class="flex items-start gap-3">
              <UIcon :name="s.icono" class="mt-0.5 size-5 shrink-0 text-primary" />
              <div class="space-y-1.5">
                <p class="text-xs font-semibold tracking-wide text-primary uppercase">{{ s.menu }}</p>
                <p class="font-medium">{{ s.pregunta }}</p>
                <div class="flex flex-wrap gap-1 pt-0.5">
                  <UBadge v-for="a in s.para.length ? s.para : ['Todos']" :key="a" :label="a" size="sm" color="neutral" variant="subtle" />
                </div>
              </div>
            </div>
          </UCard>
        </NuxtLink>
      </div>
    </section>
  </div>
</template>
