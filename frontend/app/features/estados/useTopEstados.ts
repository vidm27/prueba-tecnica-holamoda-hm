import { useQuery } from '@tanstack/vue-query'

export interface TopEstado {
  estado: string
  producto: string
  ventas_producto: number
  ventas_estado: number
  productos_empatados: number
  talla: string
  ventas_talla: number
  color: string
  ventas_color: number
  muestra_suficiente: boolean
}

export function useTopEstados() {
  const api = useApi()
  return useQuery({ queryKey: ['top-estados'], queryFn: () => api<TopEstado[]>('/estados/top-productos') })
}
