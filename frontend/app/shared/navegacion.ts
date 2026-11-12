/** Menú lateral: cada ítem es una pregunta de negocio. `menu` es la versión corta; `pregunta`, el título de la página. */
export type Audiencia = 'Marketing' | 'Ventas' | 'Finanzas'
export const AUDIENCIAS: Audiencia[] = ['Marketing', 'Ventas', 'Finanzas']

/** `para`: a quién le sirve la respuesta; vacío = a todos. */
export interface Seccion {
  slug: string
  menu: string
  pregunta: string
  icono: string
  para: Audiencia[]
  oculto?: boolean
}

export interface GrupoNavegacion {
  titulo: string
  oculto?: boolean
  secciones: Seccion[]
}

export const GRUPOS: GrupoNavegacion[] = [
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
      { slug: 'alto-valor', menu: 'Más valiosos', pregunta: 'Segmentación de clientes y concentración del gasto anual', icono: 'i-lucide-gem', para: ['Marketing', 'Finanzas'] },
      { slug: 'suscripcion', menu: 'Suscripciones', pregunta: 'Comparativa de desempeño entre clientes suscritos y no suscritos', icono: 'i-lucide-repeat', para: ['Finanzas', 'Marketing'] },
      { slug: 'envios', menu: 'Preferencia de envío', pregunta: 'Distribución de modalidades de envío por segmento de cliente', icono: 'i-lucide-truck', para: ['Ventas', 'Finanzas'] },
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
    oculto: true,
    secciones: [
      { slug: 'calidad', menu: 'Calidad de datos', pregunta: 'Auditoría estructural y estadística del conjunto de datos', icono: 'i-lucide-shield-check', para: [], oculto: true },
      { slug: 'hipotesis', menu: 'Prueba de hipótesis', pregunta: 'Laboratorio estadístico con corrección por comparaciones múltiples', icono: 'i-lucide-flask-conical', para: [], oculto: true },
    ],
  },
]

export const SECCIONES = GRUPOS.flatMap((g) => g.secciones)
export const buscarSeccion = (slug: string) => SECCIONES.find((s) => s.slug === slug)

/** Preguntas visibles para un rol; sin rol, todas las visibles (excluye las ocultas como Confianza). */
export const seccionesPara = (rol?: Audiencia) =>
  SECCIONES.filter((s) => !s.oculto && (!rol || s.para.length === 0 || s.para.includes(rol)))
