# Decisiones técnicas

Este documento explica las decisiones principales de la solución: qué elegí, por qué, qué descarté y qué
costo acepto. Empieza por el frontend, porque ahí se nota primero la experiencia del usuario.

---

## Frontend

### 1. TanStack Query para los datos del servidor

Cada pregunta de negocio pide datos a la API, a veces con filtros, y el usuario cambia esos filtros
todo el tiempo. Quería que la interfaz respondiera al instante, sin pantallas en blanco innecesarias y sin
repetir peticiones que ya hice.

TanStack Query resuelve eso con una caché por clave. La clave incluye los filtros, así que volver a una
combinación ya consultada muestra los datos de inmediato. Además entrega los estados de carga y error que
la interfaz necesita, y reintenta de forma automática solo los errores de servidor, porque un error 4xx
viene del cliente y repetirlo no lo arregla.

Los datos se consideran frescos durante 60 segundos. Eso tiene sentido porque el dataset cambia solo
cuando se corre el ETL, así que pedirlo de nuevo a cada momento sería trabajo sin valor.

### 2. Nuxt en modo SPA

La aplicación está detrás de un login, así que no hay contenido público que un buscador deba leer. Por eso
Nuxt funciona en modo SPA (`ssr: false`): el servidor entrega archivos estáticos y el navegador hace el
resto.

Con renderizado en servidor habría que resolver la hidratación y el manejo del token en dos lugares.
Aquí no aporta nada, así que lo evité.


### 4. Token en `sessionStorage`

El token de acceso vive en memoria y en `sessionStorage`, que se borra al cerrar la pestaña. Un middleware
manda a la pantalla de login si no hay token, y si la API responde 401, la sesión se cierra sola.

Es la opción más simple que cumple el objetivo sin tocar la API: no hay cookies que configurar ni
protección contra CSRF que mantener.

**Costo.** `sessionStorage` puede leerse desde JavaScript, así que un ataque XSS podría robar el token.
La mejora natural es una cookie `HttpOnly` emitida por la API. Lo dejo anotado como mejora.

### 5. Chart.js para las gráficas

Las preguntas de negocio necesitan barras, dona y líneas. Chart.js cubre esos casos con poco código y se
integra bien con Vue. Para el mapa de estados no usé una librería de mapas: una cuadrícula propia en SVG
es más clara para este caso y no depende de geometrías externas.

---

## Backend

### 6. FastAPI

FastAPI genera la documentación OpenAPI y Swagger a partir del código, con validación de tipos incluida.
La documentación no se mantiene aparte, así que no se desfasa. Flask o Django REST habrían requerido más
piezas para lograr lo mismo.

### 7. ORM en vez de SQL escrito a mano

Las consultas son agregaciones: agrupar, promediar, rankear y calcular percentiles. Con SQL textual,
las rutas se llenaron de cadenas difíciles de leer y de cambiar. Con SQLAlchemy y SQLModel, cada análisis
se lee como lo que es: qué agrupo, qué filtro y qué agrego.

Las agregaciones siguen ejecutándose en la base de datos. La lógica de clasificación, como la
recomendación de promoción o el líder por estado, vive en Python porque así se puede probar sin base de
datos.

**Costo.** Los modelos de lectura del backend describen las mismas tablas que escribe el ETL. Son dos
definiciones del mismo esquema, porque cada contenedor se construye por separado. Si una tabla cambia,
hay que actualizar los dos archivos.

### 8. Una carpeta por pregunta de negocio

Organicé el código por funcionalidad y no por capa técnica. Cada pregunta de negocio tiene su carpeta con
rutas, dependencias, servicio, esquemas y pruebas. El frontend sigue el mismo criterio.

La estructura dice qué hace el sistema, no cómo está hecho. Si una pregunta se elimina, se borra una
carpeta y nada más. Hay algo de repetición entre carpetas, y lo acepto a cambio de bajo acoplamiento: lo
común solo sube al núcleo cuando lo usan varias funcionalidades.

### 9. Rutas sin lógica y servicios sin HTTP

Cada funcionalidad tiene tres piezas: la ruta traduce la petición HTTP, el servicio decide y consulta, y
una dependencia construye el servicio con su sesión de base de datos. La ruta recibe el servicio por
inyección.

Así puedo probar `recomendar` o `calcular_top_por_estado` directamente, sin levantar un servidor, y puedo
sustituir un servicio completo en una prueba de ruta.

### 10. Errores con un solo formato, decididos en el servicio

Al principio cada ruta respondía los errores a su manera, y el frontend tenía que adivinar qué había
pasado. Ahora el servicio lanza un error que conoce su estatus HTTP y un código estable, como
`datos_insuficientes`. Un solo manejador lo convierte en:

```json
{"error": {"codigo": "datos_insuficientes", "estatus": 422, "mensaje": "…"}}
```

Quien sabe que "no hay variación suficiente" es un error de datos es el servicio, no la ruta. Dejar el
mapeo en un solo lugar evita que dos endpoints respondan distinto al mismo problema.

**Costo.** El campo `detail` de FastAPI desapareció, y el frontend se adaptó. Es un cambio que hay que
anunciar a cualquiera que consuma la API.

### 11. Autenticación aplicada una sola vez

Si cada ruta declara su propia protección, una ruta nueva puede quedar desprotegida sin que nadie lo
note. Por eso todas las rutas cuelgan de un router central protegido, y el login es lo único que vive en
el router público. Una prueba falla si alguna ruta bajo `/api/v1` queda sin token.

La seguridad por defecto es más fácil de mantener que la seguridad que hay que recordar. Quien agrega una
ruta tiene que esforzarse para hacerla pública, no para protegerla.

### 12. JWT con HS256 y un usuario en `.env`

Los tokens se firman con una clave simétrica de al menos 32 caracteres y vencen a los 60 minutos. La
aplicación no arranca sin una clave válida.

Hay un solo emisor y un solo verificador, así que una firma asimétrica no aporta nada aquí y agrega una
clave más que cuidar. El usuario administrador vive en `.env`. Con más personas haría falta una tabla de
usuarios con hash de contraseñas, pero lo dejé fuera porque el alcance pedía un acceso, no un sistema de
cuentas.

**Costo.** Si el token se filtra, sirve hasta que venza. Por eso el tiempo de vida es corto y el frontend
cierra la sesión cuando recibe un 401.

### 13. Límite de intentos de login con slowapi

El login es la puerta de entrada, y sin límite es vulnerable a fuerza bruta. Permito 10 intentos por minuto
por IP; al superarlo, la API responde 429 con la cabecera `Retry-After`.

Primero escribí un limitador propio y después lo cambié por slowapi. Escribir infraestructura de seguridad
a mano tiene más riesgo que usar una librería conocida.

**Costo.** El conteo es por IP y cuenta todas las peticiones, no solo las fallidas. Con varias réplicas,
cada una tendría sus propios contadores; la solución sería Redis, que dejé anotada.

### 14. Logs con contexto por petición

Cuando algo falla, quiero seguir una petición de principio a fin. Usé loguru como único logger. Recibe
también los logs de uvicorn, SQLAlchemy y slowapi, así que todo sale con el mismo formato.

Cada petición tiene un `request_id`, que acepta el de la cabecera `X-Request-ID` o genera uno nuevo, y se
registra con su estatus y su duración.

Desactivé `diagnose`, la opción de loguru que muestra variables locales en los tracebacks. En el login hay
claves en memoria, y prefiero un traceback menos detallado a una clave escrita en un archivo de log.

---

## Datos y ETL

### 15. Un dataset sintético, y lo digo en la solución

El CSV no trae fecha de compra, y al explorarlo encontré señales de que los datos son sintéticos:
distribuciones casi perfectamente uniformes, ninguna mujer con suscripción o descuento, y una columna de
descuento idéntica a la de código promocional.

En vez de esconder eso, el ETL audita el conjunto y guarda ocho hallazgos con su severidad y su evidencia.
La API los expone en `/calidad/auditoria`, y el frontend los muestra antes de cualquier conclusión.
Un análisis que presenta conclusiones sobre datos que no entiende no le sirve a nadie; si la solución lo
señala desde el principio, la conversación con el negocio empieza en el lugar correcto.

### 16. Validación en dos niveles

Hay errores que se ven fila por fila, como un monto negativo o un Yes/No inválido, y otros que solo se
ven mirando el conjunto, como que ningún cliente de un género tenga beneficios.

Pydantic valida cada fila y registra las que rechaza con su número de línea. Después, ocho reglas
revisan el conjunto completo. Son preguntas distintas, y no se responden con la misma herramienta.

### 17. Segmentar por valor, no con K-means

Quería segmentar a los clientes, y K-means es la respuesta que todos esperan. Al medir la dispersión de
las variables, solo el gasto tenía variación real. K-means sobre variables uniformes habría producido
grupos que parecen significativos y no lo son.

Por eso el gasto anual estimado se divide en cuartiles: Bronce, Plata, Oro y Platino. Un cuartil se
explica en una frase, y el negocio entiende "Platino" sin leer un gráfico de codos.

El resultado lo justifica: el 25 % de los clientes de Platino aporta el 65 % del gasto estimado, y el 20 %
superior de clientes aporta el 57 %.

### 18. Corrección por comparaciones múltiples

Si pruebo 28 combinaciones de métrica y variable, algunas saldrán significativas por azar. Eso pasó en el
análisis: monto contra temporada tenía p = 0.0098, pero ajustado queda en 0.276, así que no es
significativo.

Uso Kruskal-Wallis, que no exige distribución normal, con corrección de Bonferroni sobre las 28 pruebas.
El laboratorio de hipótesis existe para enseñar a no creer en cualquier p-valor; si la herramienta se
equivocara en eso, perdería toda credibilidad.

**Costo.** Bonferroni es conservador y puede ocultar efectos reales pequeños. Prefiero ese error al
contrario, porque aquí un falso positivo lleva a una decisión de negocio equivocada.

### 19. ETL bajo demanda con recarga completa

El ETL es un script de Python que corre como servicio de un solo uso: `docker compose run --rm etl`. No
usé Airflow, Spark ni dbt, porque resuelven problemas que aquí no existen: volumen, programación y
dependencias entre cientos de tareas. Un script bien estructurado es más fácil de leer y de defender.

Cada corrida recrea el esquema y carga todo dentro de una sola transacción. Si algo falla, la base queda
como estaba, y correrlo dos veces da el mismo resultado.

**Costo.** Con más datos o con carga incremental, esta forma tendría que cambiar. Lo dejo anotado como
mejora.

---

## Infraestructura

### 20. Monorepo con Docker Compose

Un solo repositorio contiene `backend/`, `frontend/`, `etl/`, `datos/` y el `docker-compose.yml`. Quien
revisa la prueba clona una vez y levanta todo con un comando, sin instalar Python ni Node.

Los cambios que atraviesan capas, como un formato de error que cambia en el backend y en el frontend, viajan
en un mismo PR. Tres repositorios separados habrían sido más fáciles de escalar en un equipo grande, pero
aquí agregan fricción sin beneficio.

El frontend corre en el puerto 3001 porque el 3000 estaba ocupado por otro proyecto local. El README lo
explica.

---

## Lo que dejé fuera a propósito

- **Tendencias en el tiempo y recompra.** El dataset no tiene fechas.
- **Redis para el límite de login.** Con una sola instancia, los contadores en memoria bastan.
- **Un orquestador para el ETL.** Sería sobreingeniería para este volumen.
- **Una tabla de usuarios.** Se pidió un acceso, no un sistema de cuentas.

## Mejoras con más tiempo

1. Cookie `HttpOnly` para el token.
2. Redis para el límite de login con varias réplicas.
3. Refrescar los datos al volver a la pestaña, si el dataset se actualizara en vivo.
4. Carga incremental en el ETL, con fechas en el dataset.
5. Usuarios por persona, con roles y hash de contraseñas.
