// Avisos con un toque para quien ya tiene cuenta: Supabase ya verificó ese correo, así que no hace falta
// el correo de confirmación. Se comprueba la sesión contra Supabase y se activa directamente.
import { json, normEmail, randomId, now, readJson, bearer, cleanSigo, cleanPerfil, replaceSigo, manageToken } from '../../../lib/avisos.js';

// Datos públicos del proyecto (los mismos que site/cuenta-config.js).
const SB_URL = 'https://jdyawzbvxucamibbqdzg.supabase.co';
const SB_KEY = 'sb_publishable_hepM5qxH6v3oaICMJLnPLw_Ynz7d7hw';

async function correoVerificado(token) {
  if (!token || token.length > 4096) return null;
  try {
    const r = await fetch(SB_URL + '/auth/v1/user', { headers: { apikey: SB_KEY, Authorization: 'Bearer ' + token } });
    if (!r.ok) return null;
    const u = await r.json();
    if (!u || !u.email || !u.email_confirmed_at) return null;
    return normEmail(u.email);
  } catch (e) { return null; }
}

export async function onRequestPost({ request, env }) {
  const email = await correoVerificado(bearer(request));
  if (!email) return json({ error: 'sesion' }, 401);
  const b = (await readJson(request)) || {};
  const idioma = b.idioma === 'en' ? 'en' : 'es';
  const t = now();
  const prev = await env.DB.prepare('SELECT * FROM suscriptores WHERE email = ?').bind(email).first();
  if (prev && prev.estado === 'activo') {
    // Ya estaba activo: no se tocan sus seguimientos; el navegador sumará los suyos después.
    return json({ ok: true, tok: await manageToken(env, prev.id), email });
  }
  const id = prev ? prev.id : randomId();
  await env.DB.prepare(
    'INSERT INTO suscriptores (id, email, estado, idioma, creado, confirmado, ultimo_correo, ultima_actividad, perfil) VALUES (?, ?, \'activo\', ?, ?, ?, NULL, ?, ?) ' +
    'ON CONFLICT(email) DO UPDATE SET estado = \'activo\', idioma = excluded.idioma, confirmado = COALESCE(suscriptores.confirmado, excluded.confirmado), ultima_actividad = excluded.ultima_actividad, perfil = excluded.perfil'
  ).bind(id, email, idioma, t, t, t, cleanPerfil(b.perfil)).run();
  await replaceSigo(env, id, cleanSigo(b.sigo));
  return json({ ok: true, tok: await manageToken(env, id), email });
}
