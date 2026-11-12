import { useQuery } from '@tanstack/vue-query'

export interface Hallazgo {
  regla: string
  descripcion: string
  severidad: 'alta' | 'media' | 'baja' | string
  filas_afectadas: number
  total_filas: number
  evidencia: Record<string, unknown>
}

export function useAuditoria() {
  const api = useApi()
  return useQuery({ queryKey: ['auditoria'], queryFn: () => api<Hallazgo[]>('/calidad/auditoria') })
}
