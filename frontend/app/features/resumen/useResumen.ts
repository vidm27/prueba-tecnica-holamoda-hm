import { useQuery } from '@tanstack/vue-query'
import type { Resumen } from './tipos'

export function useResumen() {
  const api = useApi()
  return useQuery({ queryKey: ['resumen'], queryFn: () => api<Resumen>('/resumen') })
}
