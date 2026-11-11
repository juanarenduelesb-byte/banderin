// Baja: borra el correo y todo lo asociado. Sin «cuenta desactivada»: los datos desaparecen.
//  - POST con la llave (desde «Mi perfil» o el botón de baja de 1 clic de Gmail, Apple Mail…)
//  - GET muestra una página con un botón: los antivirus del correo abren enlaces y no deben dar de baja a nadie.
import { json, html, bearer, readManageToken } from '../../../lib/avisos.js';

async function borrar(env, id) {
  await env.DB.batch([
    env.DB.prepare('DELETE FROM enviados WHERE suscriptor = ?').bind(id),
    env.DB.prepare('DELETE FROM seguimientos WHERE suscriptor = ?').bind(id),
    env.DB.prepare('DELETE FROM suscriptores WHERE id = ?').bind(id),
  ]);
}

const page = (title, body, form = '') => html('<!DOCTYPE html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>' + title + ' · Banderín</title>' +
  '<body style="font-family:system-ui,sans-serif;background:#0E2A1E;color:#F4F1E8;display:grid;place-items:center;min-height:100vh;margin:0;padding:24px">' +
  '<main style="max-width:420px;background:#FAF7EE;color:#13201A;border-radius:24px;padding:28px"><h1 style="font-family:Georgia,serif;font-weight:400;margin-top:0">' + title + '</h1><p>' + body + '</p>' + form +
  '<p><a href="/" style="color:#1C4734">Ir a Banderín</a></p></main></body></html>');

export async function onRequestGet({ request, env }) {
  const tok = new URL(request.url).searchParams.get('t') || '';
  const id = await readManageToken(env, tok);
  if (!id) return page('Enlace no válido', 'Este enlace de baja no es correcto o ya se usó.');
  return page('¿Dejar de recibir avisos?', 'Borraremos tu correo y lo que sigues. No recibirás más avisos.',
    '<form method="post" action="/api/avisos/baja?t=' + encodeURIComponent(tok) + '"><button style="background:#1C4734;color:#F4F1E8;border:0;border-radius:999px;padding:12px 20px;font:inherit;font-weight:600;cursor:pointer">Darme de baja</button></form>');
}

export async function onRequestPost({ request, env }) {
  const url = new URL(request.url);
  const tok = bearer(request) || url.searchParams.get('t') || '';
  const id = await readManageToken(env, tok);
  const wantsHtml = (request.headers.get('Accept') || '').includes('text/html');
  if (!id) return wantsHtml ? page('Enlace no válido', 'Este enlace de baja no es correcto o ya se usó.') : json({ error: 'llave' }, 401);
  await borrar(env, id);
  return wantsHtml ? page('Te has dado de baja', 'Hemos borrado tu correo y lo que seguías. No recibirás más avisos.') : json({ ok: true });
}

export async function onRequestDelete(ctx) {
  return onRequestPost(ctx);
}
