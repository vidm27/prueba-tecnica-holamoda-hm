# Tendencias de compra · Hola Moda

**Presentación técnica · Prueba para Analista de Desarrollo e Integración**

Pipeline de datos de punta a punta: un CSV de compras se carga con un ETL, una API lo expone con
autenticación y un dashboard lo visualiza. Duración sugerida: 20 minutos + demo de 5 + preguntas.

---

## 1. Qué construí

- **ETL** en Python (pandas, Pydantic, SQLModel) que carga 3,900 compras a PostgreSQL.
- **API** en FastAPI con JWT, 12 endpoints, documentación en Swagger y errores con un formato único.
- **Dashboard** en Nuxt 4 con una vista por cada pregunta de negocio.
- **Todo en Docker Compose**: `docker compose up` levanta la base, la API y el frontend.

> Empieza con el resultado: en una frase, qué puede hacer el negocio con esto que no podía hacer antes.

---

## 2. Las preguntas de negocio

1. ¿De qué producto lanzar una promoción o descuento?
2. ¿Qué producto se mueve más por estado, y en qué talla y color?
3. ¿Qué curva de tallas comprar por categoría?
4. ¿Vale la pena la suscripción?
5. ¿Quién es el cliente de alto valor?
6. ¿Qué productos tienen peor satisfacción?
7. ¿Cuándo abastecer cada producto?
8. ¿Qué tipo de envío prefiere cada segmento?

> Cada pregunta es un endpoint y una vista. Si el dato no alcanza para responder, el sistema lo dice.

---

## 3. Lo que encontré en los datos

- **No hay fechas de compra.** No puedo hablar de tendencias en el tiempo ni de recompra.
- **Los datos parecen sintéticos.** Edad, monto y calificación siguen distribuciones casi uniformes.
- **Hay sesgos de origen.** Ninguna de las 1,248 mujeres del dataset tiene suscripción ni descuento.
- **Casi no hay señal.** Monto y calificación no cambian de forma significativa con casi ninguna variable.

> Esto cambió el proyecto: en lugar de un dashboard de gráficos bonitos, el sistema audita los datos y
> separa lo que sí se puede concluir de lo que no.

---

## 4. Arquitectura

```
Kaggle CSV ──► ETL ──► PostgreSQL ◄── API FastAPI ◄── Frontend Nuxt
                                        (JWT)           (SPA, nginx)
```

- **Backend:** una carpeta por pregunta de negocio, con rutas, dependencias, servicio y esquemas.
- **Capas:** la ruta traduce HTTP; el servicio decide y consulta; el núcleo es lo transversal.
- **Documentación completa** en `ARCHITECTURE.md`, con diagramas de Mermaid.

> Si preguntan por qué esta estructura: la carpeta dice qué hace el sistema, no cómo está hecho.

---

## 5. El ETL

1. **Extraer** el CSV sin transformarlo.
2. **Validar** cada fila con Pydantic: tipos, rangos y booleanos Yes/No.
3. **Enriquecer**: grupo de edad, compras al año, gasto anual y nivel de valor por cuartil.
4. **Separar** en tres tablas: clientes, productos y compras.
5. **Auditar** el conjunto con 8 reglas de calidad.
6. **Cargar** todo en una transacción: si algo falla, la base queda como estaba.

> Resultado: 3,900 clientes, 25 productos, 3,900 compras y 8 hallazgos de calidad.

---

## 6. Hallazgos que cambian la conversación

- **Platino** (25 % de los clientes) aporta **65 %** del gasto estimado.
- El 20 % de clientes con más gasto aporta el **57 %**.
- Ninguna mujer recibió descuento: el segmento sin beneficios es un tema de negocio, no solo de datos.
- Monto contra temporada tenía **p = 0.0098**. Al corregir por las 28 pruebas posibles queda en **0.276**:
  no es significativo. Es el ejemplo de por qué no creer en cualquier p-valor.

---

## 7. Seguridad y calidad

- **Autenticación:** JWT firmado, usuario en `.env`, y una prueba que falla si una ruta queda sin token.
- **Límite de login:** 10 intentos por minuto por IP, con `Retry-After`.
- **Errores:** un solo formato, con código estable y estatus HTTP.
- **Logs:** loguru con `request_id` por petición.
- **Tests:** 8 del ETL, 40 del backend y 18 del frontend; ruff y ESLint en CI.

---

## 8. Desafíos y cómo los resolví

| Desafío | Solución |
|---|---|
| El dataset no trae fechas | Lo declaro como límite y lo muestro en la API y el dashboard |
| Datos sintéticos con sesgos | Una regla de auditoría los detecta y se muestran antes de cualquier conclusión |
| Casi no hay señal estadística | Corrección de Bonferroni y un veredicto explícito en el laboratorio de hipótesis |
| Mi primer diseño tenía SQL textual por todas partes | Refactoricé a SQLAlchemy ORM y capas: ruta, servicio y dependencias |
| Errores con formatos distintos por endpoint | Un manejador único; el servicio decide el estatus |
| La autenticación era endpoint por endpoint | Un router central protegido; una prueba verifica que ninguna ruta quede abierta |
| Un limitador propio para el login | Lo reemplacé por slowapi |
| Un cambio de formato rompió el frontend | Lo adapté en el mismo PR y lo documenté |
| Una fusión revirtió la documentación de Swagger | Restauré los commits sobre `main` y lo verifiqué con tests y el OpenAPI |
| Un puerto ocupado por otro proyecto | Usé el 3001 y lo explico en el README |

> Los desafíos más útiles para contar son los que cambiaron una decisión, no los que se arreglaron sin pensar.

---

## 9. Demostración

Guion en vivo, de unos 5 minutos:

1. **Levantar todo**
   ```bash
   cp .env.example .env          # ajustar JWT_SECRETO y ADMIN_CLAVE
   docker compose up -d --build
   docker compose run --rm etl   # carga los datos y muestra los conteos
   ```
2. **Swagger:** abrir `http://localhost:8000/docs`, mostrar la descripción, pulsar **Authorize** y
   hacer una petición a `/productos/promocion?genero=Female`.
3. **Dashboard:** abrir `http://localhost:3001`, entrar con las credenciales de `.env` y mostrar
   una pregunta de negocio con su gráfico.
4. **Calidad:** abrir `/calidad/auditoria` y señalar el hallazgo de severidad alta.
5. **Hipótesis:** consultar `/hipotesis?metrica=monto_usd&variable=temporada` y leer el veredicto.

> Plan B: si Docker falla, mostrar las respuestas guardadas y el dashboard ya abierto.

---

## 10. Mejoras con más tiempo

1. **Cookie `HttpOnly`** para el token, en lugar de `sessionStorage`.
2. **Redis** para el límite de login con varias réplicas.
3. **Refrescar datos** al volver a la pestaña, si el dataset se actualizara en vivo.
4. **Carga incremental** en el ETL, cuando haya fechas.
5. **Usuarios y roles**, con hash de contraseñas.
6. **e2e en CI:** las pruebas de Playwright ya existen, pero el CI no las corre todavía.

---

## 11. Cierre

- Construí un sistema que responde preguntas de negocio **y dice cuándo no debe responderlas**.
- Lo más valioso fue el diagnóstico de los datos, no la cantidad de gráficos.
- Todo corre con un comando, y las decisiones están documentadas con su justificación.

> Preguntas.
