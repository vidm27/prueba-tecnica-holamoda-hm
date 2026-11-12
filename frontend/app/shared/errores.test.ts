import { describe, expect, it } from 'vitest'
import { mensajeAmigable } from './errores'

describe('mensajeAmigable', () => {
  it('explica la falta de conexión sin jerga técnica', () => expect(mensajeAmigable(0)).toMatch(/conexión/))
  it('conserva el mensaje en español del backend para 422', () =>
    expect(mensajeAmigable(422, 'No hay variación suficiente para comparar los grupos')).toBe('No hay variación suficiente para comparar los grupos'))
  it('no muestra detalles técnicos en errores del servidor', () => {
    const texto = mensajeAmigable(500, 'Traceback (most recent call last)')
    expect(texto).not.toMatch(/Traceback|500/)
  })
})
