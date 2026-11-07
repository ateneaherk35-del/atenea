# Palabra clave "IA" · bot mIA (Instagram)

Actualizado: 7 de noviembre de 2026.
La automatización **no usa ManyChat**: corre en el bot propio de Atenea, **mIA** (proyecto de Lovable "Insta Engagement Buddy", tabla `keywords`), conectado a @metodomkthouse y @ateneaherk.

## Estado (7-nov)
- Palabra `ia` **activa**. Alias: `ai`, `IA`, `i.a`, `ia!`.
- `match_in_phrase = true`: responde si "ia" aparece como **palabra completa** en el comentario ("IA", "quiero la IA", "IA 🙌"). No se activa con "gracias" o "materia" porque compara palabra por palabra, después de quitar mayúsculas, acentos y signos.
- Bot encendido (`agent_settings.bot_enabled = true`). Recibe eventos de Instagram hasta hoy.

## Textos
**Respuesta pública (rota entre):** "va, te mandé la liga por dm 👀" · "listo, revisa tus mensajes 🙌" · "te acabo de mandar el video por dm ✨" · "ya te escribí (:"

**DM:**
> va, aquí está 👇
> https://registro.ateneakurevelis.com/?utm_source=instagram&utm_medium=dm&utm_campaign=lista_metodo&utm_content=ia
>
> es el video donde Ate enseña cómo le enseñó a la IA a hacer sus anuncios de Meta, con los archivos reales. si te apuntas (es gratis), cada semana te llegan sus notas y entras primero cuando abra el curso.

**Seguimiento** (una sola vez, ~23 h después, si no contestó):
> oye, ¿alcanzaste a ver el video? la lista entra primero cuando abra el curso de Ate. y si no es tu momento, todo bien 🙌

**Texto anterior (reemplazado):** hablaba del "taller en vivo a 15 personas" y de aviso por WhatsApp.

## Pendiente
- La landing debe estar **publicada** con la v2 para que el link lleve a la versión nueva.
- Probar desde otra cuenta: comentar "IA" en un reel y revisar que lleguen la respuesta pública y el DM.
- Medición: `/admin` de la landing, columna `utm_content = ia`.
