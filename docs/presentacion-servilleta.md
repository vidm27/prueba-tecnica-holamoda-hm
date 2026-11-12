# Tendencias de compra · Hola Moda

*Presentación en bocetos, basada en el método visual de Dan Roam en* The Back of the Napkin *(2008):
mirar, ver, imaginar y mostrar, con una sola idea por imagen.*

---

## 1 · MIRAR: qué tenemos

```
   3,900 compras ── 3,900 clientes ── 25 productos ── 50 estados
                    ✗ sin fechas de compra
```

Una compra por cliente, en 4 categorías de moda. Lo que no tenemos: el tiempo.

> Nota: empieza por lo que los datos permiten y lo que no. Eso fija el alcance antes de cualquier conclusión.

---

## 2 · VER: el valor está concentrado

```
  % del gasto
  100 ┤                              ┌──────
   65 ┤                  ┌───────────┘  Platino
   57 ┤  ┌───────────────┘               (25 % de clientes)
    0 ┴──┴────────────────────────────────────►
       20 % de clientes con más gasto
```

Platino, el 25 % de los clientes, aporta el **65 %** del gasto estimado.

> Nota: un solo dibujo, una sola idea. La curva 80/20 aparece aquí, con cifras reales del dataset.

---

## 3 · VER: lo que engaña

```
  Descuento y suscripción por género

  Hombres   ████████████████  63 % con descuento
  Mujeres   ░░░░░░░░░░░░░░░░   0 %   ← sesgo de origen
```

Ninguna mujer del dataset tiene suscripción ni descuento. Un análisis sin revisar esto concluye algo falso.

> Nota: el sesgo es un hallazgo de negocio, no solo un problema de datos.

---

## 4 · VER: lo que parece significativo, y no lo es

```
  p-valor (monto vs temporada)

  0.05 ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─
        ●  0.0098  sin corregir   ← parece significativo
        
        ●  0.276   corregido       ← no lo es
```

Probar 28 combinaciones produce falsos positivos. Corregir por ellas lo muestra.

> Nota: esta imagen justifica por qué el sistema no confía en cualquier p-valor.

---

## 5 · IMAGINAR: las seis preguntas del negocio

```
  ¿QUIÉN?    Clientes de alto valor (Platino)          → Retención enfocada
  ¿QUÉ?      Productos a promocionar                  → Promoción con criterio
  ¿CUÁNTO?   Ticket promedio y curva de tallas        → Inventario por talla
  ¿DÓNDE?    Producto líder por estado                → Distribución por región
  ¿CUÁNDO?   Temporada pico y valle                   → Abastecer a tiempo
  ¿CÓMO?     Qué envío prefiere cada segmento         → Oferta de envío
```

Las seis preguntas del método, aplicadas a la tienda. El ¿POR QUÉ? queda fuera: el dataset no trae causas.

> Nota: cada fila es una decisión concreta, no un gráfico. Así se responde "¿y entonces qué hacemos?".

---

## 6 · MOSTRAR: qué promocionar

```
 calificación
   alta │ PROMOCIÓN DE           │ MANTENER
        │ EXPOSICIÓN             │ (buen volumen,
        │ (bien calificado,      │  buena calificación)
        │  poco volumen)         │
   ─────┼────────────────────────┼──────────────────
   baja │ REVISAR PRODUCTO      │ RIESGO DE
        │ (poco volumen,         │ REPUTACIÓN
        │  mala calificación)    │ (mucho volumen,
        │                        │  mala calificación)
        └────────────────────────┴──────────────────►
                poco volumen        mucho volumen
```

La promoción va a los productos de arriba a la izquierda: bien calificados y con poco volumen. Descontar
un producto que ya se vende no suma nada.

> Nota: el cuadrante responde la pregunta con una imagen. El dato exacto está en la API.

---

## 7 · MOSTRAR: cuánto de cada talla

```
  Talla   Participación
  M       ████████████████████████████████████████████  45 %
  L       ███████████████████████████  28 %
  S       █████████████████  17 %
  XL      ██████████  10 %
```

Pedir inventario por talla es pedir esta proporción, no un número igual para todas.

> Nota: un solo gráfico de barras basta. Las cifras son del dataset y se recalibran con las de la tienda.

---

## 8 · MOSTRAR: qué puedes concluir y qué no

```
  SE PUEDE CONCLUIR          NO SE PUEDE CONCLUIR
  ─────────────────          ────────────────────
  Dónde está el valor        Tendencias en el tiempo
  Qué tallas comprar         Efecto de un descuento
  Qué productos promocionar  Recompra de clientes
```

El dataset no tiene fechas ni datos antes y después de una promoción. Decirlo es parte del producto.

> Nota: el límite es una respuesta, no una falta. Cierra la conversación sobre predicciones.

---

## 9 · MOSTRAR: el siguiente paso

```
  Semana 1 ─── conectar compras con fecha y costo
  Semana 2 ─── validar calidad de datos con el equipo
  Semana 3 ─── convertir preguntas en decisiones
  Semana 4 ─── medir resultados contra la línea base
```

Un piloto de cuatro semanas con las compras reales de la tienda.

---

*Inspiración: Dan Roam, The Back of the Napkin (2008). Las cifras provienen del dataset público
Customer Shopping Trends de Kaggle; los bocetos son ilustrativos.*
