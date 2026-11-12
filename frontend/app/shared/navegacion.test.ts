import { describe, expect, it } from 'vitest'
import { SECCIONES, buscarSeccion, seccionesPara } from './navegacion'

describe('navegación', () => {
  const slugs = SECCIONES.map((s) => s.slug)
  it('no repite rutas', () => expect(new Set(slugs).size).toBe(slugs.length))
  it('encuentra una sección por su ruta', () => expect(buscarSeccion('tallas')?.menu).toBe('Curva de tallas'))
  it('devuelve undefined si la ruta no existe', () => expect(buscarSeccion('nada')).toBeUndefined())
  it('sin rol muestra todas las visibles', () => expect(seccionesPara()).toHaveLength(SECCIONES.filter((s) => !s.oculto).length))
  it('filtra por rol y excluye las secciones ocultas', () => {
    const finanzas = seccionesPara('Finanzas').map((s) => s.slug)
    expect(finanzas).toContain('suscripcion')
    expect(finanzas).not.toContain('calidad')
    expect(finanzas).not.toContain('hipotesis')
    expect(finanzas).not.toContain('promocion')
  })
  it('oculta el grupo de confianza pero permite resolverlo por ruta', () => {
    expect(seccionesPara().some((s) => s.slug === 'hipotesis')).toBe(false)
    expect(seccionesPara().some((s) => s.slug === 'calidad')).toBe(false)
    expect(buscarSeccion('hipotesis')?.menu).toBe('Prueba de hipótesis')
    expect(buscarSeccion('calidad')?.menu).toBe('Calidad de datos')
  })
})
