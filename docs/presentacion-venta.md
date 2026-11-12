# Tendencias de compra · Hola Moda

**Sabe qué vender, a quién y en qué talla, antes de decidir una promoción o un pedido.**

Una plataforma de analítica de compras que convierte los datos de venta en decisiones concretas, y que
dice con honestidad cuándo los datos no alcanzan para decidir.

---

# Parte 1 · Propuesta comercial

## El problema

Las promociones y los pedidos de inventario se deciden con intuición o con reportes que responden
"qué pasó", pero no "qué conviene hacer". Eso se traduce en:

- Descuentos a productos que ya se venden bien, que no aumentan el ingreso.
- Inventario mal distribuido entre tallas.
- Esfuerzo de retención dirigido a todos los clientes por igual, cuando el valor está concentrado.

## La solución

Ocho preguntas de negocio, respondidas con los datos de compra en segundos, cada una con su evidencia:

| Pregunta | Qué obtiene el negocio |
|---|---|
| ¿Qué producto promocionar? | Productos bien calificados con poco volumen, donde falta visibilidad. |
| ¿Qué se mueve por estado, y en qué talla y color? | Producto líder por estado, con cuántas ventas lo respaldan. |
| ¿Qué curva de tallas comprar? | Reparto de tallas por categoría: M 45 %, L 28 %, S 17 %, XL 10 %. |
| ¿Vale la pena la suscripción? | Comparación real entre suscritos y no suscritos. |
| ¿Quién es el cliente de alto valor? | Segmento Platino: 25 % de los clientes aporta 65 % del gasto. |
| ¿Qué productos tienen peor satisfacción? | Ranking con margen de error, para no reaccionar a muestras pequeñas. |
| ¿Cuándo abastecer cada producto? | Temporada pico y valle por producto. |
| ¿Qué envío prefiere cada segmento? | Reparto de tipos de envío por valor, edad o género. |

## Por qué confiar en lo que muestra

Es lo que nos diferencia. Otros dashboards muestran gráficos; este **revisa primero la calidad de los datos**
y separa lo que sí se puede concluir de lo que no.

- **Detecta sesgos antes de decidir.** En el ejemplo, ninguna mujer de la base tuvo acceso a suscripción ni
  descuento. Un análisis sin esta revisión habría concluido algo equivocado.
- **Corrige por azar.** Cuando se prueban muchas combinaciones, algunas parecen significativas por casualidad.
  La herramienta lo corrige: en el ejemplo, una diferencia de monto por temporada pasa de p = 0.0098 a
  p = 0.276, y deja de ser una conclusión.
- **Dice cuándo no conviene decidir.** Si un producto tiene pocas ventas o hay empate, lo marca.

> En el ejemplo, un descuento no cambió el ticket promedio de forma significativa. Gastar margen en
> descuentos sin esta evidencia es dinero que se pierde.

## Qué se gana

- **Promociones con criterio:** se descuentan los productos que lo necesitan, no los que ya se venden.
- **Inventario por talla:** la curva de tallas reduce el stock que sobra y el que falta.
- **Retención enfocada:** el segmento de mayor valor se identifica con cifras, no con suposiciones.
- **Decisiones con respaldo:** cada recomendación viene con su evidencia y su límite.

## Lo que no hace, dicho con claridad

- No predice ventas futuras: el dataset no tiene fechas de compra.
- No mide el efecto de una promoción en el volumen: eso requiere datos antes y después.
- Los resultados de este ejemplo salen de un dataset público de compras de moda. **Con los datos reales de
  la tienda, las cifras cambian y el sistema se calibra con ellos.**

## Siguiente paso propuesto: piloto de cuatro semanas

1. **Semana 1:** conectar el historial de compras de la tienda con fechas y costos.
2. **Semana 2:** correr el análisis y validar la calidad de los datos con el equipo.
3. **Semana 3:** convertir las preguntas más urgentes en decisiones de promoción e inventario.
4. **Semana 4:** medir el resultado de las decisiones frente a la línea base.

---

# Parte 2 · Propuesta técnica

## Qué se entrega

- **Pipeline de datos:** un proceso que carga, valida y audita las compras en PostgreSQL.
- **API REST:** 12 endpoints protegidos, documentados en Swagger, con errores en un formato único.
- **Dashboard web:** una vista por pregunta de negocio, con gráficos y filtros.
- **Despliegue:** todo corre con Docker Compose, en un comando.

## Arquitectura

```
Datos ──► ETL ──► PostgreSQL ◄── API (FastAPI) ◄── Dashboard (Nuxt)
            │                    JWT · Swagger        SPA · nginx
            └── auditoría de calidad
```

- **Organizado por funcionalidad:** cada pregunta de negocio es una carpeta completa, así es fácil
  agregar, cambiar o quitar una.
- **Capas claras:** la ruta traduce la petición HTTP, el servicio decide, y la base solo guarda y agrega.
- **Lógica probada sin base de datos:** las reglas de recomendación se prueban como funciones puras.

## Seguridad

- Autenticación con JWT firmado; la aplicación no arranca sin una clave de al menos 32 caracteres.
- Límite de 10 intentos de login por minuto por IP.
- Una prueba automática falla si alguna ruta de la API queda sin protección.
- Errores sin detalles internos: el cliente recibe un código estable, no una traza de la base de datos.

## Calidad y operación

- **66 pruebas automáticas:** 8 del ETL, 40 del backend y 18 del frontend.
- **Integración continua:** lint de Ruff y pruebas de cada parte en cada cambio.
- **Logs con trazabilidad:** cada petición tiene un identificador y su duración.
- **Documentación técnica:** arquitectura, decisiones con su justificación y guía de operación.

## Integración y escalabilidad

- La API se integra con cualquier herramienta que consuma JSON; el contrato está en Swagger.
- Las consultas pesadas corren en la base de datos, que es donde escala un volumen grande.
- Pendiente para producción: caché compartida para el límite de login, cookie segura para la sesión y
  carga incremental cuando haya fechas.

## Demostración en vivo

1. Levantar todo con `docker compose up -d --build` y cargar los datos con `docker compose run --rm etl`.
2. Pedir un token en Swagger y consultar la recomendación de promoción para mujeres.
3. Abrir el dashboard y mostrar una pregunta de negocio.
4. Mostrar el hallazgo de calidad de severidad alta.

---

# Cierre

Hola Moda puede decidir promociones, inventario y retención con evidencia, y saber de antemano cuándo
sus datos no bastan para decidir. El siguiente paso es probarlo con sus propias compras.
