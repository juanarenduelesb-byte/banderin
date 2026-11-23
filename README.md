# Banderín

Todos los torneos de golf de España en un solo sitio, revisados cada mañana. Un proyecto de Esclusa.

## Cómo está montado

- `site/`: la web. Es estática (HTML, CSS y JavaScript, sin servidor) y la publica Cloudflare Pages cada vez que cambia algo en la rama `main`.
- `pipeline/`: los scripts en Python que leen NextCaddy, Golf Directo, la RFEG y los calendarios de las federaciones, comprueban cada enlace y generan `site/data.js` (torneos próximos) y `site/pasados.js` (últimos 45 días, con resultados).
- `.github/workflows/actualizar.yml`: la actualización diaria. Cada mañana a las 6:45 (7:45 en verano) GitHub ejecuta los scripts, valida el resultado y, si todo está bien, guarda los datos nuevos. Cloudflare publica la web en uno o dos minutos.

## Qué pasa si algo falla

La validación (`pipeline/validate.mjs`) no deja publicar si faltan NextCaddy o Golf Directo, si hay menos del 60 % de torneos que el día anterior o si algún torneo está mal formado. En ese caso la web se queda con los datos del día anterior y GitHub te avisa por correo de que la ejecución ha fallado.

Para lanzarla a mano: pestaña **Actions** → **Actualizar torneos** → **Run workflow**.

## Configuración de Cloudflare Pages

- Framework preset: ninguno
- Build command: vacío
- Build output directory: `site`
- Rama de producción: `main`

## Antes de lanzar

- Rellenar los datos del titular en `site/legal.js` (bloque `TITULAR`).
- Conectar el dominio propio en Cloudflare Pages → Custom domains.

## Páginas para buscadores

`pipeline/seo.py` genera cada mañana, a partir de `site/data.js`, las páginas
`/torneos-golf/` (una por comunidad y por provincia, en HTML sin JavaScript),
la portada en inglés `/en/` (copia de `index.html`), el `sitemap.xml`, los
enlaces por comunidad del pie y la descripción de la portada.

Si cambias `site/index.html` a mano, ejecuta `python3 pipeline/seo.py` antes
de subir el cambio para que `/en/` quede igual.

## Perfil y calendarios (fase 1)

- El perfil de golfista y lo que sigue cada usuario se guardan solo en su
  navegador (`banderin.perfil`, `banderin.sigo`), con el mismo formato que
  tendrán las cuentas.
- `pipeline/cond.py` lee las condiciones de inscripción que publican las fuentes
  (hándicap máximo, edad, solo socios, solo federados). Ante la duda no extrae nada.
- `pipeline/calendarios.py` genera cada día `site/cal/{prov,ccaa,club}/*.ics`
  para suscribirse desde Apple, Google u Outlook.

## Avisos por correo (fase 2) - apagados hasta activarlos

Piezas:
- `functions/api/*` y `lib/avisos.js`: API en Cloudflare Pages Functions (alta con doble
  confirmación, confirmar, consultar, sincronizar lo que se sigue y baja). Mientras falte
  la configuración, `/api/estado` responde `{"avisos":false}`, el resto 503, y la web
  muestra «Próximamente».
- `db/schema.sql`: base de datos D1 (correo, idioma y lo que sigue cada persona).
- `pipeline/avisos.py`: lo ejecuta la actualización diaria; manda como mucho un correo
  al día por persona, sin repetir avisos, y limpia altas sin confirmar e inactivas.

Activar los avisos (requisitos: dominio propio, datos del titular en el aviso legal y
cuenta de Brevo con el dominio verificado):
1. Cloudflare → D1 → crear la base `banderin` (ubicación: Europa) y ejecutar `db/schema.sql`.
2. Pages → banderin → Settings → Bindings: D1 `DB` → `banderin`.
3. Pages → Settings → Variables: `AVISOS=on`, `AVISOS_FROM=avisos@<dominio>`; secretos
   `BREVO_API_KEY` y `LINK_SECRET` (cadena aleatoria larga).
4. GitHub → Settings → Secrets and variables → Actions: variables `AVISOS=on`,
   `SITE_URL`, `AVISOS_FROM`, `CF_ACCOUNT_ID`, `D1_DATABASE_ID`; secretos `BREVO_API_KEY`,
   `LINK_SECRET` (el mismo) y `CF_API_TOKEN` (permiso D1: Edit).
5. Volver a desplegar y probar el alta con un correo propio.

Pruebas en local: `wrangler pages dev site --d1 DB=local ...` con un Brevo simulado
(`BREVO_API_URL`); `D1_SQLITE=<ruta>` para `pipeline/avisos.py`.

## Que la actualización llegue a su hora

GitHub retrasa horas las tareas programadas (la de las 5:23 llegaba a las 12:37 o no llegaba).
El workflow lo intenta cada hora en dos ventanas (mañana y tarde, hora UTC) y el trabajo «decidir»
deja pasar solo la primera pasada de cada ventana que llegue; las demás acaban en segundos.
No hace falta ningún token extra: usa el GITHUB_TOKEN del propio workflow.

## Seguridad

- **API** (`functions/api/_middleware.js`): solo acepta escrituras desde banderin.es (Origin y Sec-Fetch-Site) y en JSON; la única excepción es la baja de 1 clic de los gestores de correo. Límite de peticiones por IP (`lib/seguridad.js`): caché de Cloudflare para todo y D1 para altas y cuentas.
- **Registro**: los rechazos (origen ajeno, llave falsa, límite, robot) quedan en los registros de Cloudflare y en la tabla `seguridad` de D1, con una huella de la IP que no se puede revertir.
- **Vigilancia** (`.github/workflows/vigilancia.yml`, cada día): resume la actividad sospechosa, comprueba en producción HTTPS, cabeceras, archivos privados y CSRF, y falla (GitHub te avisa por correo) si algo no cuadra.
- **Una vez**: ejecutar `db/migracion-2026-11-18-seguridad.sql` en D1 → Console. Sin ella todo funciona, pero los límites solo cuentan por centro de datos y no se guardan eventos.
- **Copias**: con el secreto `BACKUP_PASSPHRASE` la copia semanal se sube cifrada (AES-256).

## Avisos por correo de Banderín Social

Cuando alguien pide unirse a una partida, es aceptado o envía una solicitud de amistad, la base de
datos (Supabase, `pg_net`) llama a `/api/social/aviso` y la web envía el correo con Brevo.
Hace falta la misma llave larga (24 caracteres o más) en dos sitios; sin ella no se envía nada:

1. Cloudflare Pages → Settings → Variables and Secrets: `SOCIAL_AVISO_SECRETO` (tipo Secret, en Production).
2. Supabase → Integrations → Vault → New secret, con nombre `social_aviso_secreto`.

Cada persona puede apagar los avisos en Social → Mi perfil → Editar perfil. Tope: 12 al día por persona.
