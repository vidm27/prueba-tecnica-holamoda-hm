import { useQuery } from '@tanstack/vue-query'
import type { Ref } from 'vue'

export interface ResultadoHipotesis {
  metrica: string
  variable: string
  prueba: string
  estadistico: number
  p_valor: number
  p_ajustado: number
  significativo: boolean
  veredicto: string
  grupos: { grupo: string; n: number; media: number }[]
}

export function useHipotesis(metrica: Ref<string>, variable: Ref<string>) {
  const api = useApi()
  return useQuery({
    queryKey: ['hipotesis', metrica, variable],
    queryFn: () => api<ResultadoHipotesis>('/hipotesis', { metrica: metrica.value, variable: variable.value }),
  })
}
