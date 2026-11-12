// Alta en los avisos: guarda el correo como pendiente y envía el enlace de confirmación.
// La respuesta es siempre la misma, exista o no el correo, para no revelar quién está suscrito.
import { json, normEmail, randomId, now, readJson, cleanSigo, cleanPerfil, replaceSigo, sendConfirm, sendAlready } from '../../../lib/avisos.js';

const OK = { ok: true };
const POR_IP_HORA = 6;        // altas por IP y hora (cada centro de datos de Cloudflare cuenta las suyas)
const TOPE_GLOBAL_HORA = 150; // freno de emergencia: altas pendientes nuevas en toda la web por hora
const REENVIO_MIN = 60;       // el mismo correo recibe como mucho un mensaje por hora

// Contador por IP sin guardar la IP: huella SHA-256 con la hora, en la caché de Cloudflare (se borra sola).
async function demasiadosPorIp(request) {
  const ip = request.headers.get('CF-Connecting-IP') || '';
  if (!ip) return false;
  const hora = Math.floor(Date.now() / 3600000);
  const h = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(ip + '|' + hora + '|banderin'));
  const id = [...new Uint8Array(h)].slice(0, 12).map(b => b.toString(16).padStart(2, '0')).join('');
  const key = new Request('https://limite.banderin.es/alta/' + id);
  const cache = caches.default;
  const hit = await cache.match(key);
  const n = hit ? parseInt(await hit.text(), 10) || 0 : 0;
  if (n >= POR_IP_HORA) return true;
  await cache.put(key, new Response(String(n + 1), { headers: { 'Cache-Control': 'max-age=3600' } }));
  return false;
}

// Turnstile: solo se exige si la clave secreta está puesta en Cloudflare Pages (TURNSTILE_SECRET).
async function robot(env, request, token) {
  if (!env.TURNSTILE_SECRET) return false;
  if (!token || typeof token !== 'string' || token.length > 2048) return true;
  const form = new FormData();
  form.append('secret', env.TURNSTILE_SECRET);
  form.append('response', token);
  const ip = request.headers.get('CF-Connecting-IP');
  if (ip) form.append('remoteip', ip);
  try {
    const r = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', body: form });
    const d = await r.json();
    return !d.success;
  } catch (e) {
    return false; // si Turnstile no responde, no bloqueamos a la gente: quedan los demás límites
  }
}

export async function onRequestPost({ request, env }) {
  const b = await readJson(request);
  if (!b) return json({ error: 'datos' }, 400);
  if (b.web) return json(OK); // campo trampa: solo lo rellenan los robots
  if (await robot(env, request, b.ts)) return json({ error: 'robot' }, 403);
  if (await demasiadosPorIp(request)) return json({ error: 'limite' }, 429);
  const email = normEmail(b.email);
  if (!email) return json({ error: 'correo' }, 400);
  const idioma = b.idioma === 'en' ? 'en' : 'es';
  const origin = new URL(request.url).origin;
  const t = now();
  const prev = await env.DB.prepare('SELECT * FROM suscriptores WHERE email = ?').bind(email).first();
  // Como mucho un correo por hora a la misma dirección.
  if (prev && prev.ultimo_correo && Date.now() - Date.parse(prev.ultimo_correo) < REENVIO_MIN * 60 * 1000) return json(OK);
  // Freno de emergencia: si en la última hora hay demasiadas altas nuevas sin confirmar, alguien está abusando.
  if (!prev) {
    const desde = new Date(Date.now() - 3600000).toISOString();
    const n = await env.DB.prepare("SELECT COUNT(*) AS n FROM suscriptores WHERE estado = 'pendiente' AND creado > ?").bind(desde).first();
    if (n && n.n >= TOPE_GLOBAL_HORA) { console.warn('alta: tope global alcanzado'); return json({ error: 'limite' }, 429); }
  }
  if (prev && prev.estado === 'activo') {
    await sendAlready(env, origin, prev);
    await env.DB.prepare('UPDATE suscriptores SET ultimo_correo = ? WHERE id = ?').bind(t, prev.id).run();
    return json(OK);
  }
  const sub = prev
    ? { ...prev, idioma, creado: t }
    : { id: randomId(), email, idioma, creado: t };
  await env.DB.prepare(
    'INSERT INTO suscriptores (id, email, estado, idioma, creado, ultimo_correo, ultima_actividad, perfil) VALUES (?, ?, \'pendiente\', ?, ?, ?, ?, ?) ' +
    'ON CONFLICT(email) DO UPDATE SET idioma = excluded.idioma, creado = excluded.creado, ultimo_correo = excluded.ultimo_correo, ultima_actividad = excluded.ultima_actividad, perfil = excluded.perfil'
  ).bind(sub.id, email, idioma, t, t, t, cleanPerfil(b.perfil)).run();
  await replaceSigo(env, sub.id, cleanSigo(b.sigo));
  await sendConfirm(env, origin, sub);
  return json(OK);
}
