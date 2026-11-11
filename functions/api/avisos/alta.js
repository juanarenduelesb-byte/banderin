// Alta en los avisos: guarda el correo como pendiente y envía el enlace de confirmación.
// La respuesta es siempre la misma, exista o no el correo, para no revelar quién está suscrito.
import { json, normEmail, randomId, now, readJson, cleanSigo, replaceSigo, sendConfirm, sendAlready } from '../../../lib/avisos.js';

const OK = { ok: true };

export async function onRequestPost({ request, env }) {
  const b = await readJson(request);
  if (!b) return json({ error: 'datos' }, 400);
  if (b.web) return json(OK); // campo trampa: solo lo rellenan los robots
  const email = normEmail(b.email);
  if (!email) return json({ error: 'correo' }, 400);
  const idioma = b.idioma === 'en' ? 'en' : 'es';
  const origin = new URL(request.url).origin;
  const t = now();
  const prev = await env.DB.prepare('SELECT * FROM suscriptores WHERE email = ?').bind(email).first();
  // Como mucho un correo cada 5 minutos a la misma dirección.
  if (prev && prev.ultimo_correo && Date.now() - Date.parse(prev.ultimo_correo) < 5 * 60 * 1000) return json(OK);
  if (prev && prev.estado === 'activo') {
    await sendAlready(env, origin, prev);
    await env.DB.prepare('UPDATE suscriptores SET ultimo_correo = ? WHERE id = ?').bind(t, prev.id).run();
    return json(OK);
  }
  const sub = prev
    ? { ...prev, idioma, creado: t }
    : { id: randomId(), email, idioma, creado: t };
  await env.DB.prepare(
    'INSERT INTO suscriptores (id, email, estado, idioma, creado, ultimo_correo, ultima_actividad) VALUES (?, ?, \'pendiente\', ?, ?, ?, ?) ' +
    'ON CONFLICT(email) DO UPDATE SET idioma = excluded.idioma, creado = excluded.creado, ultimo_correo = excluded.ultimo_correo, ultima_actividad = excluded.ultima_actividad'
  ).bind(sub.id, email, idioma, t, t, t).run();
  await replaceSigo(env, sub.id, cleanSigo(b.sigo));
  await sendConfirm(env, origin, sub);
  return json(OK);
}
