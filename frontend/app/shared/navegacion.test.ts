import { describe, expect, it } from 'vitest'
import { GRUPOS, buscarSeccion } from './navegacion'

describe('navegación', () => {
  const slugs = GRUPOS.flatMap((g) => g.secciones.map((s) => s.slug))
  it('no repite rutas', () => expect(new Set(slugs).size).toBe(slugs.length))
  it('encuentra una sección por su ruta', () => expect(buscarSeccion('tallas')?.menu).toBe('¿Qué tallas comprar?'))
  it('devuelve undefined si la ruta no existe', () => expect(buscarSeccion('nada')).toBeUndefined())
})
