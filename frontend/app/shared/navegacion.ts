/** Menú lateral: cada ítem es una pregunta de negocio. `menu` es la versión corta; `pregunta`, el título de la página. */
export type Audiencia = 'Marketing' | 'Ventas' | 'Finanzas'
export const AUDIENCIAS: Audiencia[] = ['Marketing', 'Ventas', 'Finanzas']

/** `para`: a quién le sirve la respuesta; vacío = a todos. */
export interface Seccion { slug: string; menu: string; pregunta: string; icono: string; para: Audiencia[] }

export const GRUPOS: { titulo: string; secciones: Seccion[] }[] = [
  {
    titulo: 'Productos',
    secciones: [
      {
        slug: 'promocion',
        menu: 'Promoción y satisfacción',
        pregunta: 'Posicionamiento de catálogo, oportunidades de visibilidad y nivel de satisfacción',
        icono: 'i-lucide-megaphone',
        para: ['Marketing', 'Ventas'],
      },
      { slug: 'tallas', menu: 'Curva de tallas', pregunta: 'Distribución de tallas vendidas por categoría de producto', icono: 'i-lucide-ruler', para: ['Ventas'] },
      { slug: 'abastecimiento', menu: 'Abastecimiento', pregunta: 'Comportamiento de demanda y estacionalidad por producto', icono: 'i-lucide-calendar-range', para: ['Ventas', 'Finanzas'] },
    ],
  },
  {
    titulo: 'Clientes',
    secciones: [
      {
        slug: 'clientes',
        menu: 'Valor, suscripción y envíos',
        pregunta: 'Segmentación por valor anual, impacto de suscripción y preferencias de envío',
        icono: 'i-lucide-users',
        para: ['Marketing', 'Ventas', 'Finanzas'],
      },
    ],
  },
  {
    titulo: 'Territorio',
    secciones: [
      { slug: 'estados', menu: 'Ventas por estado', pregunta: 'Mapa de demanda geográfica, tallas y colores por estado', icono: 'i-lucide-map', para: ['Ventas', 'Marketing'] },
    ],
  },
  {
    titulo: 'Confianza',
    secciones: [
      { slug: 'calidad', menu: 'Calidad de datos', pregunta: 'Auditoría estructural y estadística del conjunto de datos', icono: 'i-lucide-shield-check', para: [] },
      { slug: 'hipotesis', menu: 'Prueba de hipótesis', pregunta: 'Laboratorio estadístico con corrección por comparaciones múltiples', icono: 'i-lucide-flask-conical', para: [] },
    ],
  },
]

export const SECCIONES = GRUPOS.flatMap((g) => g.secciones)
export const buscarSeccion = (slug: string) => SECCIONES.find((s) => s.slug === slug)

/** Preguntas para un rol; sin rol, todas. Las de "Confianza" (para todos) siempre aparecen. */
export const seccionesPara = (rol?: Audiencia) =>
  SECCIONES.filter((s) => !rol || s.para.length === 0 || s.para.includes(rol))
