import { useQuery } from '@tanstack/vue-query'
import type { Ref } from 'vue'

export type Segmento = 'nivel_valor' | 'grupo_edad' | 'genero'
export interface EnvioSegmento { segmento: string; tipo_envio: string; compras: number; pct_segmento: number }

export function useEnvios(segmento: Ref<Segmento>) {
  const api = useApi()
  return useQuery({ queryKey: ['envios', segmento], queryFn: () => api<EnvioSegmento[]>('/envios/por-segmento', { segmento: segmento.value }) })
}
