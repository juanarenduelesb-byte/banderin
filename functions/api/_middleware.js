// Banderín - capa común de la API: cabeceras de seguridad, protección CSRF, límite de peticiones,
// registro de actividad sospechosa y avisos apagados.
import { enabled, json } from '../../lib/avisos.js';
import { limited, logEvent } from '../../lib/seguridad.js';

// Única escritura que puede llegar sin Origin: el botón de baja de 1 clic de Gmail, Apple Mail… (RFC 8058).
const SIN_ORIGEN = new Set(['/api/avisos/baja']);
const ESCRITURAS_POR_IP = 40;   // escrituras a la API por IP cada 10 minutos
const LECTURAS_POR_IP = 300;    // lecturas a la API por IP cada 10 minutos

export async function onRequest(context) {
  const { request, env, next } = context;
  const url = new URL(request.url);
  const write = !['GET', 'HEAD', 'OPTIONS'].includes(request.method);
  const deny = async (tipo, status, extra) => { await logEvent(env, request, tipo, extra); return secure(json({ error: tipo }, status)); };

  if (write) {
    // CSRF: las escrituras solo se aceptan desde la propia web.
    const origin = request.headers.get('Origin');
    if (origin && origin !== url.origin) return deny('origen', 403, origin);
    if (!origin && !SIN_ORIGEN.has(url.pathname)) return deny('origen', 403, 'sin origen');
    const site = request.headers.get('Sec-Fetch-Site');
    if (site && !['same-origin', 'none'].includes(site) && !SIN_ORIGEN.has(url.pathname)) return deny('sitio', 403, site);
    // La API solo habla JSON (un formulario de otra web no puede enviar application/json sin permiso CORS).
    const ct = (request.headers.get('Content-Type') || '').toLowerCase();
    if (!SIN_ORIGEN.has(url.pathname) && !ct.startsWith('application/json')) return deny('tipo', 415, ct.slice(0, 60));
  }
  if (await limited(env, request, write ? 'w' : 'r', write ? ESCRITURAS_POR_IP : LECTURAS_POR_IP, 600)) return deny('limite', 429);
  if (url.pathname !== '/api/estado' && !enabled(env)) return secure(json({ error: 'apagado' }, 503));
  let res;
  try {
    res = await next();
  } catch (e) {
    console.error('api', url.pathname, e && e.message);
    await logEvent(env, request, 'interno', e && e.message);
    res = json({ error: 'interno' }, 500);
  }
  // Llaves falsas, robots y límites de cada ruta también quedan registrados.
  if ([401, 403, 429].includes(res.status)) await logEvent(env, request, res.status === 401 ? 'llave' : res.status === 429 ? 'limite' : 'robot');
  return secure(res);
}

function secure(res) {
  const r = new Response(res.body, res);
  r.headers.set('X-Content-Type-Options', 'nosniff');
  r.headers.set('Referrer-Policy', 'no-referrer');
  r.headers.set('X-Frame-Options', 'DENY');
  r.headers.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  r.headers.set('Cross-Origin-Resource-Policy', 'same-origin');
  r.headers.set('Cache-Control', r.headers.get('Cache-Control') || 'no-store');
  if (!r.headers.has('Content-Security-Policy')) r.headers.set('Content-Security-Policy', "default-src 'none'; frame-ancestors 'none'");
  r.headers.delete('Access-Control-Allow-Origin');
  return r;
}
