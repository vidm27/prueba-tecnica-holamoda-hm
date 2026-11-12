export const moneda = (n: number) =>
  new Intl.NumberFormat('es-PA', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(n)

export const entero = (n: number) => new Intl.NumberFormat('es-PA').format(n)

/** Fracción (0.43) a porcentaje ("43%"). */
export const fraccion = (f: number, decimales = 0) => `${(f * 100).toFixed(decimales)}%`
