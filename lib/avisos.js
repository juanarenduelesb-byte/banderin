// Banderín - utilidades compartidas por la API de avisos (Cloudflare Pages Functions).
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
  // Se lee por trozos y se corta en cuanto pasa del tope (aunque no venga Content-Length).
  if (!request.body) return null;
  const reader = request.body.getReader();
  const chunks = []; let size = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    size += value.byteLength;
    if (size > max) { try { await reader.cancel(); } catch (e) {} return null; }
    chunks.push(value);
  }
  const buf = new Uint8Array(size); let o = 0;
  for (const c of chunks) { buf.set(c, o); o += c.byteLength; }
  try {
    const d = JSON.parse(new TextDecoder().decode(buf));
    return d && typeof d === 'object' && !Array.isArray(d) ? d : null;
  } catch { return null; }
}

// Perfil de golfista (opcional): solo lo necesario para no sugerir torneos que no encajan.
export function cleanPerfil(p) {
  if (!p || typeof p !== 'object') return null;
  const o = {};
  if (p.sexo === 'M' || p.sexo === 'F') o.sexo = p.sexo;
  const nac = Number(p.nac); if (nac >= 1900 && nac <= 2030) o.nac = nac;
  const h = Number(p.hcp); if (p.hcp !== null && p.hcp !== undefined && p.hcp !== '' && isFinite(h) && h >= -10 && h <= 54) o.hcp = h;
  if (typeof p.fed === 'string' && p.fed.length < 60) o.fed = p.fed;
  if (Array.isArray(p.clubs)) o.clubs = p.clubs.filter(c => typeof c === 'string').map(c => c.slice(0, 120)).slice(0, 10);
  return Object.keys(o).length ? JSON.stringify(o) : null;
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

export const T = {
  es: {
    eyebrow: 'Avisos',
    confirmSubject: 'Confirma tus avisos de Banderín',
    confirmPre: 'Un clic y empezamos a avisarte de lo que sigues.',
    confirmTitle: 'Confirma tus avisos',
    confirmBody: 'Pulsa el botón y empezaremos a avisarte de los torneos, clubes y provincias que sigues:',
    confirmList: ['Cuándo abre y cierra la inscripción', 'Torneos nuevos en tus clubes y provincias', 'Cambios de fecha y cancelaciones', 'Los jueves, lo que se juega el fin de semana en tu comunidad'],
    confirmBtn: 'Confirmar mis avisos',
    confirmFoot: 'Como mucho, un correo al día. Si no has pedido esto, ignora este mensaje: sin confirmar no recibirás nada y tu dirección se borrará en 7 días.',
    againSubject: 'Tus avisos de Banderín ya están activos',
    againPre: 'No hace falta hacer nada: ya los tenías.',
    againTitle: 'Ya tienes los avisos activos',
    againBody: 'Alguien (seguramente tú) ha pedido activar los avisos con este correo, pero ya estaban activos. Desde aquí puedes ver lo que sigues o darte de baja.',
    againBtn: 'Gestionar mis avisos',
    why: 'Recibes este correo porque se han pedido avisos de Banderín con esta dirección.',
    manage: 'Gestionar avisos', unsub: 'Darme de baja',
    sign: 'Banderín - un proyecto de Esclusa - Confirma siempre fechas y condiciones con el organizador.',
  },
  en: {
    eyebrow: 'Alerts',
    confirmSubject: 'Confirm your Banderín alerts',
    confirmPre: 'One click and we start alerting you about what you follow.',
    confirmTitle: 'Confirm your alerts',
    confirmBody: 'Press the button and we will start alerting you about the tournaments, clubs and provinces you follow:',
    confirmList: ['When entries open and close', 'New tournaments at your clubs and provinces', 'Date changes and cancellations', 'On Thursdays, what is on this weekend in your region'],
    confirmBtn: 'Confirm my alerts',
    confirmFoot: 'At most one email a day. If you did not ask for this, ignore this message: without confirming you will get nothing and your address will be deleted in 7 days.',
    againSubject: 'Your Banderín alerts are already on',
    againPre: 'Nothing to do: they were already on.',
    againTitle: 'Your alerts are already on',
    againBody: 'Someone (probably you) asked to turn on alerts with this email, but they were already on. From here you can see what you follow or unsubscribe.',
    againBtn: 'Manage my alerts',
    why: 'You get this email because Banderín alerts were requested for this address.',
    manage: 'Manage alerts', unsub: 'Unsubscribe',
    sign: 'Banderín - a project by Esclusa - Always confirm dates and conditions with the organiser.',
  },
};

// Plantilla de correo: la misma que pipeline/correo.py (si cambias una, cambia la otra).
const SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif";
const SERIF = "'Libre Caslon Display',Georgia,'Times New Roman',serif";
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');

export function mailShell({ lang, origin, title, pre, eyebrow, inner, footer }) {
  return '<!DOCTYPE html><html lang="' + lang + '"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">' +
    '<meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light"><title>' + esc(title) + '</title>' +
    '<style>@media (max-width:600px){.px{padding-left:22px!important;padding-right:22px!important}.h1{font-size:29px!important}.hd{padding-left:22px!important;padding-right:22px!important}}</style></head>' +
    '<body style="margin:0;padding:0;background:#ECE8DA">' +
    '<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:transparent;mso-hide:all">' + esc(pre) + '&nbsp;&zwnj;'.repeat(40) + '</div>' +
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#ECE8DA"><tr><td align="center" style="padding:26px 10px 34px">' +
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px">' +
    '<tr><td class="hd" bgcolor="#163D2B" style="background:#163D2B;border-radius:24px 24px 0 0;padding:24px 34px 22px">' +
    '<table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>' +
    '<td width="40" valign="middle"><img src="' + esc(origin) + '/icons/icon-192.png" width="34" height="34" alt="" style="display:block;border:0;border-radius:9px"></td>' +
    '<td valign="middle" style="padding-left:10px;font:700 22px/1 ' + SANS + ';letter-spacing:-.03em;color:#FAF7EE">banderín</td>' +
    '<td align="right" valign="middle" style="font:700 11px/1 ' + SANS + ';letter-spacing:.16em;text-transform:uppercase;color:#E9C77E">' + esc(eyebrow) + '</td>' +
    '</tr></table><div style="margin-top:18px;height:3px;width:44px;background:#E9C77E;border-radius:3px;font-size:0;line-height:0">&nbsp;</div></td></tr>' +
    '<tr><td class="px" style="background:#FAF7EE;border-radius:0 0 24px 24px;padding:32px 34px 34px">' + inner + '</td></tr>' +
    '<tr><td style="padding:22px 18px 0;text-align:center;font:12.5px/1.65 ' + SANS + ';color:#55645B">' + footer + '</td></tr>' +
    '</table></td></tr></table></body></html>';
}

export const h1 = t => '<h1 class="h1" style="margin:0 0 12px;font-family:' + SERIF + ';font-weight:400;font-size:34px;line-height:1.05;letter-spacing:-.01em;color:#13201A">' + esc(t) + '</h1>';
export const para = (t, size = 15.5, color = '#55645B', margin = '0 0 22px') => '<p style="margin:' + margin + ';font:' + size + 'px/1.6 ' + SANS + ';color:' + color + '">' + esc(t) + '</p>';
export const button = (url, label) => '<a href="' + esc(url) + '" style="display:inline-block;background:#163D2B;color:#FAF7EE;border:1.5px solid #163D2B;font:600 15.5px/1 ' + SANS + ';text-decoration:none;padding:16px 28px;border-radius:999px">' + esc(label) + '</a>';
export const bullets = items => '<table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 26px">' + items.map(x =>
  '<tr><td width="18" valign="top" style="padding:6px 0"><div style="width:7px;height:7px;border-radius:50%;background:#C9A86A;margin-top:7px"></div></td>' +
  '<td style="padding:4px 0;font:15px/1.5 ' + SANS + ';color:#13201A">' + esc(x) + '</td></tr>').join('') + '</table>';
export function mailFooter(t, manage, unsub) {
  const links = [];
  if (manage) links.push('<a href="' + esc(manage) + '" style="color:#1C4734;text-decoration:underline">' + esc(t.manage) + '</a>');
  if (unsub) links.push('<a href="' + esc(unsub) + '" style="color:#1C4734;text-decoration:underline">' + esc(t.unsub) + '</a>');
  return [esc(t.why), links.join(' &nbsp;-&nbsp; '), esc(t.sign)].filter(Boolean).join('<br>');
}

export function confirmMail(lang, origin, url) {
  const t = T[lang] || T.es;
  return mailShell({ lang, origin, title: t.confirmSubject, pre: t.confirmPre, eyebrow: t.eyebrow,
    inner: h1(t.confirmTitle) + para(t.confirmBody, 15.5, '#55645B', '0 0 14px') + bullets(t.confirmList) + button(url, t.confirmBtn) +
      para(t.confirmFoot, 13, '#6B776F', '26px 0 0'),
    footer: mailFooter(t) });
}

export function alreadyMail(lang, origin, manage, unsub) {
  const t = T[lang] || T.es;
  return mailShell({ lang, origin, title: t.againSubject, pre: t.againPre, eyebrow: t.eyebrow,
    inner: h1(t.againTitle) + para(t.againBody) + button(manage, t.againBtn),
    footer: mailFooter(t, manage, unsub) });
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
    htmlBody: confirmMail(sub.idioma, origin, url),
    text: t.confirmTitle + '\n\n' + t.confirmBody + '\n- ' + t.confirmList.join('\n- ') + '\n\n' + url + '\n\n' + t.confirmFoot,
  });
}

export async function sendAlready(env, origin, sub) {
  const t = T[sub.idioma] || T.es;
  const tok = await manageToken(env, sub.id);
  const manage = origin + (sub.idioma === 'en' ? '/en/' : '/') + '#perfil?avisos=' + encodeURIComponent(tok);
  const unsub = origin + '/api/avisos/baja?t=' + encodeURIComponent(tok);
  await sendMail(env, {
    to: sub.email, subject: t.againSubject,
    htmlBody: alreadyMail(sub.idioma, origin, manage, unsub),
    text: t.againTitle + '\n\n' + t.againBody + '\n\n' + manage + '\n\n' + t.unsub + ': ' + unsub,
    unsubscribe: unsub,
  });
}
