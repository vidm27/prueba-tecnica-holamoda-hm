import { describe, expect, it } from 'vitest'
import { SECCIONES, buscarSeccion, seccionesPara } from './navegacion'

describe('navegación', () => {
  const slugs = SECCIONES.map((s) => s.slug)
  it('no repite rutas', () => expect(new Set(slugs).size).toBe(slugs.length))
  it('encuentra una sección por su ruta', () => expect(buscarSeccion('tallas')?.menu).toBe('¿Qué tallas comprar?'))
  it('devuelve undefined si la ruta no existe', () => expect(buscarSeccion('nada')).toBeUndefined())
  it('sin rol muestra todas', () => expect(seccionesPara()).toHaveLength(SECCIONES.length))
  it('filtra por rol y mantiene las de confianza', () => {
    const finanzas = seccionesPara('Finanzas').map((s) => s.slug)
    expect(finanzas).toContain('suscripcion')
    expect(finanzas).toContain('calidad')
    expect(finanzas).not.toContain('promocion')
  })
})
