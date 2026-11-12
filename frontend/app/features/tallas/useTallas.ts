import { useQuery } from '@tanstack/vue-query'

export interface CurvaTalla { categoria: string; talla: string; compras: number; pct: number }

export function useTallas() {
  const api = useApi()
  return useQuery({ queryKey: ['tallas'], queryFn: () => api<CurvaTalla[]>('/tallas/curva') })
}
