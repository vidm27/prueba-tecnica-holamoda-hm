import { useQuery } from '@tanstack/vue-query'

export interface NivelValor {
  nivel: string
  clientes: number
  gasto_anual_total: number
  pct_gasto: number
  gasto_minimo: number
  gasto_maximo: number
}
export interface Valor { pareto_top20_pct_gasto: number; niveles: NivelValor[] }

export function useValor() {
  const api = useApi()
  return useQuery({ queryKey: ['valor'], queryFn: () => api<Valor>('/clientes/valor') })
}
