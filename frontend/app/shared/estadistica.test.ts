import { describe, expect, it } from 'vitest'
import { CHI2_4_TEMPORADAS_25_PRODUCTOS, chiCuadradoParejo } from './estadistica'
import { es } from './traduccion'

describe('chi-cuadrado contra reparto parejo', () => {
  it('es 0 si todo es igual', () => expect(chiCuadradoParejo([40, 40, 40, 40])).toBe(0))
  it('no marca como estacional una variación típica de azar', () =>
    expect(chiCuadradoParejo([37, 27, 50, 40])).toBeLessThan(CHI2_4_TEMPORADAS_25_PRODUCTOS))
  it('marca una concentración fuerte', () =>
    expect(chiCuadradoParejo([80, 20, 30, 26])).toBeGreaterThan(CHI2_4_TEMPORADAS_25_PRODUCTOS))
  it('no falla con ceros', () => expect(chiCuadradoParejo([0, 0, 0, 0])).toBe(0))
})

describe('traducción', () => {
  it('traduce términos conocidos', () => expect(es('Sunglasses')).toBe('Lentes de sol'))
  it('deja igual lo desconocido', () => expect(es('Montana')).toBe('Montana'))
})
