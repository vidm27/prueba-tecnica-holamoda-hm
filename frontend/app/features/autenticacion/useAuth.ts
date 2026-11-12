const CLAVE = 'token'

/** Token en memoria + sessionStorage (se borra al cerrar la pestaña). */
export function useAuth() {
  const token = useState<string | null>('token', () => import.meta.client ? sessionStorage.getItem(CLAVE) : null)

  async function entrar(usuario: string, clave: string) {
    const { apiBase } = useRuntimeConfig().public
    try {
      const r = await $fetch<{ access_token: string }>('/api/v1/auth/login', {
        baseURL: apiBase, method: 'POST',
        body: new URLSearchParams({ username: usuario, password: clave }),
      })
      token.value = r.access_token
      sessionStorage.setItem(CLAVE, r.access_token)
    } catch (e: any) {
      const mensajes: Record<number, string> = { 401: 'Usuario o clave incorrectos' }
      throw new Error(mensajes[e?.status] ?? (e?.status === 429 ? e.data?.error?.mensaje : 'No se pudo conectar con la API'))
    }
  }

  function salir() {
    token.value = null
    sessionStorage.removeItem(CLAVE)
    useQueryClient().clear()
    return navigateTo('/login')
  }

  return { token, autenticado: computed(() => !!token.value), entrar, salir }
}
