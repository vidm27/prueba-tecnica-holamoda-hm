<script setup lang="ts">
const { entrar } = useAuth()
const estado = reactive({ usuario: '', clave: '' })
const error = ref('')
const cargando = ref(false)

async function enviar() {
  error.value = ''
  cargando.value = true
  try {
    await entrar(estado.usuario, estado.clave)
    await navigateTo('/')
  } catch (e: any) {
    error.value = e.message
  } finally {
    cargando.value = false
  }
}
</script>

<template>
  <UCard>
    <template #header><h1 class="text-lg font-semibold">Iniciar sesión</h1></template>
    <UForm :state="estado" class="space-y-4" @submit="enviar">
      <UFormField label="Usuario" name="usuario">
        <UInput v-model="estado.usuario" autocomplete="username" autofocus class="w-full" />
      </UFormField>
      <UFormField label="Clave" name="clave">
        <UInput v-model="estado.clave" type="password" autocomplete="current-password" class="w-full" />
      </UFormField>
      <UAlert v-if="error" color="error" variant="subtle" icon="i-lucide-circle-alert" :description="error" />
      <UButton type="submit" block :loading="cargando" :disabled="!estado.usuario || !estado.clave" label="Entrar" />
    </UForm>
  </UCard>
</template>
