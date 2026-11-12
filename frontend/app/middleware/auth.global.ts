export default defineNuxtRouteMiddleware((to) => {
  const { autenticado } = useAuth()
  if (!autenticado.value && to.path !== '/login') return navigateTo('/login')
  if (autenticado.value && to.path === '/login') return navigateTo('/')
})
