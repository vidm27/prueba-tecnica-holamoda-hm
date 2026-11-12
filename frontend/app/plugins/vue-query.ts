import { QueryClient, VueQueryPlugin } from '@tanstack/vue-query'
import { ErrorApi } from '~/shared/useApi'

export default defineNuxtPlugin((app) => {
  const cliente = new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 60_000, // los datos cambian solo cuando se corre el ETL
        refetchOnWindowFocus: false,
        retry: (intentos, error) => !(error instanceof ErrorApi && error.estado < 500) && intentos < 2,
      },
    },
  })
  app.vueApp.use(VueQueryPlugin, { queryClient: cliente })
})
