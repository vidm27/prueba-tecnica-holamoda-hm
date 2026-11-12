/** Menú lateral: cada ítem es una pregunta de negocio. `menu` es la versión corta; `pregunta`, el título de la página. */
export type Audiencia = 'Marketing' | 'Ventas' | 'Finanzas'
export const AUDIENCIAS: Audiencia[] = ['Marketing', 'Ventas', 'Finanzas']

/** `para`: a quién le sirve la respuesta; vacío = a todos. */
export interface Seccion { slug: string; menu: string; pregunta: string; icono: string; para: Audiencia[] }

export const GRUPOS: { titulo: string; secciones: Seccion[] }[] = [
  {
    titulo: 'Productos',
    secciones: [
      { slug: 'promocion', menu: '¿Qué promocionar?', pregunta: '¿De qué producto lanzar una promoción o descuento?', icono: 'i-lucide-megaphone', para: ['Marketing'] },
      { slug: 'satisfaccion', menu: '¿Qué gusta menos?', pregunta: '¿Qué productos tienen peor satisfacción?', icono: 'i-lucide-thumbs-down', para: ['Marketing', 'Ventas'] },
      { slug: 'tallas', menu: '¿Qué tallas comprar?', pregunta: '¿Qué curva de tallas comprar por categoría?', icono: 'i-lucide-ruler', para: ['Ventas'] },
      { slug: 'abastecimiento', menu: '¿Cuándo abastecer?', pregunta: '¿Cuándo abastecer cada producto?', icono: 'i-lucide-calendar-range', para: ['Ventas', 'Finanzas'] },
    ],
  },
  {
    titulo: 'Clientes',
    secciones: [
      { slug: 'alto-valor', menu: '¿Quién vale más?', pregunta: '¿Quién es el cliente de alto valor?', icono: 'i-lucide-gem', para: ['Marketing', 'Finanzas'] },
      { slug: 'suscripcion', menu: '¿Sirve la suscripción?', pregunta: '¿Vale la pena la suscripción?', icono: 'i-lucide-repeat', para: ['Finanzas', 'Marketing'] },
      { slug: 'envios', menu: '¿Qué envío prefieren?', pregunta: '¿Qué tipo de envío prefiere cada segmento?', icono: 'i-lucide-truck', para: ['Ventas', 'Finanzas'] },
    ],
  },
  {
    titulo: 'Territorio',
    secciones: [
      { slug: 'estados', menu: '¿Qué se vende dónde?', pregunta: '¿Qué producto se mueve más por estado, en qué talla y color?', icono: 'i-lucide-map', para: ['Ventas', 'Marketing'] },
    ],
  },
  {
    titulo: 'Confianza',
    secciones: [
      { slug: 'calidad', menu: 'Calidad de los datos', pregunta: '¿Qué tan confiables son los datos?', icono: 'i-lucide-shield-check', para: [] },
      { slug: 'hipotesis', menu: 'Probar una hipótesis', pregunta: '¿Esta diferencia es real o es azar?', icono: 'i-lucide-flask-conical', para: [] },
    ],
  },
]

export const SECCIONES = GRUPOS.flatMap((g) => g.secciones)
export const buscarSeccion = (slug: string) => SECCIONES.find((s) => s.slug === slug)

/** Preguntas para un rol; sin rol, todas. Las de "Confianza" (para todos) siempre aparecen. */
export const seccionesPara = (rol?: Audiencia) =>
  SECCIONES.filter((s) => !rol || s.para.length === 0 || s.para.includes(rol))
