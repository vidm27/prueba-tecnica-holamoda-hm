export class ErrorApi extends Error {
  constructor(public estado: number, mensaje: string) { super(mensaje) }
}

/** Cliente de la API: agrega el JWT y cierra sesión si el token venció (401). */
export function useApi() {
  const { apiBase } = useRuntimeConfig().public
  const { token, salir } = useAuth()

  return async function api<T>(ruta: string, params?: Record<string, string | number | undefined>): Promise<T> {
    try {
      return await $fetch<T>(`/api/v1${ruta}`, {
        baseURL: apiBase, params,
        headers: { Authorization: `Bearer ${token.value}` },
      })
    } catch (e: any) {
      if (e?.status === 401) await salir()
      throw new ErrorApi(e?.status ?? 0, e?.data?.error?.mensaje ?? 'Error al consultar la API')
    }
  }
}
