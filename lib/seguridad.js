// Banderín - límites de peticiones y registro de actividad sospechosa (Cloudflare Pages Functions).
// La IP nunca se guarda: solo una huella (SHA-256 con la clave LINK_SECRET y el día), que no se puede revertir.
//
// Dos niveles de límite:
//  - caché de Cloudflare: gratis y rápido, pero cuenta por centro de datos (un atacante repartido lo esquiva);
//  - D1 (tabla «limites»): cuenta global y fiable; se usa solo en las rutas sensibles (altas y cuentas).
// Si la tabla aún no existe (falta db/migracion-2026-11-18-seguridad.sql), se usa solo la caché.

const enc = new TextEncoder();

export async function ipHash(env, request) {
  const ip = request.headers.get('CF-Connecting-IP') || '';
  if (!ip) return '';
  const dia = Math.floor(Date.now() / 86400000);
  const h = await crypto.subtle.digest('SHA-256', enc.encode(ip + '|' + dia + '|' + (env.LINK_SECRET || 'banderin')));
  return [...new Uint8Array(h)].slice(0, 12).map(b => b.toString(16).padStart(2, '0')).join('');
}

async function cacheCount(key, windowSec) {
  const req = new Request('https://limite.banderin.es/' + key);
  const cache = caches.default;
  const hit = await cache.match(req);
  const n = (hit ? parseInt(await hit.text(), 10) || 0 : 0) + 1;
  await cache.put(req, new Response(String(n), { headers: { 'Cache-Control': 'max-age=' + windowSec } }));
  return n;
}

// Devuelve true si se ha pasado del límite. scope: nombre de la regla; max: peticiones; windowSec: ventana.
export async function limited(env, request, scope, max, windowSec, durable = false) {
  const ip = await ipHash(env, request);
  if (!ip) return false;
  const win = Math.floor(Date.now() / 1000 / windowSec);
  const key = scope + '/' + ip + '/' + win;
  let n = 0;
  try { n = await cacheCount(key, windowSec); } catch (e) { n = 0; }
  if (n > max) return true;
  if (durable && env.DB) {
    try {
      const hasta = new Date((win + 1) * windowSec * 1000).toISOString();
      const r = await env.DB.prepare(
        'INSERT INTO limites (clave, n, hasta) VALUES (?, 1, ?) ON CONFLICT(clave) DO UPDATE SET n = n + 1 RETURNING n'
      ).bind(key, hasta).first();
      if (r && r.n > max) return true;
    } catch (e) { /* tabla «limites» aún sin crear: queda el límite de la caché */ }
  }
  return false;
}

// Registra un evento sospechoso: siempre en los registros de Cloudflare y, con tope, en D1 (tabla «seguridad»).
export async function logEvent(env, request, tipo, extra = '') {
  const url = new URL(request.url);
  const ip = await ipHash(env, request).catch(() => '');
  console.warn(JSON.stringify({ seguridad: tipo, ruta: url.pathname, metodo: request.method, ip, pais: request.headers.get('CF-IPCountry') || '', extra: String(extra).slice(0, 120) }));
  if (!env.DB || !ip) return;
  try {
    // Como mucho 30 eventos por IP y hora en la base de datos, para que un ataque no llene D1.
    if (await cacheCount('evento/' + ip + '/' + Math.floor(Date.now() / 3600000), 3600) > 30) return;
    const ventana = new Date(Math.floor(Date.now() / 600000) * 600000).toISOString();
    await env.DB.prepare(
      'INSERT INTO seguridad (ventana, ip, tipo, ruta, n) VALUES (?, ?, ?, ?, 1) ON CONFLICT(ventana, ip, tipo, ruta) DO UPDATE SET n = n + 1'
    ).bind(ventana, ip, tipo, url.pathname.slice(0, 80)).run();
  } catch (e) { /* tabla «seguridad» aún sin crear */ }
}
