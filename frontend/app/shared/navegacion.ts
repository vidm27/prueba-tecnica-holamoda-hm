/** Menú lateral: cada ítem es una pregunta de negocio. `menu` es la versión corta; `pregunta`, el título de la página. */
export interface Seccion { slug: string; menu: string; pregunta: string; icono: string }

export const GRUPOS: { titulo: string; secciones: Seccion[] }[] = [
  {
    titulo: 'Productos',
    secciones: [
      { slug: 'promocion', menu: '¿Qué promocionar?', pregunta: '¿De qué producto lanzar una promoción o descuento?', icono: 'i-lucide-megaphone' },
      { slug: 'satisfaccion', menu: '¿Qué gusta menos?', pregunta: '¿Qué productos tienen peor satisfacción?', icono: 'i-lucide-thumbs-down' },
      { slug: 'tallas', menu: '¿Qué tallas comprar?', pregunta: '¿Qué curva de tallas comprar por categoría?', icono: 'i-lucide-ruler' },
      { slug: 'abastecimiento', menu: '¿Cuándo abastecer?', pregunta: '¿Cuándo abastecer cada producto?', icono: 'i-lucide-calendar-range' },
    ],
  },
  {
    titulo: 'Clientes',
    secciones: [
      { slug: 'alto-valor', menu: '¿Quién vale más?', pregunta: '¿Quién es el cliente de alto valor?', icono: 'i-lucide-gem' },
      { slug: 'suscripcion', menu: '¿Sirve la suscripción?', pregunta: '¿Vale la pena la suscripción?', icono: 'i-lucide-repeat' },
      { slug: 'envios', menu: '¿Qué envío prefieren?', pregunta: '¿Qué tipo de envío prefiere cada segmento?', icono: 'i-lucide-truck' },
    ],
  },
  {
    titulo: 'Territorio',
    secciones: [
      { slug: 'estados', menu: '¿Qué se vende dónde?', pregunta: '¿Qué producto se mueve más por estado, en qué talla y color?', icono: 'i-lucide-map' },
    ],
  },
  {
    titulo: 'Confianza',
    secciones: [
      { slug: 'calidad', menu: 'Calidad de los datos', pregunta: '¿Qué tan confiables son los datos?', icono: 'i-lucide-shield-check' },
      { slug: 'hipotesis', menu: 'Probar una hipótesis', pregunta: '¿Esta diferencia es real o es azar?', icono: 'i-lucide-flask-conical' },
    ],
  },
]

export const buscarSeccion = (slug: string) => GRUPOS.flatMap((g) => g.secciones).find((s) => s.slug === slug)
