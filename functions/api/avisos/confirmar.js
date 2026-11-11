// Enlace del correo de confirmación: activa los avisos y devuelve a «Mi perfil» con la llave de gestión.
import { html, now, readConfirmToken, manageToken } from '../../../lib/avisos.js';

export async function onRequestGet({ request, env }) {
  const url = new URL(request.url);
  const id = await readConfirmToken(env, url.searchParams.get('t'));
  const sub = id && await env.DB.prepare('SELECT id, idioma FROM suscriptores WHERE id = ?').bind(id).first();
  if (!sub) {
    return html('<!DOCTYPE html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Enlace caducado · Banderín</title>' +
      '<body style="font-family:system-ui,sans-serif;background:#0E2A1E;color:#F4F1E8;display:grid;place-items:center;min-height:100vh;margin:0;padding:24px">' +
      '<main style="max-width:420px;background:#FAF7EE;color:#13201A;border-radius:24px;padding:28px"><h1 style="font-family:Georgia,serif;font-weight:400">Este enlace ya no vale</h1>' +
      '<p>Ha caducado o no es correcto. Vuelve a pedir los avisos desde «Mi perfil» y te enviaremos uno nuevo.</p><p><a href="/#perfil">Ir a Mi perfil</a></p></main></body></html>', 400);
  }
  const t = now();
  await env.DB.prepare('UPDATE suscriptores SET estado = \'activo\', confirmado = COALESCE(confirmado, ?), ultima_actividad = ? WHERE id = ?').bind(t, t, id).run();
  const tok = await manageToken(env, id);
  return Response.redirect(url.origin + (sub.idioma === 'en' ? '/en/' : '/') + '#perfil?avisos=' + encodeURIComponent(tok), 303);
}
