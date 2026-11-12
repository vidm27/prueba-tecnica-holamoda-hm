export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  ssr: false, // SPA: la app está detrás de login, no hay nada que indexar
  devtools: { enabled: false },
  modules: ['@nuxt/ui'],
  css: ['~/assets/css/main.css'],
  // Vertical slicing: cada funcionalidad vive en app/features/<nombre>/ con sus componentes,
  // composables y tipos; lo transversal está en app/shared/.
  components: [{ path: '~/features', pathPrefix: false }, { path: '~/shared', pathPrefix: false }],
  imports: { dirs: ['shared/*.ts', 'features/*/*.ts'] },
  runtimeConfig: {
    public: { apiBase: 'http://localhost:8000' }, // NUXT_PUBLIC_API_BASE
  },
  app: { head: { title: 'Tendencias de compra · Hola Moda' } },
})
