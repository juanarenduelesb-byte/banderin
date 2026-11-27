# 02 · Arquitectura

**Todo vive en el repositorio `juanarenduelesb-byte/banderin` (público, licencia en `LICENSE`).**

## Actualización de torneos
- `.github/workflows/actualizar.yml` → `pipeline/update.sh`: descarga fuentes → `build.py` (normaliza, ubica, fusiona duplicados)
  → `check.py` (enlaces) → `emit.py` (escribe `site/data.js` y `site/pasados.js`) → `validate.mjs` (no publica si algo no cuadra)
  → `seo.py` (páginas por comunidad y provincia, `/en/`, sitemap) → `calendarios.py` (`site/cal/*.ics`) → `avisos.py` (correos).
- Horario: 6:20, 13:20 y 20:20 (Madrid, invierno). Lo dispara el worker de Cloudflare `banderin-programador` (`workers/programador`),
  con GitHub de respaldo. El trabajo «decidir» evita actualizar dos veces la misma franja.
- Si la validación falla, la web se queda con los datos anteriores y GitHub avisa por correo.

## Web
- `site/`: estática (HTML, CSS, JS sin framework), publicada por Cloudflare Pages desde `main` en 1–2 min.
- `site/app.js` (lista, fichas, filtros, perfil y «encaja contigo»), `mapa.js`, `i18n.js` (inglés), `legal.js`, `cuenta.js`, `social/`.
- Versionado de recursos con `seo.versionar()`.

## Avisos por correo
- API en Cloudflare Pages Functions (`functions/api/avisos/*`, `lib/avisos.js`): alta con doble confirmación, bajas de 1 clic.
- Base de datos D1 `banderin` (id `8667c8ff-3788-4f70-8a62-ba53a5ea31ad`): tablas `suscriptores`, `seguimientos`, `enviados`, `limites`, `seguridad`.
- `pipeline/avisos.py`: como mucho un correo al día por persona, compara con los torneos del último aviso, envía con Brevo desde avisos@banderin.es.
- Seguir: provincias, clubes y torneos. Perfil opcional (sexo, año, hándicap, federación, clubes) para filtrar lo que encaja.

## Cuentas y Banderín Social
- Supabase (`jdyawzbvxucamibbqdzg`), clave pública en `site/cuenta-config.js`; los datos los protege RLS.
  Tablas: `perfiles`, `avatares`, `social_*`. La clave de administrador nunca se usa desde agentes.

## Seguridad y copias
- `vigilancia.yml` (diaria): cabeceras, HTTPS, archivos privados, CSRF, actividad sospechosa.
- `copia.yml` (semanal): copia cifrada de D1 y Supabase.

## Correo
- avisos@banderin.es reenvía a juanarenduelesb@gmail.com (Cloudflare Email Routing). En Gmail llevan la etiqueta «Banderín» (filtro creado el 26/11).
- Contacto público de la web: juanarenduelesb@gmail.com.

## Motor de reels
- `marketing/reels/`: páginas HTML animadas + `build.py` (voz, música sintetizada, subtítulos, render con Playwright y ffmpeg). Ver su README.
