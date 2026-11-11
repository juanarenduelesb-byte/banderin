// Banderín · utilidades compartidas por la API de avisos (Cloudflare Pages Functions).
// Los avisos están apagados mientras falte cualquiera de estas variables del proyecto:
//   AVISOS=on, DB (base de datos D1), BREVO_API_KEY, LINK_SECRET, AVISOS_FROM (correo remitente)

export const MAX_SIGO = { club: 50, prov: 60, torneo: 200 };
const enc = new TextEncoder();

export function enabled(env) {
  return env.AVISOS === 'on' && !!env.DB && !!env.BREVO_API_KEY && !!env.LINK_SECRET && !!env.AVISOS_FROM;
}

export function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store' },
  });
}

export function html(body, status = 200) {
  return new Response(body, {
    status,
    headers: {
      'Content-Type': 'text/html; charset=utf-8',
      'Cache-Control': 'no-store',
      'Content-Security-Policy': "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'",
    },
  });
}

export const now = () => new Date().toISOString();

export function normEmail(v) {
  const e = String(v || '').trim().toLowerCase();
  if (e.length > 254 || !/^[^\s@<>()[\]\\,;:"]+@[a-z0-9-]+(\.[a-z0-9-]+)+$/.test(e)) return null;
  return e;
}

export function randomId() {
  const b = new Uint8Array(16);
  crypto.getRandomValues(b);
  return [...b].map(x => x.toString(16).padStart(2, '0')).join('');
}

function b64url(buf) {
  let s = '';
  for (const x of new Uint8Array(buf)) s += String.fromCharCode(x);
  return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

async function hmac(secret, msg) {
  const key = await crypto.subtle.importKey('raw', enc.encode(secret), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  return b64url(await crypto.subtle.sign('HMAC', key, enc.encode(msg))).slice(0, 32);
}

function same(a, b) {
  if (a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}

// Enlace para gestionar los avisos (y darse de baja): id.firma. Mismo cálculo en pipeline/avisos.py.
export async function manageToken(env, id) {
  return id + '.' + await hmac(env.LINK_SECRET, 'gestion|' + id);
}

export async function readManageToken(env, tok) {
  const m = /^([0-9a-f]{32})\.([A-Za-z0-9_-]{32})$/.exec(String(tok || ''));
  if (!m) return null;
  return same(await hmac(env.LINK_SECRET, 'gestion|' + m[1]), m[2]) ? m[1] : null;
}

// Enlace de confirmación: caduca a las 48 horas.
export async function confirmToken(env, id, creado) {
  const t = Date.parse(creado).toString(36);
  return id + '.' + t + '.' + await hmac(env.LINK_SECRET, 'confirmar|' + id + '|' + t);
}

export async function readConfirmToken(env, tok) {
  const m = /^([0-9a-f]{32})\.([0-9a-z]{1,12})\.([A-Za-z0-9_-]{32})$/.exec(String(tok || ''));
  if (!m) return null;
  if (!same(await hmac(env.LINK_SECRET, 'confirmar|' + m[1] + '|' + m[2]), m[3])) return null;
  if (Date.now() - parseInt(m[2], 36) > 48 * 3600 * 1000) return null;
  return m[1];
}

export function bearer(request) {
  const h = request.headers.get('Authorization') || '';
  return h.startsWith('Bearer ') ? h.slice(7).trim() : '';
}

export async function readJson(request, max = 20000) {
  const len = Number(request.headers.get('Content-Length') || 0);
  if (len > max) return null;
  const text = await request.text();
  if (text.length > max) return null;
  try { return JSON.parse(text); } catch { return null; }
}

// Lo que sigue la persona, limpio y acotado.
export function cleanSigo(s) {
  const out = [];
  const add = (tipo, arr) => {
    if (!Array.isArray(arr)) return;
    const seen = new Set();
    for (const v of arr) {
      const k = String(v || '').trim().slice(0, 300);
      if (!k || seen.has(k)) continue;
      if (tipo === 'torneo' && !/^https?:\/\//.test(k)) continue;
      seen.add(k);
      out.push([tipo, k]);
      if (seen.size >= MAX_SIGO[tipo]) break;
    }
  };
  add('club', s && s.clubs);
  add('prov', s && s.prov);
  add('torneo', s && s.torneos);
  return out;
}

export async function replaceSigo(env, id, pairs) {
  const st = [env.DB.prepare('DELETE FROM seguimientos WHERE suscriptor = ?').bind(id)];
  for (const [tipo, clave] of pairs) {
    st.push(env.DB.prepare('INSERT OR IGNORE INTO seguimientos (suscriptor, tipo, clave) VALUES (?, ?, ?)').bind(id, tipo, clave));
  }
  await env.DB.batch(st);
}

export async function readSigo(env, id) {
  const r = await env.DB.prepare('SELECT tipo, clave FROM seguimientos WHERE suscriptor = ? ORDER BY tipo, clave').bind(id).all();
  const s = { clubs: [], prov: [], torneos: [] };
  for (const x of r.results || []) (x.tipo === 'club' ? s.clubs : x.tipo === 'prov' ? s.prov : s.torneos).push(x.clave);
  return s;
}

const T = {
  es: {
    confirmSubject: 'Confirma tus avisos de Banderín',
    confirmTitle: 'Confirma tus avisos',
    confirmBody: 'Pulsa el botón para empezar a recibir avisos de los torneos que sigues: cuándo abre o cierra la inscripción, torneos nuevos, cambios de fecha y cancelaciones. Como mucho, un correo al día.',
    confirmBtn: 'Confirmar mis avisos',
    confirmFoot: 'Si no has pedido esto, ignora este correo: sin confirmar no recibirás nada y tu dirección se borrará en 7 días.',
    againSubject: 'Tus avisos de Banderín ya están activos',
    againTitle: 'Ya tienes los avisos activos',
    againBody: 'Alguien (seguramente tú) ha pedido activar los avisos con este correo, pero ya estaban activos. Desde aquí puedes ver lo que sigues o darte de baja.',
    againBtn: 'Gestionar mis avisos',
    sign: 'Banderín · Todos los torneos de golf de España',
  },
  en: {
    confirmSubject: 'Confirm your Banderín alerts',
    confirmTitle: 'Confirm your alerts',
    confirmBody: 'Press the button to start getting alerts about the tournaments you follow: when entries open or close, new tournaments, date changes and cancellations. At most one email a day.',
    confirmBtn: 'Confirm my alerts',
    confirmFoot: 'If you did not ask for this, ignore this email: without confirming you will get nothing and your address will be deleted in 7 days.',
    againSubject: 'Your Banderín alerts are already on',
    againTitle: 'Your alerts are already on',
    againBody: 'Someone (probably you) asked to turn on alerts with this email, but they were already on. From here you can see what you follow or unsubscribe.',
    againBtn: 'Manage my alerts',
    sign: 'Banderín · Every golf tournament in Spain',
  },
};

export function mailLayout({ title, body, btn, url, foot, sign }) {
  const e = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  return '<!DOCTYPE html><html><body style="margin:0;background:#0E2A1E;padding:24px 12px;font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif">' +
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr><td align="center">' +
    '<table role="presentation" width="100%" style="max-width:520px;background:#FAF7EE;border-radius:20px" cellpadding="0" cellspacing="0"><tr><td style="padding:28px 28px 24px;color:#13201A">' +
    '<p style="margin:0 0 18px;font-weight:700;font-size:18px;letter-spacing:-.02em">⛳ banderín</p>' +
    '<h1 style="margin:0 0 12px;font-family:Georgia,serif;font-weight:400;font-size:28px;line-height:1.1">' + e(title) + '</h1>' +
    '<p style="margin:0 0 22px;font-size:15px;line-height:1.55;color:#3B4A41">' + e(body) + '</p>' +
    '<p style="margin:0 0 22px"><a href="' + e(url) + '" style="display:inline-block;background:#1C4734;color:#F4F1E8;text-decoration:none;font-weight:600;padding:12px 20px;border-radius:999px">' + e(btn) + '</a></p>' +
    (foot ? '<p style="margin:0;font-size:13px;line-height:1.5;color:#6B776F">' + e(foot) + '</p>' : '') +
    '</td></tr></table><p style="margin:14px 0 0;font-size:12px;color:#9FB2A6">' + e(sign) + '</p></td></tr></table></body></html>';
}

export async function sendMail(env, { to, subject, htmlBody, text, unsubscribe }) {
  const from = String(env.AVISOS_FROM);
  const payload = {
    sender: { name: 'Banderín', email: from },
    to: [{ email: to }],
    subject,
    htmlContent: htmlBody,
    textContent: text,
  };
  if (unsubscribe) payload.headers = { 'List-Unsubscribe': '<' + unsubscribe + '>', 'List-Unsubscribe-Post': 'List-Unsubscribe=One-Click' };
  const r = await fetch((env.BREVO_API_URL || 'https://api.brevo.com') + '/v3/smtp/email', {
    method: 'POST',
    headers: { 'api-key': env.BREVO_API_KEY, 'Content-Type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!r.ok) throw new Error('Brevo ' + r.status);
}

export async function sendConfirm(env, origin, sub) {
  const t = T[sub.idioma] || T.es;
  const url = origin + '/api/avisos/confirmar?t=' + encodeURIComponent(await confirmToken(env, sub.id, sub.creado));
  await sendMail(env, {
    to: sub.email, subject: t.confirmSubject,
    htmlBody: mailLayout({ title: t.confirmTitle, body: t.confirmBody, btn: t.confirmBtn, url, foot: t.confirmFoot, sign: t.sign }),
    text: t.confirmTitle + '\n\n' + t.confirmBody + '\n\n' + url + '\n\n' + t.confirmFoot,
  });
}

export async function sendAlready(env, origin, sub) {
  const t = T[sub.idioma] || T.es;
  const tok = await manageToken(env, sub.id);
  const url = origin + (sub.idioma === 'en' ? '/en/' : '/') + '#perfil?avisos=' + encodeURIComponent(tok);
  await sendMail(env, {
    to: sub.email, subject: t.againSubject,
    htmlBody: mailLayout({ title: t.againTitle, body: t.againBody, btn: t.againBtn, url, sign: t.sign }),
    text: t.againTitle + '\n\n' + t.againBody + '\n\n' + url,
    unsubscribe: origin + '/api/avisos/baja?t=' + encodeURIComponent(tok),
  });
}
