import { describe, expect, it } from 'vitest'
import { CUADRICULA } from './cuadricula'

describe('cuadrícula de estados', () => {
  const fichas = Object.values(CUADRICULA)
  it('tiene los 50 estados y DC', () => expect(fichas).toHaveLength(51))
  it('no superpone fichas', () => expect(new Set(fichas.map((f) => `${f.col},${f.fila}`)).size).toBe(51))
  it('abreviaturas únicas', () => expect(new Set(fichas.map((f) => f.abrev)).size).toBe(51))
})
