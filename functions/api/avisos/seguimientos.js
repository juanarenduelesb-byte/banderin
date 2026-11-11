// La web envía aquí lo que sigue la persona cada vez que cambia, para que los avisos estén al día.
import { json, bearer, readManageToken, readJson, cleanSigo, replaceSigo, now } from '../../../lib/avisos.js';

export async function onRequestPut({ request, env }) {
  const id = await readManageToken(env, bearer(request));
  if (!id) return json({ error: 'llave' }, 401);
  const exists = await env.DB.prepare('SELECT 1 FROM suscriptores WHERE id = ?').bind(id).first();
  if (!exists) return json({ error: 'llave' }, 401);
  const b = await readJson(request);
  if (!b) return json({ error: 'datos' }, 400);
  await replaceSigo(env, id, cleanSigo(b.sigo));
  await env.DB.prepare('UPDATE suscriptores SET ultima_actividad = ? WHERE id = ?').bind(now(), id).run();
  return json({ ok: true });
}
