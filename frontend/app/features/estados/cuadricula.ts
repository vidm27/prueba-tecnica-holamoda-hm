/** Mapa de EE.UU. como cuadrícula de fichas (una por estado), sin librería de mapas. */
const F: [string, string, number, number][] = [
  ['Alaska', 'AK', 0, 0], ['Maine', 'ME', 10, 0],
  ['Vermont', 'VT', 9, 1], ['New Hampshire', 'NH', 10, 1],
  ['Washington', 'WA', 0, 2], ['Idaho', 'ID', 1, 2], ['Montana', 'MT', 2, 2], ['North Dakota', 'ND', 3, 2], ['Minnesota', 'MN', 4, 2],
  ['Illinois', 'IL', 5, 2], ['Wisconsin', 'WI', 6, 2], ['Michigan', 'MI', 7, 2], ['New York', 'NY', 8, 2], ['Rhode Island', 'RI', 9, 2], ['Massachusetts', 'MA', 10, 2],
  ['Oregon', 'OR', 0, 3], ['Nevada', 'NV', 1, 3], ['Wyoming', 'WY', 2, 3], ['South Dakota', 'SD', 3, 3], ['Iowa', 'IA', 4, 3],
  ['Indiana', 'IN', 5, 3], ['Ohio', 'OH', 6, 3], ['Pennsylvania', 'PA', 7, 3], ['New Jersey', 'NJ', 8, 3], ['Connecticut', 'CT', 9, 3],
  ['California', 'CA', 0, 4], ['Utah', 'UT', 1, 4], ['Colorado', 'CO', 2, 4], ['Nebraska', 'NE', 3, 4], ['Missouri', 'MO', 4, 4],
  ['Kentucky', 'KY', 5, 4], ['West Virginia', 'WV', 6, 4], ['Virginia', 'VA', 7, 4], ['Maryland', 'MD', 8, 4], ['Delaware', 'DE', 9, 4],
  ['Arizona', 'AZ', 1, 5], ['New Mexico', 'NM', 2, 5], ['Kansas', 'KS', 3, 5], ['Arkansas', 'AR', 4, 5], ['Tennessee', 'TN', 5, 5],
  ['North Carolina', 'NC', 6, 5], ['South Carolina', 'SC', 7, 5], ['District of Columbia', 'DC', 8, 5],
  ['Oklahoma', 'OK', 3, 6], ['Louisiana', 'LA', 4, 6], ['Mississippi', 'MS', 5, 6], ['Alabama', 'AL', 6, 6], ['Georgia', 'GA', 7, 6],
  ['Hawaii', 'HI', 0, 7], ['Texas', 'TX', 3, 7], ['Florida', 'FL', 8, 7],
]

export const CUADRICULA: Record<string, { abrev: string; col: number; fila: number }> =
  Object.fromEntries(F.map(([nombre, abrev, col, fila]) => [nombre, { abrev, col, fila }]))
