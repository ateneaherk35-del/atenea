# Palabra clave "IA" · Automatización de comentarios → DM

Fecha: 7 de noviembre de 2026. Herramienta sugerida: ManyChat (conectado a la cuenta de Instagram de Atenea).
No hay conexión a Instagram ni a ManyChat desde la sesión de Claude: Atenea la activa en su cuenta con estos pasos. Los nombres de los menús pueden variar un poco según la versión de ManyChat.

## Antes de activar
- **Publicar la landing** en Lovable. Si no, el link lleva a la versión vieja de `registro.ateneakurevelis.com`.
- Instagram debe ser cuenta **profesional** (creador o empresa) y estar conectada a ManyChat.
- En Instagram: Configuración → Mensajes → Herramientas conectadas → **"Permitir acceso a los mensajes"** activado.

## Configuración en ManyChat
1. **Automatizaciones → Nueva automatización → Empezar desde cero.**
2. **Disparador:** "El usuario comenta tu publicación o reel".
   - Para Trial Reels: elige **"Cualquier publicación o reel"** (o selecciona cada reel después de publicarlo).
   - **Palabras clave:** `IA`, `ia`, `Ia`.
   - Coincidencia: **"es exactamente"** / "is", **no** "contiene". Con "contiene", "IA" se activa con "gracIAs", "materIA", "famIlIA"...
3. **Respuesta pública al comentario** (activar y poner 3–4 variantes, para que Instagram no lo vea como spam):
   - "¡Te lo mandé por DM! 💌"
   - "Listo, revisa tus mensajes 👀"
   - "Ya te escribí 🙌"
   - "Te llegó por DM ✨"
4. **Mensaje directo 1 (apertura, con botón):**
   > ¡Hola! 👋 Gracias por comentar. Te mando cómo le enseñé a la IA a hacer mis anuncios de Meta (y cómo hacerlo con los tuyos). ¿Te lo paso?
   - Botón: **"Sí, mándamelo"**
   (El botón hace que la persona responda. Eso abre la conversación y mejora la entrega de los siguientes mensajes.)
5. **Mensaje directo 2 (al tocar el botón):**
   > Aquí está 👉 [link]
   > Es mi newsletter gratis: cada semana te mando lo que estoy haciendo con IA en anuncios, con campañas reales. Y cuando abra el curso, la lista entra primero.
   - Botón con URL: **"Quiero entrar"** → link con UTM (abajo).
6. **Opcional:** recordatorio a las 23 h si no tocó el botón: "¿Todavía lo quieres? 👇" + mismo botón. Dentro de la ventana de 24 h de Meta.
7. **Activar** y probar desde otra cuenta: comentar "IA" en un reel y revisar que llegan la respuesta pública y los dos DMs, y que el link abre la landing.

## Link (uno por reel, para saber cuál trae suscriptores)
```
https://registro.ateneakurevelis.com/?utm_source=instagram&utm_medium=trial_reel&utm_campaign=lista_metodo&utm_content=NOMBRE_DEL_REEL
```
Cambiar `NOMBRE_DEL_REEL` por algo corto y sin espacios: `reel_segmentacion`, `reel_creativos`, `reel_vsl`... Si se usa una sola automatización para todos los reels, dejar `utm_content=ia_dm` y medir por fecha de publicación.

## En el reel
- Pantalla final y caption: **"Comenta IA y te mando cómo lo hago"**.
- Caption: la palabra en mayúsculas para que se vea clara.

## Qué medir
Comentarios con "IA" → clics en el botón → suscriptores en `/admin` (columna `utm_content`).
