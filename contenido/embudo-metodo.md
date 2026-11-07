# MĒTODO · Embudo completo: Trial Reels → newsletter → Hotmart → upsells

Fecha: 7 de noviembre de 2026.
Relacionado: `contenido/landing-metodo.md` (auditoría y copy), `contenido/landing-waiting-list-curso.md`, `contenido/vsl-waiting-list-curso.md`.

**Decisiones de Atenea (7-nov):**
- El producto es un **curso grabado (4 módulos) + sesiones en vivo**, vendido en **Hotmart**.
- La landing es **newsletter + lista de espera**. El newsletter se llama *Notas de MĒTODO* (nombre propuesto, se puede cambiar).
- El tráfico llega de **Trial Reels** con **palabra clave en comentarios → link por DM**.
- **Todavía no hay plataforma de newsletter.** Los registros se guardan en la base de datos del proyecto de Lovable hasta elegir una.
- Después de la venta: **upsells al estilo Hormozi**.

---

## 1. El flujo

```
Trial Reel (solo lo ven no seguidores)
   │  "Comenta METODO y te mando…"
   ▼
DM automático con link (con UTM por reel)
   ▼
Landing: VSL + suscripción (nombre, email, WhatsApp opcional)
   ▼
Notas de MĒTODO (1 por semana) ── mantiene la confianza y genera prueba
   ▼
Lanzamiento: la lista entra 24–48 h antes y con precio de fundador
   ▼
Checkout Hotmart ($2,600 MXN) + order bump
   ▼
Upsell justo después de la compra → downsell si dice que no
   ▼
Continuidad (mensual) para quien quiere seguimiento
```

---

## 2. Trial Reels → DM → landing

- **Configura la palabra clave antes de publicar.** Quien comenta en un Trial Reel no te conoce. Si el DM no sale en automático, lo pierdes.
- **Palabra clave: `IA`** (decisión de Atenea, 7-nov). Como es muy corta, la regla debe ser **"el comentario es exactamente IA"** (no "contiene"), o se dispara con "gracIAs", "materIA", etc. Agregar variantes: `ia`, `Ia`, `IA!`, `IA 🙌`.
- **Herramienta:** ManyChat u otra automatización de DMs de Instagram.
- **Mensaje del DM** (corto, un solo link):
  > ¡Hola! Aquí está 👉 [link]. Es mi newsletter gratis: cada semana te mando lo que estoy haciendo con IA en anuncios de Meta, con una marca real. Y cuando abra el curso, te enteras primero.
- **Link con UTM, uno por reel**, para saber cuál trae suscriptores:
  `https://registro.ateneakurevelis.com/?utm_source=instagram&utm_medium=trial_reel&utm_campaign=lista_metodo&utm_content=reel01`
  Cambia `reel01` por un nombre corto de cada video (`reel_segmentacion`, `reel_creativos`…). La landing guarda estos datos en cada registro.
- **Recordatorio opcional en el DM** a las 24 h si no dio clic (si la herramienta lo permite).
- **Métrica por reel:** comentarios → clics al link → suscriptores (columna `utm_content` en tu panel o CSV).

---

## 3. Plataforma de newsletter (pendiente)

Mientras tanto, los registros viven en la base de datos de Lovable (panel `/admin` + exportación a CSV, con columnas de UTM, referrer y la respuesta de "qué te frustra"). Para elegir:

| Opción | A favor | En contra |
|---|---|---|
| **Kit (ConvertKit)** | Hecha para creadores que venden cursos; etiquetas y automatizaciones fáciles | El plan gratis es limitado en automatizaciones (revisar el plan actual) |
| **MailerLite** | Plan gratis con automatizaciones, barato al crecer | Menos enfocada en creadores |
| **Beehiiv** | Muy buena para newsletter de contenido, con crecimiento y referidos | Más débil para secuencias de venta |

**Recomendación:** Kit o MailerLite, porque vas a necesitar **secuencias de lanzamiento y etiquetas** ("compró" / "no compró"), no solo un newsletter.

**Antes de enviar el primer correo:**
- Envía desde **tu dominio** (ej. `notas@[tu-dominio]`), no desde Gmail. Si no, termina en spam.
- Importa el CSV de Lovable o conecta el formulario con Zapier o un webhook. Lo dejo listo cuando elijas.
- Agrega un **aviso de privacidad** a la landing (se piden datos personales en México). Está pendiente.

⚠️ La confirmación de la landing dice *"Tu primer Notas de MĒTODO te llega esta semana"*. Con suscriptores, **hay que mandar el primero esa misma semana** (aunque sea a mano, desde el CSV), o cambiar el texto.

---

## 4. Notas de MĒTODO: qué mandar cada semana

**Formato:** 1 correo por semana, 1 idea, 300–500 palabras, mismo día y hora. Termina con **una pregunta para que respondan**: las respuestas mejoran la entrega y te dan contenido.

**4 pilares, en rotación:**
1. **Diario de la marca real** (tu mejor activo). Qué hiciste esta semana, qué números salieron, qué cambiaste. Es prueba en tiempo real y crea serie: quieren saber cómo sigue.
2. **El prompt o plantilla de la semana.** Algo que puedan usar hoy (sale de tus grabaciones de pantalla).
3. **El mito de la semana.** Como "no es la segmentación": una creencia equivocada + lo que sí funciona.
4. **Respondo tu pregunta.** Sale de las respuestas a "¿Qué te frustra de tus anuncios?" que guarda la landing.

**Primer correo (bienvenida):** quién eres en 3 líneas, qué van a recibir y cuándo, el caso de la marca real en una frase, y la pregunta *"¿qué es lo que más te frustra hoy de tus anuncios?"*.

**Reutiliza:** cada correo puede salir de un reel y volver a convertirse en reel. El newsletter es la versión larga.

---

## 5. Secuencia de lanzamiento (cuando el curso esté en Hotmart)

| Día | Correo | Objetivo |
|---|---|---|
| L-7 | "El curso abre el [fecha]" | Fecha + qué incluye + recordar el precio de fundador |
| L-3 | Caso de la marca real con números | Prueba |
| L-1 | "Mañana abre, primero para ti" | Expectativa + objeciones (FAQ) |
| **L-0** | **Abre solo para la lista** (link de Hotmart) | Ventas de la lista caliente |
| L+1 | Recordatorio + respuestas a dudas reales | Objeciones |
| L+2 | Apertura pública (redes) + último aviso a la lista | Ventas |
| Cierre | "Hoy termina el precio de fundador" (fecha real) | Urgencia real |

- Después del cierre, quien no compró sigue en el newsletter. Etiquétalo como "no compró" para la siguiente apertura.
- **Urgencia y cupos solo si son reales:** fecha de cierre del precio de fundador y cupos de las sesiones en vivo si de verdad tienen límite.

---

## 6. Modelo de dinero al estilo Hormozi (*$100M Money Models*, 2025)

Hormozi divide un modelo de dinero en **4 tipos de oferta**:
- **Atracción:** lo que trae al cliente.
- **Upsell:** más valor justo después de comprar.
- **Downsell:** recupera a quien dijo que no.
- **Continuidad:** ingreso recurrente.

Dos de sus ideas aplican directo aquí:
- **Los upsells suelen generar la mayor parte de la ganancia.** El mejor momento para ofrecer es **justo después de la compra**.
- **Menu upsell:** en lugar de preguntar "¿sí o no?", dar a elegir entre A y B.

Su meta es que lo que deja un cliente nuevo **pague el costo de conseguirlo en los primeros 30 días**. Esto importa cuando metas pauta.

**Aplicado a MĒTODO** (precios entre [ ] por definir):

| Pieza | Qué es | Ejemplo para MĒTODO | En Hotmart |
|---|---|---|---|
| **Atracción** | El curso | 4 módulos grabados + sesiones en vivo, **$2,600 MXN** fundador | Producto principal |
| **Order bump** | Extra barato en el mismo checkout, con un clic | "Pack de 50 prompts + plantillas de creativos por industria", [$300–500 MXN] | **Order Bump** (se configura en el panel; tiene que ser un producto digital, no un servicio en vivo) |
| **Upsell** (justo después de pagar) | El siguiente problema que crea el curso: "ya tengo campañas, ¿quién me dice si van bien?" | **Menú A/B:** A) Revisión 1:1 de tu cuenta (60 min) [$X] · B) Implementación en grupo de 4 semanas, armamos las campañas juntas [$Y] | Revisa en tu cuenta si existe upsell de un clic después del pago. Si no, ponlo en la página de gracias o en el primer correo después de la compra |
| **Downsell** | Para quien dice que no al upsell | Mismo upsell en **parcialidades**, o versión reducida (revisión grabada de 20 min) | Pago en parcialidades / producto aparte |
| **Continuidad** | Ingreso mensual | "MĒTODO Club": revisión mensual en vivo + el agente de revisión + comunidad, [$X/mes] | Suscripción |
| **High ticket** (después) | Que lo hagas tú por ellos | Gestión de campañas hecha por ti para negocios de alumnas que quieren delegar | Fuera de Hotmart (llamada) |

**Orden práctico:** lanza primero **curso + order bump**, que es simple y sube el ticket desde la primera venta. Agrega el **upsell de revisión 1:1** cuando tengas las primeras 10–20 alumnas y sepas qué piden. La **continuidad** va cuando veas que se repite la pregunta "¿y después qué?".

---

## 7. Qué medir

| Etapa | Métrica | Dónde |
|---|---|---|
| Reel | Comentarios con la palabra clave | Instagram / herramienta de DMs |
| DM → landing | Clics al link | Herramienta de DMs |
| Landing → suscriptor | % de visitas que se suscriben (por `utm_content`) | Panel de Lovable / CSV |
| Newsletter | Apertura, clics y **respuestas** | Plataforma de email |
| Lista → compra | % de la lista que compra en el lanzamiento | Hotmart |
| Ticket promedio | % que toma el order bump y el upsell | Hotmart |

---

## 8. Pendientes de Atenea

1. Elegir plataforma de newsletter y dominio de envío.
2. Configurar la palabra clave `IA` y el DM **antes** de publicar los Trial Reels (pasos en `contenido/manychat-palabra-ia.md`).
3. Pegar la URL del VSL en `VSL_VIDEO_URL` (`src/lib/workshop-video.ts` del proyecto de Lovable, o pedírselo al agente) cuando esté listo. Acepta YouTube, Vimeo, Bunny o un .mp4. Mientras esté vacío, la sección no se muestra.
4. Publicar la landing en Lovable: los cambios del 7-nov están en la vista previa; `registro.ateneakurevelis.com` sigue mostrando la versión anterior hasta publicar.
5. Aviso de privacidad.
6. Escribir y mandar el primer *Notas de MĒTODO* la semana en que llegan los primeros suscriptores.
7. Confirmar el precio en Hotmart ($2,600 MXN fundador, ¿y el precio normal?), la fecha de apertura y si las sesiones en vivo tienen cupo.
8. Definir el order bump.

---

## Fuentes
- Resumen de *$100M Money Models* (4 tipos de oferta): https://www.supersummary.com/100m-money-models/summary/
- Hormozi, Parte 5 "Upsell Offers" (audiolibro, ep. 942): https://www.shortform.com/podcast/episode/the-game-w-alex-hormozi-2025-08-19-episode-summary-part-5-upsell-offers-100m-money-models-audiobook-ep-942
- Notas sobre *$100M Money Models* (menu upsell, recuperar el costo en 30 días): https://www.maxmednik.com/blog/notes-on-100m-money-models-by-alex-hormozi
- Hotmart, ¿Qué es y cómo configurar el Order Bump?: https://help.hotmart.com/es/article/360019967392/-que-es-y-como-configurar-el-order-bump-
- Hotmart, herramienta Order Bump (MX): https://hotmart.com/mx/herramientas/order-bump
- TechCrunch, Instagram lanza Trial Reels: https://techcrunch.com/2024/12/10/instagram-rolls-out-trial-reels-that-arent-shown-to-a-creators-followers
- InstantDM, How Instagram Trial Reels Work: https://instantdm.com/blog/how-instagram-trial-reels-work
