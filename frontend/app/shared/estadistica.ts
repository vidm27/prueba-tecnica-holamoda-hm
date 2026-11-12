/** Chi-cuadrado contra un reparto parejo: ¿las ventas se concentran en alguna temporada o grupo? */
export function chiCuadradoParejo(valores: number[]) {
  const esperado = valores.reduce((s, v) => s + v, 0) / valores.length
  return esperado ? valores.reduce((s, v) => s + (v - esperado) ** 2 / esperado, 0) : 0
}

/**
 * Valor crítico de chi-cuadrado con 3 grados de libertad (4 temporadas) para α = 0.05 / 25 productos
 * (corrección de Bonferroni). Por encima de esto, el pico de temporada no se explica por azar.
 */
export const CHI2_4_TEMPORADAS_25_PRODUCTOS = 14.8
