// Banderín - una sola dirección: todo lo que llega a banderin.pages.dev o a www.banderin.es
// se redirige de forma permanente (301) a https://banderin.es, conservando la ruta.
// Así Google no ve dos webs iguales y no se pierde ningún enlace antiguo.
const CANON = 'banderin.es';
const OLD = new Set(['banderin.pages.dev', 'www.banderin.es']);

export async function onRequest({ request, next }) {
  const url = new URL(request.url);
  if (OLD.has(url.hostname)) {
    url.hostname = CANON;
    url.protocol = 'https:';
    url.port = '';
    return new Response(null, { status: 301, headers: { Location: url.toString(), 'Cache-Control': 'max-age=86400' } });
  }
  const res = await next();
  // Archivos con huella en el enlace (app.js?v=1a2b…): si cambian, cambia el enlace, así que el navegador
  // puede guardarlos un año sin volver a preguntar. Sin huella se quedan con lo que diga _headers.
  if (res.status === 200 && url.searchParams.has('v') && /\.(js|css|woff2|webp|png|jpg|svg)$/.test(url.pathname)) {
    const r = new Response(res.body, res);
    r.headers.set('Cache-Control', 'public, max-age=31536000, immutable');
    return r;
  }
  return res;
}
