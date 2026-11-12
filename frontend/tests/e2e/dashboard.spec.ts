import { test, expect } from '@playwright/test'
import { prepararMocksApi, autenticarSesion, limpiarSesion } from './helpers'

test.describe('Autenticación y Control de Acceso', () => {
  test.beforeEach(async ({ page }) => {
    await prepararMocksApi(page)
  })

  test('redirige automáticamente al login si no hay token en sesión', async ({ page }) => {
    await limpiarSesion(page)
    await page.goto('/')
    await expect(page).toHaveURL(/.*\/login/)
    await expect(page.getByRole('heading', { name: 'Hola Moda' })).toBeVisible()
    await expect(page.locator('input[type="text"]')).toBeVisible()
    await expect(page.locator('input[type="password"]')).toBeVisible()
  })

  test('permite iniciar sesión con credenciales correctas y redirige a inicio', async ({ page }) => {
    await limpiarSesion(page)
    await page.goto('/login')
    await page.locator('input[type="text"]').fill('admin')
    await page.locator('input[type="password"]').fill('admin123')
    await page.locator('button[type="submit"]').click()

    await expect(page).toHaveURL(/\//)
    await expect(page.getByText('Tendencias de compra')).toBeVisible()
  })
})

test.describe('Navegación y Módulos de Analítica', () => {
  test.beforeEach(async ({ page }) => {
    await prepararMocksApi(page)
    await autenticarSesion(page)
  })

  test('muestra indicadores del inicio y filtra módulos por rol', async ({ page }) => {
    await page.goto('/')
    // Verifica KPIs del inicio
    await expect(page.getByText('Ingreso total')).toBeVisible()
    await expect(page.getByText('Ticket promedio')).toBeVisible()

    // Verifica botones de filtro de audiencia
    await expect(page.getByRole('button', { name: 'Todos' })).toBeVisible()
    const btnMarketing = page.getByRole('button', { name: 'Marketing' })
    await expect(btnMarketing).toBeVisible()

    // Filtra por Marketing y verifica que permanezca visible Promoción y satisfacción en el inicio
    await btnMarketing.click()
    await expect(page.getByRole('link', { name: 'Promoción y satisfacción', exact: true })).toBeVisible()
  })

  test('módulo de Promoción y satisfacción: tarjeta de sesgo y cuadrantes', async ({ page }) => {
    await page.goto('/promocion')
    // Verifica encabezado unificado
    await expect(page.getByRole('heading', { name: /Oportunidades de promoción/ })).toBeVisible()
    await expect(page.getByRole('heading', { name: /Productos que menos gustan/ })).toBeVisible()

    // Verifica la barra interactiva de posicionamiento por género y oportunidad comercial
    await expect(page.getByText('Oportunidades de promoción y posicionamiento por género')).toBeVisible()
    await expect(page.getByRole('button', { name: 'Mujeres' })).toBeVisible()

    // Verifica presencia de cuadrantes interactivos
    await expect(page.getByRole('button', { name: /^Promover/ })).toBeVisible()
    await expect(page.getByRole('button', { name: /^Cuidar/ })).toBeVisible()
  })

  test('módulo de Curva de tallas: cards de tallas y tabla de datos', async ({ page }) => {
    await page.goto('/tallas')
    await expect(page.locator('span').filter({ hasText: /^Talla S$/ })).toBeVisible()
    await expect(page.locator('span').filter({ hasText: /^Talla M$/ })).toBeVisible()
    await expect(page.getByText('¿Cambia la talla según el tipo de prenda?')).toBeVisible()
  })

  test('módulo de Abastecimiento: abre por defecto en Guía visual', async ({ page }) => {
    await page.goto('/abastecimiento')
    // Verifica que el modo activo por defecto sea la Guía visual
    await expect(page.getByText(/Guía visual por prenda/)).toBeVisible()
    await expect(page.getByRole('button', { name: /^Primavera/ })).toBeVisible()
    await expect(page.getByRole('button', { name: /^Verano/ })).toBeVisible()
  })

  test('módulo de Clientes - Más valiosos: radiografía de cuartiles', async ({ page }) => {
    await page.goto('/alto-valor')
    await expect(page.getByRole('button', { name: /^Platino/ })).toBeVisible()
    await expect(page.getByRole('button', { name: /^Bronce/ })).toBeVisible()
    await expect(page.getByText('Distribución del gasto anual')).toBeVisible()
  })

  test('módulo de Clientes - Suscripciones y Envíos', async ({ page }) => {
    await page.goto('/suscripcion')
    await expect(page.getByText('Proporción de suscripción')).toBeVisible()
    await expect(page.getByText('Comparativa directa: Suscritos vs. No suscritos')).toBeVisible()

    await page.goto('/envios')
    await expect(page.getByText('Modalidades de envío', { exact: true })).toBeVisible()
    await expect(page.getByText('Reparto uniforme esperado')).toBeVisible()
  })

  test('módulo de Ventas por estado: estados con líder claro', async ({ page }) => {
    await page.goto('/estados')
    await expect(page.getByText('Estados analizados')).toBeVisible()
    await expect(page.getByText('Con producto líder claro', { exact: true })).toBeVisible()
    await expect(page.locator('p.font-bold', { hasText: 'California' })).toBeVisible()
  })
})
