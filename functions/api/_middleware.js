// Banderín · capa común de la API: cabeceras de seguridad, protección CSRF y avisos apagados.
import { enabled, json } from '../../lib/avisos.js';

export async function onRequest(context) {
  const { request, env, next } = context;
  const url = new URL(request.url);
  const write = !['GET', 'HEAD', 'OPTIONS'].includes(request.method);
  // Las escrituras solo se aceptan desde la propia web (o sin Origin: el enlace de baja de 1 clic de los gestores de correo).
  const origin = request.headers.get('Origin');
  if (write && origin && origin !== url.origin) return secure(json({ error: 'origen' }, 403));
  if (url.pathname !== '/api/estado' && !enabled(env)) return secure(json({ error: 'apagado' }, 503));
  let res;
  try {
    res = await next();
  } catch (e) {
    console.error('api', url.pathname, e && e.message);
    res = json({ error: 'interno' }, 500);
  }
  return secure(res);
}

function secure(res) {
  const r = new Response(res.body, res);
  r.headers.set('X-Content-Type-Options', 'nosniff');
  r.headers.set('Referrer-Policy', 'no-referrer');
  r.headers.set('X-Frame-Options', 'DENY');
  r.headers.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains');
  r.headers.set('Cross-Origin-Resource-Policy', 'same-origin');
  if (!r.headers.has('Content-Security-Policy')) r.headers.set('Content-Security-Policy', "default-src 'none'; frame-ancestors 'none'");
  r.headers.delete('Access-Control-Allow-Origin');
  return r;
}
