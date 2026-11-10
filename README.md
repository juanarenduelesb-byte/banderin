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
