/**
 * Convierte un código HTTP en un mensaje para la persona, no para el desarrollador.
 * El 422 conserva el mensaje del backend: ya viene en español y dice qué filtro revisar.
 */
export function mensajeAmigable(estado: number, mensajeBackend = ''): string {
  if (estado === 422 && mensajeBackend) return mensajeBackend
  if (estado === 0) return 'No hay conexión con el servidor. Revisa tu internet e intenta de nuevo.'
  if (estado === 401) return 'Tu sesión venció. Vuelve a iniciar sesión.'
  if (estado === 403) return 'No tienes permiso para ver esta información.'
  if (estado === 404) return 'No encontramos la información que buscas.'
  if (estado === 429) return 'Hiciste demasiadas solicitudes. Espera un minuto e intenta de nuevo.'
  if (estado >= 500) return 'El servidor tuvo un problema. Intenta de nuevo en unos minutos.'
  return 'Ocurrió un error inesperado. Intenta de nuevo.'
}
