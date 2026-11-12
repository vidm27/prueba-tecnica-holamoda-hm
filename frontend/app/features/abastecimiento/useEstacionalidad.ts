import { useQuery } from '@tanstack/vue-query'

export interface Estacionalidad {
  producto: string
  ventas_por_temporada: Record<string, number>
  temporada_pico: string
  temporada_valle: string
}

export function useEstacionalidad() {
  const api = useApi()
  return useQuery({ queryKey: ['estacionalidad'], queryFn: () => api<Estacionalidad[]>('/productos/estacionalidad') })
}
