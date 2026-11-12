import { useQuery } from '@tanstack/vue-query'

export type Recomendacion = 'promocion_exposicion' | 'revisar_producto' | 'riesgo_reputacion' | 'mantener'

/** Cómo se muestra cada recomendación de la API, en lenguaje de negocio. */
export const RECOMENDACIONES: Record<Recomendacion, { texto: string; accion: string; color: string }> = {
  promocion_exposicion: { texto: 'Promover', accion: 'Gusta pero se vende poco: darle visibilidad.', color: '#16a34a' },
  revisar_producto: { texto: 'Revisar', accion: 'Se vende poco y gusta poco: un descuento no lo arregla.', color: '#d97706' },
  riesgo_reputacion: { texto: 'Cuidar', accion: 'Se vende mucho pero gusta poco: riesgo de reputación.', color: '#dc2626' },
  mantener: { texto: 'Mantener', accion: 'Se vende y gusta: no necesita promoción.', color: '#a1a1aa' },
}

export interface ProductoPromocion {
  producto: string
  categoria: string
  ventas: number
  calificacion: number
  pct_descuento: number
  pct_mujeres: number
  ticket_con_descuento: number | null
  ticket_sin_descuento: number | null
  recomendacion: Recomendacion
  motivo: string
}

export interface Promociones {
  mediana_ventas: number
  mediana_calificacion: number
  compras_mujeres_con_descuento: number
  advertencia: string
  productos: ProductoPromocion[]
}

export function usePromociones() {
  const api = useApi()
  return useQuery({ queryKey: ['promociones'], queryFn: () => api<Promociones>('/productos/promocion') })
}
