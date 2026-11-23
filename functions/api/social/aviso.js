// Banderín Social - avisos por correo. Solo lo llama la base de datos (Supabase, pg_net) con la llave
// compartida SOCIAL_AVISO_SECRETO; un navegador no puede usarlo. Ver db/social.sql («Avisos por correo»).
import { json, readJson, normEmail, sendMail, mailShell, h1, para, button } from '../../../lib/avisos.js';

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

// Comparación sin fugas de tiempo: se comparan los resúmenes, no las cadenas.
async function igual(a, b) {
  const e = new TextEncoder();
  const [x, y] = await Promise.all([crypto.subtle.digest('SHA-256', e.encode(a)), crypto.subtle.digest('SHA-256', e.encode(b))]);
  const u = new Uint8Array(x), v = new Uint8Array(y);
  let d = 0;
  for (let i = 0; i < u.length; i++) d |= u[i] ^ v[i];
  return d === 0;
}

const limpio = (v, n) => String(v == null ? '' : v).replace(/[\u0000-\u001f\u007f<>]/g, ' ').replace(/\s+/g, ' ').trim().slice(0, n);

function fechaLarga(iso) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(String(iso || ''))) return '';
  return new Date(iso + 'T12:00:00Z').toLocaleDateString('es-ES', { weekday: 'long', day: 'numeric', month: 'long', timeZone: 'UTC' });
}

export function redactar(d, origin) {
  const quien = limpio(d.quien, 40) || 'Un jugador';
  const campo = limpio(d.campo, 80);
  const dia = fechaLarga(d.fecha);
  const donde = campo ? ' en ' + campo + (dia ? ' el ' + dia : '') : '';
  const partida = UUID.test(String(d.partida || '')) ? origin + '/social/#partida/' + d.partida : origin + '/social/#mias';
  switch (d.tipo) {
    case 'solicitud': return { asunto: quien + ' quiere unirse a tu partida', titulo: 'Tienes una solicitud', texto: quien + ' quiere unirse a tu partida' + donde + '. Entra para ver su perfil y aceptar o rechazar.', boton: 'Ver la solicitud', url: partida };
    case 'aceptada': return { asunto: 'Ya tienes partida' + (campo ? ' en ' + campo : ''), titulo: 'Estás dentro', texto: quien + ' te ha aceptado en su partida' + donde + '. Ya podéis hablar en el chat de la partida para cerrar la hora.', boton: 'Abrir la partida', url: partida };
    case 'amistad': return { asunto: quien + ' quiere ser tu amigo en Banderín', titulo: 'Solicitud de amistad', texto: quien + ' te ha enviado una solicitud de amistad en Banderín Social. Los amigos ven vuestras partidas privadas y vuestro contacto.', boton: 'Ver la solicitud', url: origin + '/social/#jugadores' };
    case 'amigo': return { asunto: quien + ' ha aceptado tu amistad', titulo: 'Ya sois amigos', texto: quien + ' ha aceptado tu solicitud de amistad en Banderín Social.', boton: 'Abrir Banderín Social', url: origin + '/social/#jugadores' };
  }
  return null;
}

export async function onRequestPost({ request, env }) {
  const llave = String(env.SOCIAL_AVISO_SECRETO || '');
  if (llave.length < 24 || !(await igual(llave, request.headers.get('X-Aviso-Secreto') || ''))) return json({ error: 'llave' }, 401);
  const d = await readJson(request, 4000);
  const para_ = d && normEmail(d.para);
  if (!d || !para_) return json({ error: 'datos' }, 400);
  const origin = String(env.SITE_URL || 'https://banderin.es').replace(/\/+$/, '');
  const m = redactar(d, origin);
  if (!m) return json({ error: 'tipo' }, 400);
  const pie = 'Recibes este correo porque tienes un perfil en Banderín Social. Puedes apagar estos avisos en Social → Mi perfil → Editar perfil.';
  const htmlBody = mailShell({ lang: 'es', origin, title: m.asunto, pre: m.texto, eyebrow: 'Social',
    inner: h1(m.titulo) + para(m.texto) + button(m.url, m.boton),
    footer: pie.replace(/&/g, '&amp;').replace(/</g, '&lt;') + '<br>Banderín · banderin.es' });
  await sendMail(env, { to: para_, subject: m.asunto, htmlBody, text: m.texto + '\n\n' + m.url + '\n\n' + pie });
  return json({ ok: true });
}
