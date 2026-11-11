// Estado de los avisos de quien tiene la llave de gestión (la guarda su navegador).
import { json, bearer, readManageToken, readSigo } from '../../../lib/avisos.js';

export async function onRequestGet({ request, env }) {
  const id = await readManageToken(env, bearer(request));
  const sub = id && await env.DB.prepare('SELECT email, estado, idioma FROM suscriptores WHERE id = ?').bind(id).first();
  if (!sub) return json({ error: 'llave' }, 401);
  return json({ email: sub.email, estado: sub.estado, idioma: sub.idioma, sigo: await readSigo(env, id) });
}
