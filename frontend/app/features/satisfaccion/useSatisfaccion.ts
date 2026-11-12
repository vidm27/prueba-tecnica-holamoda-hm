import { useQuery } from '@tanstack/vue-query'

export interface Satisfaccion { producto: string; categoria: string; compras: number; calificacion: number; margen_error_95: number }

export function useSatisfaccion() {
  const api = useApi()
  return useQuery({ queryKey: ['satisfaccion'], queryFn: () => api<Satisfaccion[]>('/productos/satisfaccion') })
}
