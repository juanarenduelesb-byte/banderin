// Banderín · una sola dirección: todo lo que llega a banderin.pages.dev o a www.banderin.es
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
  return next();
}
