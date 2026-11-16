// Enlace para compartir un torneo: banderin.es/t/<id>. Devuelve una página mínima con la vista previa
// (título, fecha y club) para WhatsApp, Instagram, etc., y lleva al torneo dentro de Banderín.
// El id es el FNV-1a del enlace del torneo, igual que tid() en site/app.js.
function tid(u) { let h = 2166136261; for (let i = 0; i < u.length; i++) { h ^= u.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; } return h.toString(36); }
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const MES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'];
const fecha = s => { const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(s || ''); return m ? (+m[3]) + ' ' + MES[+m[2] - 1] + ' ' + m[1] : ''; };

export async function onRequestGet({ request, env, params }) {
  const id = String(params.id || '').toLowerCase();
  const origin = new URL(request.url).origin;
  let t = null;
  if (/^[a-z0-9]{1,8}$/.test(id)) {
    try {
      const r = await env.ASSETS.fetch(new Request(origin + '/data.js'));
      const s = await r.text();
      const a = s.indexOf('window.TORNEOS=');
      if (a >= 0) {
        const start = s.indexOf('[', a);
        const end = s.indexOf('];', start);
        const list = JSON.parse(s.slice(start, end + 1));
        t = list.find(x => x && x.url && tid(x.url) === id) || null;
      }
    } catch (e) { t = null; }
  }
  const dest = t ? '/#t=' + id : '/';
  const title = t ? t.n + ' - Banderín' : 'Banderín - Todos los torneos de golf de España';
  const desc = t ? [fecha(t.s), t.club, t.city || t.prov].filter(Boolean).join(' - ') + '. Mira el torneo y apúntate en Banderín.' : 'Todos los torneos de golf de España en un solo sitio.';
  const body = '<!DOCTYPE html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' +
    '<title>' + esc(title) + '</title><meta name="robots" content="noindex">' +
    '<meta name="description" content="' + esc(desc) + '">' +
    '<meta property="og:type" content="website"><meta property="og:site_name" content="Banderín">' +
    '<meta property="og:title" content="' + esc(title) + '"><meta property="og:description" content="' + esc(desc) + '">' +
    '<meta property="og:url" content="' + esc(origin + '/t/' + id) + '"><meta property="og:image" content="' + esc(origin + '/og.png') + '">' +
    '<meta name="twitter:card" content="summary_large_image">' +
    '<meta http-equiv="refresh" content="0;url=' + esc(dest) + '"><link rel="canonical" href="' + esc(origin + '/') + '"></head>' +
    '<body style="font-family:system-ui,sans-serif;background:#0E2A1E;color:#F4F1E8;display:grid;place-items:center;min-height:100vh;margin:0">' +
    '<p><a style="color:#E9C77E" href="' + esc(dest) + '">' + esc(t ? 'Abrir ' + t.n + ' en Banderín' : 'Ir a Banderín') + '</a></p></body></html>';
  return new Response(body, { status: t ? 200 : 404, headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'public, max-age=600' } });
}
