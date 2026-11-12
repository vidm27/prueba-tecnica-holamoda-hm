import { useQuery } from '@tanstack/vue-query'

export interface ImpactoSuscripcion {
  suscrito: boolean
  clientes: number
  ticket_promedio: number
  compras_previas_promedio: number
  calificacion_promedio: number
  gasto_anual_promedio: number
}

export function useSuscripcion() {
  const api = useApi()
  return useQuery({ queryKey: ['suscripcion'], queryFn: () => api<ImpactoSuscripcion[]>('/suscripcion/impacto') })
}
