import { test, expect } from '@playwright/test'

/**
 * Fixture con mocks de todas las respuestas de la API analítica
 * para pruebas E2E deterministas e independientes de la base de datos real.
 */
export async function prepararMocksApi(page: any) {
  // Login exitoso
  await page.route('**/api/v1/auth/login', async (route: any) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ access_token: 'fake-jwt-token-playwright', token_type: 'bearer' }),
    })
  })

  // Resumen / KPIs
  await page.route('**/api/v1/resumen', async (route: any) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        ingreso_total: 233081,
        compras: 3900,
        clientes: 3900,
        productos: 25,
        ticket_promedio: 59.76,
        calificacion_promedio: 3.75,
      }),
    })
  })

  // Auditoría de calidad
  await page.route('**/api/v1/calidad/auditoria', async (route: any) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        {
          regla: 'beneficios_por_genero',
          severidad: 'alta',
          descripcion: 'Ninguna mujer tiene suscripción ni descuento.',
          filas_afectadas: 1248,
          total_filas: 3900,
          evidencia: { mujeres_con_descuento: 0, mujeres_suscritas: 0 },
        },
      ]),
    })
  })

  // Promociones
  await page.route('**/api/v1/productos/promocion', async (route: any) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        mediana_ventas: 157,
        mediana_calificacion: 3.75,
        compras_mujeres_con_descuento: 0,
        advertencia: 'Datos simulados con calificaciones en décimas.',
        productos: [
          {
            producto: 'Backpack',
            categoria: 'Accessories',
            ventas: 140,
            calificacion: 3.85,
            pct_descuento: 40,
            pct_mujeres: 30,
            ticket_con_descuento: 55,
            ticket_sin_descuento: 60,
            recomendacion: 'promocion_exposicion',
            motivo: 'Buena calificación pero bajas ventas',
          },
          {
            producto: 'Shirt',
            categoria: 'Clothing',
            ventas: 170,
            calificacion: 3.65,
            pct_descuento: 42,
            pct_mujeres: 31,
            ticket_con_descuento: 58,
            ticket_sin_descuento: 62,
            recomendacion: 'riesgo_reputacion',
            motivo: 'Altas ventas pero baja satisfacción',
          },
        ],
      }),
    })
  })

  // Satisfacción
  await page.route('**/api/v1/productos/satisfaccion', async (route: any) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { producto: 'Shirt', categoria: 'Clothing', compras: 169, calificacion: 3.63, margen_error_95: 0.1 },
        { producto: 'Boots', categoria: 'Footwear', compras: 144, calificacion: 3.82, margen_error_95: 0.09 },
      ]),
    })
  })

  // Curva de tallas
  await page.route('**/api/v1/tallas/curva', async (route: any) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { categoria: 'Clothing', talla: 'S', compras: 300, pct: 18 },
        { categoria: 'Clothing', talla: 'M', compras: 700, pct: 44 },
        { categoria: 'Clothing', talla: 'L', compras: 430, pct: 27 },
        { categoria: 'Clothing', talla: 'XL', compras: 180, pct: 11 },
      ]),
    })
  })

  // Abastecimiento / Estacionalidad
  await page.route('**/api/v1/productos/estacionalidad', async (route: any) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        {
          producto: 'Backpack',
          ventas_por_temporada: { Spring: 40, Summer: 35, Fall: 38, Winter: 27 },
          temporada_pico: 'Spring',
          temporada_valle: 'Winter',
        },
      ]),
    })
  })

  // Clientes / Valor
  await page.route('**/api/v1/clientes/valor', async (route: any) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        pareto_top20_pct_gasto: 65,
        niveles: [
          { nivel: 'Bronce', clientes: 975, gasto_anual_total: 25000, pct_gasto: 5, gasto_minimo: 20, gasto_maximo: 150 },
          { nivel: 'Plata', clientes: 975, gasto_anual_total: 50000, pct_gasto: 10, gasto_minimo: 151, gasto_maximo: 350 },
          { nivel: 'Oro', clientes: 975, gasto_anual_total: 100000, pct_gasto: 20, gasto_minimo: 351, gasto_maximo: 850 },
          { nivel: 'Platino', clientes: 975, gasto_anual_total: 325000, pct_gasto: 65, gasto_minimo: 851, gasto_maximo: 5200 },
        ],
      }),
    })
  })

  // Suscripción
  await page.route('**/api/v1/suscripcion/impacto', async (route: any) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        {
          suscrito: false,
          clientes: 2847,
          ticket_promedio: 59.8,
          compras_previas_promedio: 25.1,
          calificacion_promedio: 3.75,
          gasto_anual_promedio: 620.5,
        },
        {
          suscrito: true,
          clientes: 1053,
          ticket_promedio: 59.6,
          compras_previas_promedio: 25.6,
          calificacion_promedio: 3.74,
          gasto_anual_promedio: 618.2,
        },
      ]),
    })
  })

  // Envíos
  await page.route('**/api/v1/envios/por-segmento*', async (route: any) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { segmento: 'Platino', tipo_envio: 'Express', compras: 160, pct_segmento: 16.4 },
        { segmento: 'Platino', tipo_envio: 'Standard', compras: 165, pct_segmento: 16.9 },
        { segmento: 'Bronce', tipo_envio: 'Express', compras: 162, pct_segmento: 16.6 },
        { segmento: 'Bronce', tipo_envio: 'Standard', compras: 163, pct_segmento: 16.7 },
      ]),
    })
  })

  // Estados
  await page.route('**/api/v1/estados/top-productos', async (route: any) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        {
          estado: 'California',
          producto: 'Backpack',
          ventas_producto: 12,
          ventas_estado: 95,
          productos_empatados: 1,
          talla: 'M',
          ventas_talla: 6,
          color: 'Blue',
          ventas_color: 4,
          muestra_suficiente: true,
        },
      ]),
    })
  })
}

/** Inicia sesión simulada inyectando token en sessionStorage o completando formulario */
export async function autenticarSesion(page: any) {
  await page.addInitScript(() => {
    window.sessionStorage.setItem('token', 'fake-jwt-token-playwright')
  })
}

export async function limpiarSesion(page: any) {
  await page.addInitScript(() => {
    window.sessionStorage.clear()
  })
}
