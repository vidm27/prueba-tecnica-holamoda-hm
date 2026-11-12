import { describe, expect, it } from 'vitest'
import { entero, fraccion, moneda } from './formato'

describe('formato', () => {
  it('formatea dólares sin decimales', () => expect(moneda(59.76)).toContain('60'))
  it('separa miles', () => expect(entero(3900)).toMatch(/3\D?900/))
  it('convierte fracción a porcentaje', () => expect(fraccion(0.428)).toBe('43%'))
})
