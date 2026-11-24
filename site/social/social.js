// Banderín Social (versión de prueba) · partidas, busco pareja, amigos y perfiles de jugador.
// Usa las cuentas de Banderín (Supabase). Sin sesión, o si la base de datos aún no está preparada,
// enseña una vista previa con datos de ejemplo y no guarda nada.
(() => {
'use strict';
const $ = s => document.querySelector(s), view = $('#view');
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const CU = window.CUENTA || {};
const SB = window.supabase && CU.url ? window.supabase.createClient(CU.url, CU.key, {
  auth: { flowType: 'pkce', persistSession: true, autoRefreshToken: true, detectSessionInUrl: true } }) : null;

// ───────── Fechas ─────────
const pad = n => String(n).padStart(2, '0');
const isoOf = d => d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate());
const TODAY = isoOf(new Date());
const addDays = (n, base = new Date()) => { const d = new Date(base); d.setDate(d.getDate() + n); return isoOf(d); };
const D = s => new Date(s + 'T12:00:00');
const F = {};
const fmt = (k, o) => F[k] || (F[k] = new Intl.DateTimeFormat('es-ES', o));
const dow = s => fmt('w', { weekday: 'short' }).format(D(s)).replace('.', '');
const mon = s => fmt('m', { month: 'short' }).format(D(s)).replace('.', '');
const dlong = s => fmt('l', { weekday: 'long', day: 'numeric', month: 'long' }).format(D(s));
const when = s => s === TODAY ? 'Hoy' : s === addDays(1) ? 'Mañana' : dlong(s).replace(/^./, c => c.toUpperCase());
const hhmm = h => h ? h.slice(0, 5) : '';
const weekend = () => { const d = new Date(), w = d.getDay(); const toSat = (6 - w + 7) % 7; const sat = w === 0 ? addDays(-1) : addDays(toSat); return [w === 0 ? TODAY : sat, addDays(w === 0 ? 0 : toSat + 1)]; };

// ───────── Datos de Banderín: clubes, provincias y torneos por parejas ─────────
const TT = Array.isArray(window.TORNEOS) ? window.TORNEOS : [];
const CLUBS = new Map(), CINFO = new Map();   // club -> provincia · club -> [localidad, provincia, lat, lng, hoyos]
(window.CLUBES || []).forEach(c => { CLUBS.set(c[0], c[2]); CINFO.set(c[0], c.slice(1)); });
TT.forEach(t => { if (t.club && t.prov && t.prov !== 'Por confirmar' && !CLUBS.has(t.club)) { CLUBS.set(t.club, t.prov); CINFO.set(t.club, [(t.city || '').split(' (')[0], t.prov, t.ll ? t.ll[0] : null, t.ll ? t.ll[1] : null, 0]); } });
const fold = x => String(x || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
const CLIST = [...CLUBS.keys()].map(k => [k, fold(k + ' ' + ((CINFO.get(k) || [])[0] || ''))]);
const findClubs = (txt, skip = []) => { const w = fold(txt).split(/\s+/).filter(Boolean); return w.length ? CLIST.filter(([k, f]) => !skip.includes(k) && w.every(x => f.includes(x))).slice(0, 7).map(([k]) => k) : []; };
const whereOf = c => { const i = CINFO.get(c); return i ? [i[0], i[1]].filter(Boolean).join(', ') : ''; };
const mapsUrl = c => 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent(c + (whereOf(c) ? ', ' + whereOf(c) : ''));
const clubSugg = L => L.map(k => `<button type="button" data-c="${esc(k)}">${esc(k)}<small>${esc(whereOf(k))}</small></button>`).join('');
const PROVS = [...new Set([...CLUBS.values()])].sort((a, b) => a.localeCompare(b, 'es'));
// Perfil único: la parte privada (para «Encajan conmigo» en Torneos) usa los clubes tal como los publican los torneos.
const TCLIST = [...new Set(TT.map(t => t.club).filter(Boolean))].map(k => [k, fold(k + ' ' + ((CINFO.get(k) || [])[0] || ''))]);
const findTClubs = (txt, skip = []) => { const w = fold(txt).split(/\s+/).filter(Boolean); return w.length ? TCLIST.filter(([k, f]) => !skip.includes(k) && w.every(x => f.includes(x))).slice(0, 7).map(([k]) => k) : []; };
const CCAA = ['Andalucía', 'Aragón', 'Canarias', 'Cantabria', 'Castilla y León', 'Castilla-La Mancha', 'Cataluña', 'Comunidad de Madrid', 'Comunidad Foral de Navarra', 'Comunitat Valenciana', 'Extremadura', 'Galicia', 'Illes Balears', 'La Rioja', 'País Vasco', 'Principado de Asturias', 'Región de Murcia', 'Ceuta', 'Melilla'];
const tid = t => { let h = 2166136261; const u = t.url || ''; for (let i = 0; i < u.length; i++) { h ^= u.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0 } return h.toString(36) };
const PAREJAS = TT.filter(t => t.form === 'Parejas' && t.s >= TODAY && t.s <= addDays(60) && t.cat !== 'Juvenil' && t.cat !== 'Profesional')
  .sort((a, b) => a.s.localeCompare(b.s));
const safeUrl = u => /^https:\/\//.test(u || '') ? u : '';

// ───────── Estado ─────────
let ME = null, EST = null, MYP = null, MYC = null, DEMO = true, NOSQL = false;
let CHAT = 0;
let FIL = { prov: '', cuando: 'todas', hcp: false, tipo: '' };

// ───────── Utilidades de interfaz ─────────
const PAL = ['#17643F', '#1E5A3E', '#8A6D3B', '#2F6F5E', '#46664F', '#6B5A2E', '#24543F', '#5B7351'];
const colorOf = id => { let h = 0; for (const c of String(id)) h = (h * 31 + c.charCodeAt(0)) >>> 0; return PAL[h % PAL.length]; };
const ini = n => String(n || '?').trim().split(/\s+/).slice(0, 2).map(w => w[0]).join('').toUpperCase();
const av = (p, size = 's') => { const u = p && (p._fotoLocal || (p.foto && FOTO.get(p.foto)));
  return `<span class="av ${size}" style="background:${colorOf(p && p.user_id)}" aria-hidden="true">${u ? `<img src="${esc(u)}" alt="" loading="lazy" decoding="async">` : esc(ini(p && p.nombre))}</span>`; };

// Foto: se recorta a un cuadrado de 512 px y se vuelve a codificar en el navegador (fuera EXIF y ubicación).
async function prepararFoto(file) {
  if (!file || !/^image\//.test(file.type || 'image/')) throw new Error('foto: no es una imagen');
  if (file.size > 25e6) throw new Error('foto: demasiado grande');
  let bmp;
  try { bmp = await createImageBitmap(file, { imageOrientation: 'from-image' }); }
  catch (e) { bmp = await new Promise((ok, ko) => { const i = new Image(); i.onload = () => ok(i); i.onerror = () => ko(new Error('foto: formato')); i.src = URL.createObjectURL(file); }); }
  const w = bmp.width, h = bmp.height, s = Math.min(w, h), N = Math.min(512, s);
  const cv = document.createElement('canvas'); cv.width = cv.height = N;
  cv.getContext('2d').drawImage(bmp, (w - s) / 2, (h - s) / 2, s, s, 0, 0, N, N);
  const toB = (t, qy) => new Promise(ok => cv.toBlob(ok, t, qy));
  let b = await toB('image/webp', .86);
  if (!b || b.type !== 'image/webp') b = await toB('image/jpeg', .86);
  if (!b || b.size > 400000) b = await toB('image/jpeg', .7);
  if (!b) throw new Error('foto: formato');
  return b;
}
async function borrarFotos(keep) {
  try { const { data } = await SB.storage.from('avatares').list(ME.id, { limit: 50 }); const rm = (data || []).map(o => ME.id + '/' + o.name).filter(n => n !== keep); if (rm.length) await SB.storage.from('avatares').remove(rm); } catch (e) { }
}
const hcpTxt = h => h == null || h === '' ? '—' : String(Number(h).toFixed(1)).replace('.', ',');
const hcpRange = p => p.hcp_min == null && p.hcp_max == null ? 'Cualquiera' : p.hcp_min != null && p.hcp_max != null ? hcpTxt(p.hcp_min) + ' – ' + hcpTxt(p.hcp_max) : p.hcp_min != null ? 'Desde ' + hcpTxt(p.hcp_min) : 'Hasta ' + hcpTxt(p.hcp_max);
const seats = (n, on) => `<span class="seats" aria-label="${on} de ${n} plazas ocupadas">${Array.from({ length: n }, (_, i) => `<i class="${i < on ? 'on' : ''}"></i>`).join('')}<em>${on >= n ? 'Completa' : (n - on) + (n - on === 1 ? ' libre' : ' libres')}</em></span>`;
const dateBox = (f, h) => `<div class="date"><small>${esc(dow(f))}</small><b>${D(f).getDate()}</b><span>${esc(mon(f))}${h ? ' · ' + esc(hhmm(h)) : ''}</span></div>`;
const I = {
  share: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v12M7 8l5-5 5 5"/><path d="M5 13v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6"/></svg>',
  wa: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.6.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>',
  mail: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
  lock: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/></svg>',
  back: '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>',
  plus: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>',
  check: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
};
let tT = 0;
function toast(m) { const t = $('#toast'); t.textContent = m; t.classList.add('on'); clearTimeout(tT); tT = setTimeout(() => t.classList.remove('on'), 2800); }
function openSheet(html, after) {
  $('#sheetBody').innerHTML = html; const s = $('#sheet'); s.classList.add('on'); document.body.style.overflow = 'hidden';
  const f = s.querySelector('input,textarea,select,button'); if (f) setTimeout(() => f.focus(), 60);
  if (after) after(s);
}
function closeSheet() { $('#sheet').classList.remove('on'); document.body.style.overflow = ''; }
$('#sheet').addEventListener('click', e => { if (e.target.id === 'sheet' || e.target.closest('[data-close]')) closeSheet(); });
addEventListener('keydown', e => { if (e.key === 'Escape') closeSheet(); });
function errMsg(e) {
  const m = String((e && (e.message || e.error_description)) || e || '');
  if (/limite/.test(m)) return 'Has llegado al límite de hoy. Prueba mañana.';
  if (/edad/.test(m)) return 'Hay que tener al menos 16 años para usar Banderín Social.';
  if (/plazas/.test(m)) return 'La partida ya está completa.';
  if (/fecha/.test(m)) return 'La fecha tiene que estar entre hoy y dentro de 6 meses.';
  if (/hcp/.test(m)) return 'El hándicap mínimo no puede ser mayor que el máximo.';
  if (/^perfil:/.test(m)) return 'Primero crea tu perfil de jugador.';
  if (/foto/i.test(m)) return /^No se/.test(m) ? m : 'No se ha podido guardar la foto. Prueba con otra.';
  if (/permission denied|row-level security/i.test(m)) return 'No se ha podido guardar. Recarga la página e inténtalo de nuevo; si sigue, escríbenos.';
  if (/whatsapp/.test(m)) return 'El número de WhatsApp no parece válido.';
  if (/email/.test(m)) return 'El correo no parece válido.';
  if (/duplicate|unique/.test(m)) return 'Eso ya está hecho.';
  if (/Invalid login/.test(m)) return 'Correo o contraseña incorrectos.';
  if (/Email not confirmed/.test(m)) return 'Confirma tu correo antes de entrar (revisa la bandeja de entrada).';
  return 'No se ha podido completar. Inténtalo de nuevo.';
}
const isMissing = e => e && (/PGRST20[25]|42P01|42883|does not exist|Could not find/.test((e.code || '') + ' ' + (e.message || '')));
function needReal(msg) {
  if (!DEMO) return false;
  if (NOSQL) toast('La base de datos de Social aún no está preparada.');
  else openLogin(msg || 'Entra con tu cuenta de Banderín para hacerlo de verdad.');
  return true;
}

// ───────── Datos de ejemplo (vista previa) ─────────
const DEMOD = (() => {
  const clubsBy = p => [...CLUBS].filter(([k, v]) => v === p && k.length <= 30 && !/\bS\.? ?A\.?$|S\.L\.?$/i.test(k) && /golf|club/i.test(k)).map(([k]) => k);
  const mad = clubsBy('Madrid'), mal = clubsBy('Málaga'), bcn = clubsBy('Barcelona');
  const c = (arr, i, f) => arr[i % (arr.length || 1)] || f;
  const U = [
    { user_id: 'd1', nombre: 'Lucía Martín', hcp: 14.2, provincia: 'Madrid', campos: [c(mad, 0, 'Club de Campo Villa de Madrid'), c(mad, 3, 'Golf Olivar de la Hinojosa')], visible: true, bio: 'Juego los sábados por la mañana. Me encantan los scrambles y los torneos benéficos.' },
    { user_id: 'd2', nombre: 'Javier Ruiz', hcp: 22.5, provincia: 'Madrid', campos: [c(mad, 1, 'Golf Park')], bio: 'Empecé hace dos años. Busco gente con paciencia y buen humor.' },
    { user_id: 'd3', nombre: 'Marta Pons', hcp: 8.1, provincia: 'Barcelona', campos: [c(bcn, 0, 'Real Club de Golf El Prat')], bio: 'Competición amateur. Siempre con ganas de un fourball.' },
    { user_id: 'd4', nombre: 'Íñigo Sáez', hcp: 31.0, provincia: 'Málaga', campos: [c(mal, 0, 'Golf Torrequebrada')], bio: 'Recién llegado a la Costa del Sol. ¿Alguien para una partida entre semana?' },
    { user_id: 'd5', nombre: 'Carmen López', hcp: 17.8, provincia: 'Madrid', campos: [c(mad, 2, 'La Herrería')], bio: '' },
    { user_id: 'd6', nombre: 'Pablo Gil', hcp: 11.4, provincia: 'Málaga', campos: [c(mal, 2, 'Los Naranjos')], bio: 'Hándicap bajando. Torneos por parejas siempre.' },
  ];
  const par = PAREJAS[0];
  const P = [
    { id: 'p1', autor: 'd1', campo: c(mad, 0, 'Club de Campo Villa de Madrid'), provincia: 'Madrid', fecha: weekend()[0], hora: '09:30:00', tipo: 'partida', plazas: 3, hcp_min: 10, hcp_max: 28, precio: 85, nota: 'Partida tranquila de 18 hoyos. Salimos a las 9:30 y después caña en el bar del club.', solo_amigos: false, cerrada: false, ok: 1 },
    par ? { id: 'p2', autor: 'd6', campo: par.club, provincia: par.prov, fecha: par.s, hora: null, tipo: 'torneo', torneo: par.n, torneo_url: safeUrl(par.url), plazas: 1, hcp_min: null, hcp_max: 24, precio: 60, nota: 'Busco pareja para este torneo. Me da igual el hándicap si te lo tomas con ganas.', solo_amigos: false, cerrada: false, ok: 0 } : null,
    { id: 'p3', autor: 'd2', campo: c(mad, 1, 'Golf Park'), provincia: 'Madrid', fecha: addDays(3), hora: '17:00:00', tipo: 'partida', plazas: 2, hcp_min: 18, hcp_max: 36, precio: 25, nota: 'Nueve hoyos al salir del trabajo. Nivel principiante, sin presión.', solo_amigos: false, cerrada: false, ok: 1 },
    { id: 'p4', autor: 'd3', campo: c(bcn, 0, 'Real Club de Golf El Prat'), provincia: 'Barcelona', fecha: addDays(9), hora: '08:40:00', tipo: 'partida', plazas: 3, hcp_min: null, hcp_max: 15, precio: 110, nota: 'Fourball con apuesta amistosa. Hándicap hasta 15.', solo_amigos: false, cerrada: false, ok: 2 },
    { id: 'p5', autor: 'd4', campo: c(mal, 0, 'Golf Torrequebrada'), provincia: 'Málaga', fecha: addDays(5), hora: '10:00:00', tipo: 'partida', plazas: 2, hcp_min: null, hcp_max: null, precio: 70, nota: 'Cualquier nivel. Yo pongo el buen rollo.', solo_amigos: false, cerrada: false, ok: 0 },
  ].filter(Boolean);
  return { U, P };
})();
const demoP = id => DEMOD.U.find(u => u.user_id === id);

// ───────── Acceso a datos ─────────
const PCOLS = 'user_id,nombre,hcp,provincia,campos,bio,visible,creado,foto';
// Fotos de perfil: almacén privado, enlaces firmados que caducan en 2 h (se renuevan al recargar).
const FOTO = new Map();
async function firmar(rows) {
  const paths = [...new Set((rows || []).map(r => r && r.foto).filter(f => f && !FOTO.has(f)))];
  if (!paths.length || !SB) return rows;
  try { const { data } = await SB.storage.from('avatares').createSignedUrls(paths, 7200); (data || []).forEach(d => { if (d && d.signedUrl) FOTO.set(d.path, d.signedUrl); }); } catch (e) { }
  return rows;
}
const MCOLS = 'id,autor,campo,provincia,fecha,hora,tipo,torneo,torneo_url,plazas,hcp_min,hcp_max,nota,solo_amigos,cerrada,creado,precio';
// Precio por jugador (green fee o inscripción). 0 = no cuesta nada; vacío en partidas antiguas.
const precioTxt = p => p.precio == null ? '' : +p.precio === 0 ? 'Sin coste' : p.precio + ' € / jugador';
async function q(p) { const { data, error } = await p; if (error) throw error; return data; }
async function perfilesDe(ids) {
  ids = [...new Set(ids.filter(Boolean))]; if (!ids.length) return new Map();
  const rows = await firmar(await q(SB.from('social_perfiles').select(PCOLS).in('user_id', ids)));
  return new Map(rows.map(r => [r.user_id, r]));
}
async function partidas() {
  if (DEMO) return DEMOD.P.map(p => ({ ...p, autorP: demoP(p.autor), ocupadas: p.ok, mia: false, yo: null }));
  const rows = await q(SB.from('social_partidas').select(MCOLS).gte('fecha', TODAY).order('fecha').order('hora', { nullsFirst: true }).limit(200));
  const ids = rows.map(r => r.id);
  const sol = ids.length ? await q(SB.from('social_solicitudes').select('partida,jugador,estado').in('partida', ids)) : [];
  const prof = await perfilesDe(rows.map(r => r.autor));
  return rows.filter(r => prof.has(r.autor)).map(r => ({ ...r, autorP: prof.get(r.autor),
    ocupadas: sol.filter(s => s.partida === r.id && s.estado === 'aceptada').length,
    pendientes: sol.filter(s => s.partida === r.id && s.estado === 'pendiente').length,
    mia: ME && r.autor === ME.id, yo: ME ? (sol.find(s => s.partida === r.id && s.jugador === ME.id) || null) : null }));
}
async function partida(id) {
  if (DEMO) {
    const p = DEMOD.P.find(x => x.id === id); if (!p) return null;
    const acc = DEMOD.U.filter(u => u.user_id !== p.autor).slice(0, p.ok);
    return { ...p, autorP: demoP(p.autor), ocupadas: p.ok, sol: acc.map(u => ({ jugador: u.user_id, estado: 'aceptada', p: u })), contactos: new Map(), yo: null, mia: false };
  }
  const p = (await q(SB.from('social_partidas').select(MCOLS).eq('id', id).limit(1)))[0]; if (!p) return null;
  const sol = await q(SB.from('social_solicitudes').select('partida,jugador,mensaje,estado,creado').eq('partida', id).order('creado'));
  const prof = await perfilesDe([p.autor, ...sol.map(s => s.jugador)]);
  const cids = [p.autor, ...sol.filter(s => s.estado === 'aceptada').map(s => s.jugador)].filter(x => x !== ME.id);
  const cont = cids.length ? await q(SB.from('social_contacto').select('user_id,whatsapp,email').in('user_id', cids)) : [];
  return { ...p, autorP: prof.get(p.autor), sol: sol.map(s => ({ ...s, p: prof.get(s.jugador) })).filter(s => s.p),
    ocupadas: sol.filter(s => s.estado === 'aceptada').length, contactos: new Map(cont.map(c => [c.user_id, c])),
    mia: p.autor === ME.id, yo: sol.find(s => s.jugador === ME.id) || null };
}
async function jugadores(f) {
  if (DEMO) return DEMOD.U;
  let qq = SB.from('social_perfiles').select(PCOLS).eq('visible', true).neq('user_id', ME.id).order('actualizado', { ascending: false }).limit(100);
  if (f.prov) qq = qq.eq('provincia', f.prov);
  if (f.nombre) qq = qq.ilike('nombre', '%' + f.nombre.replace(/[%_,()]/g, '') + '%');
  return firmar(await q(qq));
}
async function amistades() {
  if (DEMO) return { amigos: DEMOD.U.slice(0, 2), recibidas: [DEMOD.U[3]], enviadas: [] };
  const rows = await q(SB.from('social_amistades').select('de,para,estado,creado'));
  const other = r => r.de === ME.id ? r.para : r.de;
  const prof = await perfilesDe(rows.map(other));
  const pick = f => rows.filter(f).map(r => prof.get(other(r))).filter(Boolean);
  return { rows, amigos: pick(r => r.estado === 'aceptada'), recibidas: pick(r => r.estado === 'pendiente' && r.para === ME.id), enviadas: pick(r => r.estado === 'pendiente' && r.de === ME.id) };
}
async function jugador(id) {
  if (DEMO) { const p = demoP(id); return p && { p, c: null, rel: 'nada', partidas: DEMOD.P.filter(x => x.autor === id) }; }
  const p = (await firmar(await q(SB.from('social_perfiles').select(PCOLS).eq('user_id', id).limit(1))))[0]; if (!p) return null;
  const c = (await q(SB.from('social_contacto').select('user_id,whatsapp,email,publico').eq('user_id', id).limit(1)))[0] || null;
  const am = id === ME.id ? [] : await q(SB.from('social_amistades').select('de,para,estado').or(`and(de.eq.${ME.id},para.eq.${id}),and(de.eq.${id},para.eq.${ME.id})`));
  const a = am[0]; const rel = !a ? 'nada' : a.estado === 'aceptada' ? 'amigos' : a.de === ME.id ? 'enviada' : 'recibida';
  const ps = await q(SB.from('social_partidas').select(MCOLS).eq('autor', id).gte('fecha', TODAY).order('fecha').limit(10));
  return { p, c, rel, partidas: ps };
}
async function estado() {
  EST = null; MYP = null; MYC = null;
  if (!ME) return;
  const { data, error } = await SB.rpc('social_mi_estado');
  if (error) { if (isMissing(error)) { NOSQL = true; return; } throw error; }
  NOSQL = false; EST = data;
  if (EST.perfil) {
    MYP = (await firmar(await q(SB.from('social_perfiles').select(PCOLS).eq('user_id', ME.id).limit(1))))[0] || null;
    MYC = (await q(SB.from('social_contacto').select('user_id,whatsapp,email,publico').eq('user_id', ME.id).limit(1)))[0] || null;
  }
}
async function badges() {
  const dj = $('#dotJ'), dm = $('#dotM'); dj.hidden = dm.hidden = true;
  if (DEMO || !ME || NOSQL) return;
  try {
    const r = await q(SB.from('social_amistades').select('de').eq('para', ME.id).eq('estado', 'pendiente'));
    if (r.length) { dj.hidden = false; dj.textContent = r.length; }
    const mine = await q(SB.from('social_partidas').select('id').eq('autor', ME.id).gte('fecha', TODAY));
    if (mine.length) {
      const s = await q(SB.from('social_solicitudes').select('partida').in('partida', mine.map(m => m.id)).eq('estado', 'pendiente'));
      if (s.length) { dm.hidden = false; dm.textContent = s.length; }
    }
  } catch (e) { /* sin avisos */ }
}

// ───────── Cabecera ─────────
function chrome() { document.body.classList.toggle('logged', !!ME); }
document.addEventListener('click', e => { if (e.target.closest('[data-login]')) { e.preventDefault(); openLogin(); } });
{ const th = $('#theme'); if (th) th.onclick = () => { const r = document.documentElement, dark = r.dataset.theme ? r.dataset.theme === 'dark' : matchMedia('(prefers-color-scheme:dark)').matches; r.dataset.theme = dark ? 'light' : 'dark';
  try { if (localStorage.getItem('banderin.tema') !== null) localStorage.setItem('banderin.tema', JSON.stringify(r.dataset.theme)); } catch (e) { } }; }

// ───────── Entrar ─────────
function openLogin(msg) {
  openSheet(`<h2 id="sheetT">Entra en Banderín</h2><p class="sub">${esc(msg || 'Usa la misma cuenta que en banderin.es.')}</p>
  <form id="lf"><label class="field"><span>Correo</span><input class="in" type="email" name="e" autocomplete="email" required></label>
  <label class="field"><span>Contraseña</span><input class="in" type="password" name="p" autocomplete="current-password" required minlength="6"></label>
  <p class="err" id="lerr" hidden></p><button class="btn primary block" type="submit">Entrar</button></form>
  <div class="more smore"><a href="https://banderin.es/#perfil" target="_blank" rel="noopener">Crear una cuenta</a><a href="https://banderin.es/#perfil" target="_blank" rel="noopener">He olvidado la contraseña</a></div>`, s => {
    s.querySelector('#lf').addEventListener('submit', async e => {
      e.preventDefault(); const f = e.target, btn = f.querySelector('button'); btn.disabled = true;
      const tk = window.botToken ? await window.botToken() : '';
      const { error } = await SB.auth.signInWithPassword({ email: f.e.value.trim(), password: f.p.value, options: tk ? { captchaToken: tk } : {} });
      btn.disabled = false;
      if (error) { const er = s.querySelector('#lerr'); er.hidden = false; er.textContent = errMsg(error); return; }
      closeSheet();
    });
  });
}

// ───────── Vistas ─────────
function setTab(t) { document.querySelectorAll('.subnav a').forEach(a => { const on = a.dataset.tab === t; a.classList.toggle('on', on); if (on) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current'); }); const f = $('#fab'); if (f) f.hidden = !ME || NOSQL || !MYP || t === 'publicar' || t === 'perfil' || /^#(partida|jugador)\//.test(location.hash); }
const skel = n => '<div class="list" aria-busy="true">' + '<div class="skel"></div>'.repeat(n) + '</div>';
const backBtn = () => `<button class="back" data-back>${I.back}Volver</button>`;
document.addEventListener('click', e => { if (e.target.closest('[data-back]')) { e.preventDefault(); history.length > 1 ? history.back() : (location.hash = '#partidas'); } });

function matchCard(p) {
  const a = p.autorP || {}, n = p.plazas, on = Math.min(p.ocupadas || 0, n);
  const st = p.mia ? `<span class="tag gold">Tuya${p.pendientes ? ' · ' + p.pendientes + ' solicitud' + (p.pendientes > 1 ? 'es' : '') : ''}</span>` :
    p.yo ? (p.yo.estado === 'aceptada' ? '<span class="tag">Estás dentro</span>' : p.yo.estado === 'pendiente' ? '<span class="tag mute">Solicitud enviada</span>' : '') : '';
  return `<a class="match glass" href="#partida/${esc(p.id)}">${dateBox(p.fecha, p.hora)}<div>
    <div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin-bottom:4px">${p.tipo === 'torneo' ? '<span class="tag gold">Busca pareja · Torneo</span>' : '<span class="tag">Partida</span>'}${p.solo_amigos ? '<span class="tag mute">Solo amigos</span>' : ''}${st}</div>
    <h3>${esc(p.tipo === 'torneo' && p.torneo ? p.torneo : p.campo)}</h3>
    <div class="meta"><span>${esc(p.tipo === 'torneo' ? p.campo : (p.provincia || ''))}</span><span>Hándicap: ${esc(hcpRange(p))}</span>${p.precio != null ? `<span>${esc(precioTxt(p))}</span>` : ''}</div>
    <div class="foot"><span class="who">${av(a)}<span>${esc(a.nombre || '')}</span><span class="hcp" style="font-weight:600;color:var(--muted)">${hcpTxt(a.hcp)}</span></span>${seats(n, on)}</div></div></a>`;
}

async function vPartidas() {
  setTab('partidas');
  const nombre = MYP ? MYP.nombre.split(' ')[0] : '';
  view.innerHTML = `<section class="shero"><p class="eb">Banderín Social</p><h1>${nombre ? 'Hola, ' + esc(nombre) + '.<br>' : ''}¿Con quién juegas?</h1>
    <p>Únete a una partida, busca pareja para un torneo o publica la tuya y deja que te encuentren.</p>
    <div class="acts"><a class="btn gold" href="#publicar">${I.plus}Publicar partida</a><a class="btn ghost" href="#jugadores">Ver jugadores</a></div></section>
    ${PAREJAS.length ? `<div class="sec"><h2>Torneos por parejas</h2><a href="https://banderin.es/#lista" target="_blank" rel="noopener">Ver todos</a></div>
    <p class="lede">¿Te falta pareja? Publícalo y que te encuentren.</p>
    <div class="rail">${PAREJAS.slice(0, 10).map((t, i) => `<div class="tcard glass"><span class="tag gold" style="align-self:flex-start">${esc(when(t.s))}</span><h4>${esc(t.n)}</h4><p>${esc(t.club)} · ${esc(t.prov)}</p><a class="btn soft sm" href="#publicar/t/${esc(tid(t))}">Busco pareja</a></div>`).join('')}</div>` : ''}
    <div class="sec"><h2>Partidas abiertas</h2></div>
    <div class="filters" role="group" aria-label="Filtros">
      <select class="pill" id="fprov" aria-label="Provincia"><option value="">Toda España</option>${PROVS.map(p => `<option${FIL.prov === p ? ' selected' : ''}>${esc(p)}</option>`).join('')}</select>
      <button class="pill" data-c="finde" aria-pressed="${FIL.cuando === 'finde'}">Este finde</button>
      <button class="pill" data-c="semana" aria-pressed="${FIL.cuando === 'semana'}">7 días</button>
      <button class="pill" data-t="torneo" aria-pressed="${FIL.tipo === 'torneo'}">Busca pareja</button>
      ${MYP && MYP.hcp != null ? `<button class="pill" data-h aria-pressed="${FIL.hcp}">Mi hándicap</button>` : ''}
    </div><div id="ml">${skel(3)}</div>`;
  view.querySelector('#fprov').onchange = e => { FIL.prov = e.target.value; draw(); };
  view.querySelectorAll('[data-c]').forEach(b => b.onclick = () => { FIL.cuando = FIL.cuando === b.dataset.c ? 'todas' : b.dataset.c; vPartidas(); });
  view.querySelectorAll('[data-t]').forEach(b => b.onclick = () => { FIL.tipo = FIL.tipo ? '' : 'torneo'; vPartidas(); });
  view.querySelectorAll('[data-h]').forEach(b => b.onclick = () => { FIL.hcp = !FIL.hcp; vPartidas(); });
  let all = [];
  try { all = await partidas(); } catch (e) { $('#ml').innerHTML = `<div class="empty"><b>No se han podido cargar las partidas.</b>${esc(errMsg(e))}</div>`; return; }
  function draw() {
    const [s, d] = weekend(), wk = addDays(7);
    const L = all.filter(p => (!FIL.prov || p.provincia === FIL.prov) && (FIL.cuando !== 'finde' || (p.fecha >= s && p.fecha <= d)) && (FIL.cuando !== 'semana' || p.fecha <= wk)
      && (!FIL.tipo || p.tipo === FIL.tipo) && (!FIL.hcp || !MYP || ((p.hcp_min == null || MYP.hcp >= p.hcp_min) && (p.hcp_max == null || MYP.hcp <= p.hcp_max))) && !p.cerrada);
    $('#ml').innerHTML = L.length ? '<div class="list">' + L.map(matchCard).join('') + '</div>' :
      `<div class="empty glass panel"><b>${all.length ? 'Ninguna partida con estos filtros.' : 'Todavía no hay partidas.'}</b>${all.length ? 'Prueba a quitar alguno.' : 'Sé el primero: publica una y compártela con tus amigos.'}<br><a class="btn primary" href="#publicar">${I.plus}Publicar partida</a></div>`;
  }
  draw();
}

async function vPartida(id) {
  setTab('partidas');
  view.innerHTML = backBtn() + skel(2);
  let p; try { p = await partida(id); } catch (e) { view.innerHTML = backBtn() + `<div class="empty"><b>No se ha podido cargar.</b>${esc(errMsg(e))}</div>`; return; }
  if (!p && DEMO && !NOSQL) { view.innerHTML = backBtn() + `<div class="empty glass panel"><b>Entra para ver esta partida.</b>Las partidas solo las ven los jugadores con cuenta de Banderín.<br><button class="btn primary" data-login>Entrar</button></div>`; return; }
  if (!p) { view.innerHTML = backBtn() + `<div class="empty glass panel"><b>Esta partida ya no existe.</b>Puede que la hayan borrado o que no tengas acceso.<br><a class="btn primary" href="#partidas">Ver partidas</a></div>`; return; }
  const a = p.autorP || {}, n = p.plazas, on = Math.min(p.ocupadas, n), full = on >= n;
  const acc = p.sol.filter(s => s.estado === 'aceptada'), pend = p.sol.filter(s => s.estado === 'pendiente');
  const contactBtns = (c) => c && (c.whatsapp || c.email) ? `<div class="contact">${c.whatsapp ? `<a class="btn primary sm" href="https://wa.me/${esc(waNum(c.whatsapp))}" target="_blank" rel="noopener">${I.wa}WhatsApp</a>` : ''}${c.email ? `<a class="btn soft sm" href="mailto:${esc(c.email)}">${I.mail}Correo</a>` : ''}</div>` : '';
  const pRow = (s, extra = '') => `<div class="row">${av(s.p, 'm')}<a class="grow" href="#jugador/${esc(s.jugador)}"><b>${esc(s.p.nombre)}</b><span>Hándicap ${hcpTxt(s.p.hcp)}${s.p.provincia ? ' · ' + esc(s.p.provincia) : ''}</span>${s.mensaje && s.estado === 'pendiente' ? `<span style="display:block;color:var(--ink);margin-top:2px">“${esc(s.mensaje)}”</span>` : ''}</a>${extra}</div>`;
  let cta = '';
  if (p.mia) cta = `<button class="btn ghost" data-share>${I.share}Compartir</button><button class="btn ${p.cerrada ? 'primary' : 'soft'}" data-close-m>${p.cerrada ? 'Reabrir' : 'Cerrar partida'}</button>`;
  else if (!p.yo) cta = `<button class="btn ghost" data-share aria-label="Compartir">${I.share}</button><button class="btn primary" data-join ${full || p.cerrada ? 'disabled' : ''}>${full ? 'Partida completa' : p.cerrada ? 'Cerrada' : p.tipo === 'torneo' ? 'Quiero ser tu pareja' : 'Pedir unirme'}</button>`;
  else if (p.yo.estado === 'pendiente') cta = `<button class="btn ghost" data-leave>Retirar solicitud</button><button class="btn soft" disabled>Solicitud enviada</button>`;
  else if (p.yo.estado === 'aceptada') cta = `<button class="btn ghost" data-leave>Salir</button><button class="btn primary" disabled>${I.check}Estás dentro</button>`;
  else cta = `<button class="btn soft" disabled>Esta vez no hay hueco</button>`;
  const yoDentro = p.yo && p.yo.estado === 'aceptada';
  view.innerHTML = backBtn() + `
  <div class="dhead">${dateBox(p.fecha, p.hora)}<div>${p.tipo === 'torneo' ? '<span class="tag gold">Busca pareja · Torneo</span>' : '<span class="tag">Partida</span>'}
    <h1 style="margin-top:6px">${esc(p.tipo === 'torneo' && p.torneo ? p.torneo : p.campo)}</h1>
    <div class="meta" style="color:var(--muted);font-size:14px;margin-top:4px">${esc(when(p.fecha))}${p.hora ? ' · ' + esc(hhmm(p.hora)) : ''}${p.tipo === 'torneo' ? ' · ' + esc(p.campo) : ''}</div></div></div>
  <div class="facts"><div><small>Plazas</small>${seats(n, on)}</div><div><small>Precio</small><b>${esc(precioTxt(p) || 'Sin indicar')}</b></div>
    <div><small>Hándicap</small><b>${esc(hcpRange(p))}</b></div><div><small>Dónde</small><b>${esc(whereOf(p.campo) || p.provincia || '—')}</b></div></div>
  ${p.solo_amigos ? '<p class="lock" style="margin:-6px 0 12px">' + I.lock + 'Solo la ven tus amigos.</p>' : ''}
  <a class="btn ghost block" style="margin-bottom:8px" href="${esc(mapsUrl(p.campo))}" target="_blank" rel="noopener">Cómo llegar a ${esc(p.campo)}</a>
  ${p.torneo_url ? `<a class="btn ghost block" href="${esc(safeUrl(p.torneo_url))}" target="_blank" rel="noopener">Ver el torneo y la inscripción</a>` : ''}
  ${p.nota ? `<p class="note">${esc(p.nota)}</p>` : ''}
  <div class="panel glass" style="margin-top:14px"><div class="row">${av(a, 'm')}<a class="grow" href="#jugador/${esc(p.autor)}"><b>${esc(a.nombre || '')}</b><span>Organiza · Hándicap ${hcpTxt(a.hcp)}</span></a>${p.mia ? '<span class="tag gold">Tú</span>' : ''}</div>
    ${!p.mia && yoDentro ? contactBtns(p.contactos.get(p.autor)) || '<p class="lock">' + I.lock + 'No ha añadido contacto. Escríbele desde su perfil cuando seáis amigos.</p>' : ''}
    ${acc.map(s => pRow(s)).join('')}
    ${p.mia && acc.length ? acc.map(s => contactBtns(p.contactos.get(s.jugador)) ? `<div style="margin:6px 0 4px 56px">${contactBtns(p.contactos.get(s.jugador))}</div>` : '').join('') : ''}
    ${!acc.length ? `<p class="lede" style="margin:8px 0 0">Aún no se ha unido nadie.</p>` : ''}</div>
  ${p.mia || yoDentro ? `<div class="sec"><h2>Chat de la partida</h2></div><div class="panel glass chat"><div class="msgs" id="msgs" aria-live="polite"><p class="lede" style="margin:0">Cargando…</p></div><form id="cf" class="cform"><input class="in" id="ct" maxlength="500" placeholder="Escribe un mensaje" autocomplete="off" aria-label="Mensaje"><button class="btn primary" type="submit" aria-label="Enviar">Enviar</button></form><p class="lede" style="margin:8px 0 0;font-size:12px">Solo lo leéis quien organiza y los jugadores aceptados.</p></div>` : `<p class="lock" style="margin:14px 4px 0;color:var(--on-page-m)">${I.lock}<span>El chat de la partida se abre cuando te aceptan.</span></p>`}
  ${p.mia ? `<div class="sec"><h2>Solicitudes${pend.length ? ' <span class="dot">' + pend.length + '</span>' : ''}</h2></div>
    <div class="panel glass">${pend.length ? pend.map(s => pRow(s, `<div style="display:flex;gap:6px"><button class="btn soft sm" data-rej="${esc(s.jugador)}">No</button><button class="btn primary sm" data-acc="${esc(s.jugador)}" ${full ? 'disabled' : ''}>Aceptar</button></div>`)).join('') : '<p class="lede" style="margin:0">Cuando alguien pida unirse, aparecerá aquí. Comparte la partida para que te encuentren.</p>'}</div>` : ''}
  <div class="cta glass">${cta}</div>
  <div class="more smore">${p.mia ? '<button data-del>Borrar partida</button>' : `<button data-report>Denunciar</button><button data-block>Bloquear a ${esc((a.nombre || '').split(' ')[0])}</button>`}</div>`;
  const reload = () => vPartida(id);
  if (p.mia || yoDentro) {
    const names = new Map([[p.autor, a], ...p.sol.map(x => [x.jugador, x.p])]); let last = 0, first = true;
    const box = view.querySelector('#msgs');
    const pull = async () => {
      if (!document.body.contains(box)) { clearInterval(CHAT); return; }
      let rows; try { rows = await q(SB.from('social_mensajes').select('id,autor,texto,creado').eq('partida', p.id).gt('id', last).order('id').limit(200)); } catch (e) { if (first) box.innerHTML = '<p class="lede" style="margin:0">El chat no está disponible todavía.</p>'; return; }
      if (first) { box.innerHTML = rows.length ? '' : '<p class="lede" id="nomsg" style="margin:0">Aún no hay mensajes. Rompe el hielo: hora, punto de encuentro, buggy…</p>'; first = false; }
      if (!rows.length) return;
      const nm = box.querySelector('#nomsg'); if (nm) nm.remove();
      box.insertAdjacentHTML('beforeend', rows.map(m => { const me = m.autor === ME.id, w = names.get(m.autor) || {}; const d = new Date(m.creado);
        return `<div class="msg${me ? ' me' : ''}">${me ? '' : `<b>${esc((w.nombre || 'Jugador').split(' ')[0])}</b>`}<span>${esc(m.texto)}</span><time>${isNaN(d) ? '' : pad(d.getHours()) + ':' + pad(d.getMinutes())}</time></div>`; }).join(''));
      last = rows[rows.length - 1].id; box.scrollTop = box.scrollHeight;
    };
    clearInterval(CHAT); pull(); CHAT = setInterval(() => { if (!document.hidden) pull(); }, 7000);
    view.querySelector('#cf').onsubmit = async e => { e.preventDefault(); const i = view.querySelector('#ct'), txt = i.value.trim(); if (!txt) return; i.value = '';
      try { await q(SB.from('social_mensajes').insert({ partida: p.id, texto: txt })); pull(); } catch (er) { i.value = txt; toast(errMsg(er)); } };
  }
  view.querySelectorAll('[data-share]').forEach(b => b.onclick = () => share(`${p.tipo === 'torneo' ? 'Busco pareja: ' + (p.torneo || p.campo) : 'Partida en ' + p.campo} · ${when(p.fecha)}`, location.origin + '/social/#partida/' + p.id));
  const on1 = (sel, fn) => { const b = view.querySelector(sel); if (b) b.onclick = fn; };
  on1('[data-join]', () => { if (needReal()) return; if (!MYP) return askProfile();
    openSheet(`<h2 id="sheetT">${p.tipo === 'torneo' ? 'Ofrécete como pareja' : 'Pedir unirme'}</h2><p class="sub">${esc(a.nombre)} verá tu nombre y tu hándicap, y decidirá. Tu contacto solo se comparte si te acepta.</p>
      <label class="field"><span>Mensaje (opcional)</span><textarea class="in" id="jm" maxlength="200" placeholder="Hola, juego los sábados y tengo hándicap ${hcpTxt(MYP.hcp)}…"></textarea></label>
      <button class="btn primary block" id="jgo">Enviar solicitud</button>`, s => s.querySelector('#jgo').onclick = async () => {
        try { await q(SB.from('social_solicitudes').insert({ partida: p.id, jugador: ME.id, mensaje: s.querySelector('#jm').value.trim() || null })); closeSheet(); toast('Solicitud enviada'); reload(); } catch (e) { toast(errMsg(e)); } }); });
  on1('[data-leave]', async () => { if (needReal()) return; try { await q(SB.from('social_solicitudes').delete().eq('partida', p.id).eq('jugador', ME.id)); toast('Hecho'); reload(); } catch (e) { toast(errMsg(e)); } });
  view.querySelectorAll('[data-acc],[data-rej]').forEach(b => b.onclick = async () => {
    const acc = !!b.dataset.acc, j = b.dataset.acc || b.dataset.rej;
    try { await q(SB.from('social_solicitudes').update({ estado: acc ? 'aceptada' : 'rechazada' }).eq('partida', p.id).eq('jugador', j)); toast(acc ? '¡Aceptado! Ya podéis contactar.' : 'Rechazada'); reload(); badges(); } catch (e) { toast(errMsg(e)); } });
  on1('[data-close-m]', async () => { try { await q(SB.from('social_partidas').update({ cerrada: !p.cerrada }).eq('id', p.id)); reload(); } catch (e) { toast(errMsg(e)); } });
  on1('[data-del]', () => confirmSheet('¿Borrar la partida?', 'Se borran también las solicitudes. No se puede deshacer.', 'Borrar', async () => {
    try { await q(SB.from('social_partidas').delete().eq('id', p.id)); toast('Partida borrada'); location.hash = '#mias'; } catch (e) { toast(errMsg(e)); } }));
  on1('[data-report]', () => report(p.autor, p.id));
  on1('[data-block]', () => block(p.autor, a.nombre));
}
const waNum = w => { let d = String(w).replace(/\D/g, ''); if (d.length === 9) d = '34' + d; return d; };
async function share(text, url) {
  try { if (navigator.share) { await navigator.share({ title: 'Banderín Social', text, url }); return; } } catch (e) { if (e && e.name === 'AbortError') return; }
  try { await navigator.clipboard.writeText(text + ' ' + url); toast('Enlace copiado'); } catch (e) { location.href = 'https://wa.me/?text=' + encodeURIComponent(text + ' ' + url); }
}
function confirmSheet(t, sub, ok, fn, danger = true) {
  openSheet(`<h2 id="sheetT">${esc(t)}</h2><p class="sub">${esc(sub)}</p><div style="display:flex;gap:8px"><button class="btn ghost" style="flex:1" data-close>Cancelar</button><button class="btn ${danger ? 'primary' : 'primary'}" style="flex:1;${danger ? 'background:var(--crit);color:#fff' : ''}" id="cok">${esc(ok)}</button></div>`,
    s => s.querySelector('#cok').onclick = () => { closeSheet(); fn(); });
}
function report(uid, pid) {
  if (needReal()) return;
  const M = [['acoso', 'Acoso o insultos'], ['spam', 'Spam o publicidad'], ['suplantacion', 'Suplanta a otra persona'], ['contenido', 'Contenido inapropiado'], ['menor', 'Riesgo para un menor'], ['otro', 'Otro motivo']];
  openSheet(`<h2 id="sheetT">Denunciar</h2><p class="sub">Lo revisamos nosotros. La otra persona no sabrá quién ha denunciado.</p>
    <div class="choice" style="flex-direction:column">${M.map(([k, v], i) => `<label style="min-width:100%"><input type="radio" name="rm" value="${k}"${i ? '' : ' checked'}><span>${v}</span></label>`).join('')}</div>
    <label class="field" style="margin-top:12px"><span>Cuéntanos qué ha pasado (opcional)</span><textarea class="in" id="rt" maxlength="500"></textarea></label>
    <button class="btn primary block" id="rgo">Enviar denuncia</button>`, s => s.querySelector('#rgo').onclick = async () => {
      try { await q(SB.from('social_denuncias').insert({ contra: uid, partida: pid || null, motivo: s.querySelector('input[name=rm]:checked').value, texto: s.querySelector('#rt').value.trim() || null }));
        closeSheet(); toast('Gracias. Lo revisaremos.'); } catch (e) { toast(errMsg(e)); } });
}
function block(uid, nombre) {
  if (needReal()) return;
  confirmSheet('¿Bloquear a ' + (nombre || 'este jugador') + '?', 'Dejaréis de ver vuestros perfiles y partidas, y se borran la amistad y las solicitudes entre vosotros. Puedes desbloquearlo desde tu perfil.', 'Bloquear', async () => {
    try { await q(SB.from('social_bloqueos').insert({ quien: ME.id, a_quien: uid })); toast('Bloqueado'); location.hash = '#partidas'; } catch (e) { toast(errMsg(e)); } });
}
function askProfile() { toast('Primero crea tu perfil de jugador'); location.hash = '#perfil/editar'; }

function vPublicar(arg) {
  setTab('publicar');
  if (DEMO) { view.innerHTML = `<section class="shero"><p class="eb">Publicar</p><h1>Publica tu partida.</h1><p>Elige campo, día y plazas. Los jugadores te piden unirse y tú decides.</p><div class="acts"><button class="btn gold" data-login>Entrar para publicar</button></div></section>${demoForm()}`; return; }
  if (!MYP) { view.innerHTML = `<div class="empty glass panel" style="margin-top:14px"><b>Primero, tu perfil de jugador.</b>Así los demás saben con quién van a jugar.<br><a class="btn primary" href="#perfil/editar">Crear mi perfil</a></div>`; return; }
  const t = arg && arg.startsWith('t/') ? TT.find(x => tid(x) === arg.slice(2)) : null;
  view.innerHTML = `<div class="sec" style="margin-top:18px"><h2>Publicar partida</h2></div>
  <form id="pf" class="panel glass" novalidate>
    <div class="field"><span>¿Qué buscas?</span><div class="choice"><label><input type="radio" name="tipo" value="partida"${t ? '' : ' checked'}><span>Gente para jugar</span></label><label><input type="radio" name="tipo" value="torneo"${t ? ' checked' : ''}><span>Pareja para un torneo</span></label></div></div>
    <div id="tsel" ${t ? '' : 'hidden'} class="field"><span>Torneo</span><input class="in" id="tq" placeholder="Busca por nombre o club" autocomplete="off" value="${t ? esc(t.n) : ''}"><div class="sugg glass" id="ts" hidden></div><small id="tinfo">${t ? esc(t.club + ' · ' + when(t.s)) : 'Los torneos por parejas salen primero.'}</small></div>
    <div class="field"><span>Campo</span><input class="in" name="campo" id="campo" required maxlength="80" placeholder="Escribe el club o la localidad" autocomplete="off" value="${t ? esc(t.club) : ''}"><div class="sugg glass" id="ps" hidden></div><small id="pwhere">${t && whereOf(t.club) ? esc(whereOf(t.club)) : 'Elige el club de la lista y sabremos dónde está.'}</small></div>
    <div class="two"><label class="field"><span>Día</span><input class="in" type="date" name="fecha" required min="${TODAY}" max="${addDays(180)}" value="${t ? esc(t.s) : weekend()[0]}"></label>
      <label class="field"><span>Hora <small style="display:inline;color:var(--muted)">(opcional)</small></span><input class="in" type="time" name="hora" step="300"></label></div>
    <div class="field"><span>¿Cuántos buscas?</span><div class="choice">${[1, 2, 3].map(n => `<label><input type="radio" name="plazas" value="${n}"${n === (t ? 1 : 3) ? ' checked' : ''}><span>${n} ${n === 1 ? 'jugador' : 'jugadores'}</span></label>`).join('')}</div></div>
    <div class="field"><span>Hándicap que buscas <small style="display:inline;color:var(--muted)">(opcional)</small></span><div class="two"><input class="in" type="number" name="hmin" step="0.1" min="-10" max="54" placeholder="Desde"><input class="in" type="number" name="hmax" step="0.1" min="-10" max="54" placeholder="Hasta"></div></div>
    <label class="field"><span>Precio por jugador</span><div class="eur"><input class="in" type="number" name="precio" required min="0" max="2000" step="1" inputmode="numeric" placeholder="Ej.: 65"><b>€</b></div><small>Lo que paga cada uno: green fee, buggy si va incluido o la inscripción del torneo. Pon 0 si no cuesta nada.</small></label>
    <label class="field"><span>Nota</span><textarea class="in" name="nota" maxlength="280" placeholder="Ritmo de juego, si vais en buggy, tercer tiempo…"></textarea></label>
    <div class="switch"><div><b>Solo para mis amigos</b><small>Si no, la ve cualquier jugador con cuenta.</small></div><input type="checkbox" name="am" aria-label="Solo para mis amigos"></div>
    <p class="err" id="perr" hidden></p>
    <button class="btn primary block" type="submit" style="margin-top:14px">Publicar</button>
  </form>`;
  const f = view.querySelector('#pf'); let tor = t;
  f.querySelectorAll('input[name=tipo]').forEach(r => r.onchange = () => { f.querySelector('#tsel').hidden = f.tipo.value !== 'torneo'; if (f.tipo.value === 'torneo') f.plazas.value = '1'; });
  const ci = f.querySelector('#campo'), ps = f.querySelector('#ps'), pw = f.querySelector('#pwhere');
  const setWhere = () => { const w = whereOf(ci.value.trim()); pw.textContent = w ? w : (ci.value.trim() ? 'No lo tenemos en la lista: se publicará con tu provincia.' : 'Elige el club de la lista y sabremos dónde está.'); };
  ci.oninput = () => { const L = findClubs(ci.value); ps.hidden = !L.length; ps.innerHTML = clubSugg(L); setWhere(); };
  ps.onclick = e => { const b = e.target.closest('[data-c]'); if (!b) return; ci.value = b.dataset.c; ps.hidden = true; setWhere(); };
  const tq = f.querySelector('#tq'), ts = f.querySelector('#ts');
  tq.oninput = () => {
    const s = tq.value.trim().toLowerCase(); if (s.length < 2) { ts.hidden = true; return; }
    const L = TT.filter(x => x.s >= TODAY && (x.n + ' ' + x.club).toLowerCase().includes(s)).sort((a, b) => (b.form === 'Parejas') - (a.form === 'Parejas') || a.s.localeCompare(b.s)).slice(0, 8);
    ts.hidden = !L.length; ts.innerHTML = L.map(x => `<button type="button" data-k="${esc(tid(x))}">${esc(x.n)}<small>${esc(x.club)} · ${esc(when(x.s))}${x.form === 'Parejas' ? ' · Parejas' : ''}</small></button>`).join('');
  };
  ts.onclick = e => { const b = e.target.closest('button'); if (!b) return; tor = TT.find(x => tid(x) === b.dataset.k); tq.value = tor.n; ts.hidden = true; f.campo.value = tor.club; setWhere(); f.fecha.value = tor.s; f.querySelector('#tinfo').textContent = tor.club + ' · ' + when(tor.s); };
  f.onsubmit = async e => {
    e.preventDefault(); const er = f.querySelector('#perr'); er.hidden = true;
    const campo = f.campo.value.trim(), tipo = f.tipo.value;
    const hmin = f.hmin.value === '' ? null : +f.hmin.value, hmax = f.hmax.value === '' ? null : +f.hmax.value;
    const bad = !campo ? 'Escribe el campo.' : !f.fecha.value || f.fecha.value < TODAY ? 'Elige un día a partir de hoy.' : tipo === 'torneo' && !tor ? 'Elige el torneo de la lista.' : hmin != null && hmax != null && hmin > hmax ? 'El hándicap «desde» es mayor que «hasta».' : f.precio.value === '' ? 'Pon el precio por jugador (0 si no cuesta nada).' : !(+f.precio.value >= 0 && +f.precio.value <= 2000) ? 'El precio tiene que estar entre 0 y 2.000 €.' : '';
    if (bad) { er.hidden = false; er.textContent = bad; return; }
    const row = { campo, provincia: CLUBS.get(campo) || (tor && tor.prov) || MYP.provincia || null, fecha: f.fecha.value, hora: f.hora.value || null, tipo, plazas: +f.plazas.value,
      hcp_min: hmin, hcp_max: hmax, nota: f.nota.value.trim() || null, solo_amigos: f.am.checked, precio: Math.round(+f.precio.value),
      torneo: tipo === 'torneo' && tor ? tor.n.slice(0, 160) : null, torneo_url: tipo === 'torneo' && tor ? (safeUrl(tor.url) || null) : null };
    const btn = f.querySelector('[type=submit]'); btn.disabled = true;
    try { const r = await q(SB.from('social_partidas').insert(row).select('id').single()); toast('¡Publicada! Compártela para que te encuentren.'); location.hash = '#partida/' + r.id; }
    catch (e2) { er.hidden = false; er.textContent = errMsg(e2); btn.disabled = false; }
  };
}
function demoForm() {
  return `<div class="panel glass" style="opacity:.75;pointer-events:none" aria-hidden="true"><div class="field"><span>¿Qué buscas?</span><div class="choice"><label><input type="radio" checked><span>Gente para jugar</span></label><label><input type="radio"><span>Pareja para un torneo</span></label></div></div>
  <label class="field"><span>Campo</span><input class="in" value="${esc([...CLUBS.keys()][0] || 'Tu club')}"></label><div class="two"><label class="field"><span>Día</span><input class="in" value="${esc(dow(weekend()[0]) + ' ' + D(weekend()[0]).getDate() + ' ' + mon(weekend()[0]))}"></label><label class="field"><span>Hora</span><input class="in" value="09:30"></label></div>
  <div class="field"><span>¿Cuántos buscas?</span><div class="choice"><label><input type="radio"><span>1 jugador</span></label><label><input type="radio"><span>2 jugadores</span></label><label><input type="radio" checked><span>3 jugadores</span></label></div></div></div>`;
}

const playerRow = (p, extra = '') => `<div class="row">${av(p, 'm')}<a class="grow" href="#jugador/${esc(p.user_id)}"><b>${esc(p.nombre)}</b><span>Hándicap ${hcpTxt(p.hcp)}${p.provincia ? ' · ' + esc(p.provincia) : ''}${p.campos && p.campos[0] ? ' · ' + esc(p.campos[0]) : ''}</span></a>${extra}</div>`;
let JTAB = 'buscar', JF = { prov: '', nombre: '', h: '' };
async function vJugadores(sub) {
  setTab('jugadores'); if (sub) JTAB = sub;
  let am = { amigos: [], recibidas: [], enviadas: [] };
  try { if (ME || DEMO) am = await amistades(); } catch (e) { /* sigue */ }
  view.innerHTML = `<div class="sec" style="margin-top:18px"><h2>Jugadores</h2></div>
  <div class="sseg" role="tablist"><button role="tab" data-j="buscar" aria-selected="${JTAB === 'buscar'}">Buscar</button><button role="tab" data-j="amigos" aria-selected="${JTAB === 'amigos'}">Amigos ${am.amigos.length ? '· ' + am.amigos.length : ''}</button><button role="tab" data-j="sol" aria-selected="${JTAB === 'sol'}">Solicitudes${am.recibidas.length ? '<span class="dot">' + am.recibidas.length + '</span>' : ''}</button></div><div id="jl"></div>`;
  view.querySelectorAll('[data-j]').forEach(b => b.onclick = () => { JTAB = b.dataset.j; vJugadores(); });
  const box = $('#jl');
  if (JTAB === 'amigos') {
    box.innerHTML = am.amigos.length ? `<div class="panel glass">${am.amigos.map(p => playerRow(p)).join('')}</div>` : `<div class="empty glass panel"><b>Aún no tienes amigos aquí.</b>Busca a la gente con la que juegas y añádela.<br><button class="btn primary" data-j2="buscar">Buscar jugadores</button></div>`;
  } else if (JTAB === 'sol') {
    box.innerHTML = (am.recibidas.length ? `<div class="panel glass">${am.recibidas.map(p => playerRow(p, `<div style="display:flex;gap:6px"><button class="btn soft sm" data-fno="${esc(p.user_id)}">No</button><button class="btn primary sm" data-fok="${esc(p.user_id)}">Aceptar</button></div>`)).join('')}</div>` : `<div class="empty glass panel"><b>No tienes solicitudes.</b>Cuando alguien quiera ser tu amigo, aparecerá aquí.</div>`)
      + (am.enviadas.length ? `<div class="sec"><h2>Enviadas</h2></div><div class="panel glass">${am.enviadas.map(p => playerRow(p, '<span class="tag mute">Pendiente</span>')).join('')}</div>` : '');
  } else {
    box.innerHTML = `<div class="filters"><select class="pill" id="jp" aria-label="Provincia"><option value="">Toda España</option>${PROVS.map(p => `<option${JF.prov === p ? ' selected' : ''}>${esc(p)}</option>`).join('')}</select>
      ${[['', 'Cualquier hándicap'], ['0-12', 'Hasta 12'], ['12-24', '12 – 24'], ['24-54', 'Más de 24']].map(([k, v]) => `<button class="pill" data-h="${k}" aria-pressed="${JF.h === k}">${v}</button>`).join('')}</div>
      <input class="in" id="jn" type="search" placeholder="Buscar por nombre" value="${esc(JF.nombre)}" style="margin:4px 0 10px;border-radius:999px"><div id="jr">${skel(3)}</div>`;
    box.querySelector('#jp').onchange = e => { JF.prov = e.target.value; load(); };
    box.querySelectorAll('[data-h]').forEach(b => b.onclick = () => { JF.h = b.dataset.h; box.querySelectorAll('[data-h]').forEach(x => x.setAttribute('aria-pressed', x === b)); load(); });
    let tq = 0; box.querySelector('#jn').oninput = e => { clearTimeout(tq); tq = setTimeout(() => { JF.nombre = e.target.value.trim(); load(); }, 250); };
    async function load() {
      let L = []; try { L = await jugadores(JF); } catch (e) { $('#jr').innerHTML = `<div class="empty"><b>No se ha podido cargar.</b>${esc(errMsg(e))}</div>`; return; }
      if (DEMO) L = L.filter(p => (!JF.prov || p.provincia === JF.prov) && (!JF.nombre || p.nombre.toLowerCase().includes(JF.nombre.toLowerCase())));
      if (JF.h) { const [lo, hi] = JF.h.split('-').map(Number); L = L.filter(p => p.hcp != null && p.hcp >= lo && p.hcp <= hi); }
      $('#jr').innerHTML = L.length ? `<div class="panel glass">${L.map(p => playerRow(p)).join('')}</div>` : `<div class="empty glass panel"><b>Nadie con estos filtros todavía.</b>Invita a tus compañeros de partida a Banderín Social.<br><button class="btn primary" data-inv>Invitar</button></div>`;
      const inv = $('#jr [data-inv]'); if (inv) inv.onclick = () => share('Únete a Banderín Social y juguemos juntos', location.origin + '/social/');
    }
    load();
  }
  box.querySelectorAll('[data-j2]').forEach(b => b.onclick = () => { JTAB = b.dataset.j2; vJugadores(); });
  box.querySelectorAll('[data-fok],[data-fno]').forEach(b => b.onclick = async () => {
    if (needReal()) return; const id = b.dataset.fok || b.dataset.fno;
    try { if (b.dataset.fok) await q(SB.from('social_amistades').update({ estado: 'aceptada' }).eq('de', id).eq('para', ME.id)); else await q(SB.from('social_amistades').delete().eq('de', id).eq('para', ME.id));
      toast(b.dataset.fok ? '¡Ahora sois amigos!' : 'Solicitud rechazada'); vJugadores(); badges(); } catch (e) { toast(errMsg(e)); } });
}

function profileBlock(p, c, opts = {}) {
  const contact = c && (c.whatsapp || c.email) ? `<div class="contact" style="justify-content:center;margin-top:12px">${c.whatsapp ? `<a class="btn primary sm" href="https://wa.me/${esc(waNum(c.whatsapp))}" target="_blank" rel="noopener">${I.wa}WhatsApp</a>` : ''}${c.email ? `<a class="btn soft sm" href="mailto:${esc(c.email)}">${I.mail}Correo</a>` : ''}</div>` :
    opts.self ? '' : `<p class="lock" style="justify-content:center;margin-top:12px">${I.lock}<span>Su contacto se ve cuando sois amigos o jugáis una partida juntos.</span></p>`;
  return `<div class="panel glass prof">${av(p, 'l')}<h1>${esc(p.nombre)}</h1><p class="sub">${p.provincia ? esc(p.provincia) : 'Golfista'}${opts.self && !p.visible ? ' · Oculto en Jugadores' : ''}</p>
    <div class="stats"><div><b>${hcpTxt(p.hcp)}</b><span>Hándicap</span></div><div><b>${(p.campos || []).length}</b><span>Campos</span></div><div><b>${opts.n != null ? opts.n : '—'}</b><span>Partidas</span></div></div>
    ${p.bio ? `<p class="bio">${esc(p.bio)}</p>` : ''}
    ${(p.campos || []).length ? `<div class="chips" style="justify-content:center">${p.campos.map(x => `<span class="chip" style="padding-right:12px">${esc(x)}</span>`).join('')}</div>` : ''}
    ${contact}${opts.acts ? `<div class="acts">${opts.acts}</div>` : ''}</div>`;
}
async function vJugador(id) {
  setTab('jugadores');
  if (ME && id === ME.id) { location.hash = '#perfil'; return; }
  view.innerHTML = backBtn() + skel(1);
  let r; try { r = await jugador(id); } catch (e) { view.innerHTML = backBtn() + `<div class="empty"><b>No se ha podido cargar.</b>${esc(errMsg(e))}</div>`; return; }
  if (!r) { view.innerHTML = backBtn() + `<div class="empty glass panel"><b>Este perfil no está disponible.</b>Puede que sea privado o que ya no exista.</div>`; return; }
  const btn = r.rel === 'amigos' ? `<button class="btn soft" data-unf>${I.check}Amigos</button>` : r.rel === 'enviada' ? `<button class="btn soft" disabled>Solicitud enviada</button>` :
    r.rel === 'recibida' ? `<button class="btn primary" data-facc>Aceptar amistad</button>` : `<button class="btn primary" data-fadd>${I.plus}Añadir amigo</button>`;
  view.innerHTML = backBtn() + `<div style="margin-top:12px">${profileBlock(r.p, r.c, { n: r.partidas.length, acts: btn })}</div>
    ${r.partidas.length ? `<div class="sec"><h2>Sus próximas partidas</h2></div><div class="list">${r.partidas.map(p => matchCard({ ...p, autorP: r.p, ocupadas: p.ok || 0 })).join('')}</div>` : ''}
    <div class="more smore"><button data-report>Denunciar</button><button data-block>Bloquear</button></div>`;
  const on1 = (s, fn) => { const b = view.querySelector(s); if (b) b.onclick = fn; };
  on1('[data-fadd]', async () => { if (needReal()) return; if (!MYP) return askProfile(); try { await q(SB.from('social_amistades').insert({ de: ME.id, para: id })); toast('Solicitud enviada'); vJugador(id); } catch (e) { toast(errMsg(e)); } });
  on1('[data-facc]', async () => { try { await q(SB.from('social_amistades').update({ estado: 'aceptada' }).eq('de', id).eq('para', ME.id)); toast('¡Ahora sois amigos!'); vJugador(id); badges(); } catch (e) { toast(errMsg(e)); } });
  on1('[data-unf]', () => confirmSheet('¿Quitar de amigos?', 'Dejaréis de ver el contacto del otro (salvo que juguéis una partida juntos).', 'Quitar', async () => {
    try { await q(SB.from('social_amistades').delete().or(`and(de.eq.${ME.id},para.eq.${id}),and(de.eq.${id},para.eq.${ME.id})`)); vJugador(id); } catch (e) { toast(errMsg(e)); } }));
  on1('[data-report]', () => report(id, null));
  on1('[data-block]', () => block(id, r.p.nombre));
}

let MTAB = 'pub';
async function vMias() {
  setTab('mias');
  if (DEMO) { view.innerHTML = `<div class="empty glass panel" style="margin-top:18px"><b>Aquí verás tus partidas.</b>Las que publicas y a las que te apuntas, con sus solicitudes.<br><button class="btn primary" data-login>Entrar</button></div>`; return; }
  view.innerHTML = `<div class="sec" style="margin-top:18px"><h2>Mis partidas</h2></div><div class="sseg" role="tablist"><button role="tab" data-m="pub" aria-selected="${MTAB === 'pub'}">Publicadas</button><button role="tab" data-m="ap" aria-selected="${MTAB === 'ap'}">Me apunté</button></div><div id="mm">${skel(2)}</div>`;
  view.querySelectorAll('[data-m]').forEach(b => b.onclick = () => { MTAB = b.dataset.m; vMias(); });
  try {
    if (MTAB === 'pub') {
      const rows = await q(SB.from('social_partidas').select(MCOLS).eq('autor', ME.id).gte('fecha', addDays(-30)).order('fecha', { ascending: false }));
      const sol = rows.length ? await q(SB.from('social_solicitudes').select('partida,estado').in('partida', rows.map(r => r.id))) : [];
      const L = rows.map(r => ({ ...r, autorP: MYP, mia: true, ocupadas: sol.filter(s => s.partida === r.id && s.estado === 'aceptada').length, pendientes: sol.filter(s => s.partida === r.id && s.estado === 'pendiente').length }));
      $('#mm').innerHTML = L.length ? '<div class="list">' + L.map(matchCard).join('') + '</div>' : `<div class="empty glass panel"><b>No has publicado ninguna partida.</b>¿Juegas este finde? Publícalo y que se apunte alguien.<br><a class="btn primary" href="#publicar">${I.plus}Publicar</a></div>`;
    } else {
      const sol = await q(SB.from('social_solicitudes').select('partida,estado').eq('jugador', ME.id));
      const rows = sol.length ? await q(SB.from('social_partidas').select(MCOLS).in('id', sol.map(s => s.partida)).gte('fecha', addDays(-30)).order('fecha')) : [];
      const prof = await perfilesDe(rows.map(r => r.autor));
      const L = rows.map(r => ({ ...r, autorP: prof.get(r.autor) || { nombre: '' }, yo: sol.find(s => s.partida === r.id), ocupadas: 0 }));
      $('#mm').innerHTML = L.length ? '<div class="list">' + L.map(matchCard).join('') + '</div>' : `<div class="empty glass panel"><b>Aún no te has apuntado a ninguna.</b><br><a class="btn primary" href="#partidas">Ver partidas</a></div>`;
    }
  } catch (e) { $('#mm').innerHTML = `<div class="empty"><b>No se ha podido cargar.</b>${esc(errMsg(e))}</div>`; }
}

async function vPerfil(sub) {
  setTab('perfil');
  if (!ME) {
    view.innerHTML = `<section class="shero"><p class="eb">Tu perfil de jugador</p><h1>Que sepan con quién juegan.</h1><p>Tu nombre, tu hándicap, tus campos y tu zona. Tu contacto, solo si tú quieres.</p><div class="acts"><button class="btn gold" data-login>Entrar con mi cuenta</button></div></section>
    <div style="margin-top:12px">${profileBlock(DEMOD.U[0], null, { n: 1, self: true })}</div><p class="lede" style="text-align:center;margin-top:10px">Perfil de ejemplo</p>`;
    return;
  }
  if (NOSQL) { view.innerHTML = `<div class="empty glass panel" style="margin-top:18px"><b>Falta preparar la base de datos.</b>Cuando esté lista podrás crear tu perfil de jugador.<br><button class="btn ghost" id="lo">Cerrar sesión</button></div>`; $('#lo').onclick = () => SB.auth.signOut(); return; }
  if (sub === 'editar' || !MYP) return await vEditar();
  let n = 0; try { n = (await q(SB.from('social_partidas').select('id').eq('autor', ME.id).gte('fecha', TODAY))).length; } catch (e) { }
  view.innerHTML = `<div style="margin-top:14px">${profileBlock(MYP, MYC, { self: true, n, acts: `<a class="btn primary" href="#perfil/editar">Editar perfil</a><button class="btn ghost" data-sh>${I.share}Compartir</button>` })}</div>
    <div class="panel glass" style="margin-top:10px"><div class="lock">${I.lock}<span>${MYC && MYC.publico ? 'Tu contacto es visible para cualquier jugador con cuenta.' : 'Tu contacto solo lo ven tus amigos y quien juega una partida contigo.'} Tu fecha de nacimiento no la ve nadie.</span></div></div>
    <div class="more smore"><button id="lo">Cerrar sesión</button><button id="unb">Desbloquear jugadores</button><button id="delp">Borrar mi perfil social</button></div>`;
  view.querySelector('[data-sh]').onclick = () => share('Juega conmigo en Banderín Social', location.origin + '/social/#jugador/' + ME.id);
  $('#lo').onclick = () => SB.auth.signOut();
  $('#unb').onclick = async () => {
    const b = await q(SB.from('social_bloqueos').select('a_quien')).catch(() => []);
    openSheet(`<h2 id="sheetT">Jugadores bloqueados</h2>${b.length ? b.map(x => `<div class="row"><div class="grow"><b>Jugador bloqueado</b><span>No ves su perfil mientras esté bloqueado</span></div><button class="btn soft sm" data-ub="${esc(x.a_quien)}">Desbloquear</button></div>`).join('') : '<p class="sub">No has bloqueado a nadie.</p>'}`,
      s => s.querySelectorAll('[data-ub]').forEach(x => x.onclick = async () => { await q(SB.from('social_bloqueos').delete().eq('quien', ME.id).eq('a_quien', x.dataset.ub)).catch(() => {}); x.closest('.row').remove(); toast('Desbloqueado'); }));
  };
  $('#delp').onclick = () => confirmSheet('¿Borrar tu perfil social?', 'Se borran tu perfil, tu contacto y tus partidas de Social. Tu cuenta de Banderín y tus avisos siguen igual.', 'Borrar', async () => {
    try { await q(SB.from('social_partidas').delete().eq('autor', ME.id)); await q(SB.from('social_contacto').delete().eq('user_id', ME.id)); await q(SB.from('social_perfiles').delete().eq('user_id', ME.id)); await borrarFotos(null); await refresh(); toast('Perfil borrado'); location.hash = '#partidas'; } catch (e) { toast(errMsg(e)); } });
}

async function vEditar() {
  // Un solo perfil: lo de Social y lo de «Mi cuenta» (hándicap, sexo, federación, socio de…) se editan aquí juntos.
  let datos = null, pre = null, nacAno = null;
  try { const r = (await q(SB.from('perfiles').select('datos').eq('user_id', ME.id).limit(1)))[0]; datos = (r && r.datos) || null; pre = datos && datos.perfil; } catch (e) { }
  try { const r = (await q(SB.from('social_privado').select('nacimiento').eq('user_id', ME.id).limit(1)))[0]; if (r) nacAno = +r.nacimiento.slice(0, 4); } catch (e) { }
  const priv = { sexo: (pre && pre.sexo) || '', fed: (pre && pre.fed) || '', socio: pre && Array.isArray(pre.clubs) ? pre.clubs.filter(c => typeof c === 'string').slice(0, 10) : [] };
  // Clubes escritos a mano en la cuenta («real club puerta de hierro») → el nombre del directorio («Real Club de la Puerta de Hierro»).
  const VACIAS = new Set(['de', 'del', 'la', 'las', 'el', 'los', 'y', 'club', 'golf', 'real', 'cg', 'rcg']);
  const pal = x => fold(x).split(/[^a-z0-9]+/).filter(w => w && !VACIAS.has(w));
  const canon = c => { if (CLUBS.has(c)) return c; const w = pal(c); if (!w.length) return c;
    const hit = [...CLUBS.keys()].filter(k => { const kw = pal(k); return w.every(x => kw.includes(x)); }).sort((a, b) => pal(a).length - pal(b).length);
    return hit[0] || c; };
  const preClubs = pre && Array.isArray(pre.clubs) ? [...new Set(pre.clubs.filter(c => typeof c === 'string').map(canon))].slice(0, 8) : [];
  const base = MYP ? { ...MYP, hcp: MYP.hcp ?? (pre && typeof pre.hcp === 'number' ? pre.hcp : null) } : null;
  const p = base || { nombre: (ME.user_metadata && (ME.user_metadata.full_name || ME.user_metadata.name)) || '', hcp: pre && typeof pre.hcp === 'number' ? pre.hcp : null, provincia: (preClubs.map(c => CLUBS.get(c)).find(Boolean)) || '', campos: preClubs, bio: '', visible: true };
  const c = MYC || { whatsapp: '', email: ME.email || '', publico: false };
  let campos = [...(p.campos || [])], socio = [...priv.socio];
  const nuevo = !MYP;
  view.innerHTML = `${MYP ? backBtn() : ''}<div class="sec" style="margin-top:18px"><h2>${nuevo ? (pre ? 'Activa tu perfil en Social' : 'Crea tu perfil de jugador') : 'Editar mi perfil'}</h2></div>
  ${nuevo ? `<p class="lede">${pre ? 'Tu perfil de Banderín ya está aquí. Para que te vean otros jugadores solo faltan el nombre que verán y tu fecha de nacimiento.' : 'Un solo perfil para Torneos y para Social. Dos minutos.'}</p>` : ''}
  <form id="ef" class="panel glass" novalidate>
    <div class="fotopick"><span id="fprev">${av({ ...p, user_id: ME.id }, 'l')}</span>
      <div><b>Foto de perfil</b><small>Opcional. Que se te vea la cara ayuda a quedar. La ven solo los jugadores con cuenta.</small>
      <div class="fbtns"><label class="btn soft sm">Elegir foto<input type="file" accept="image/*" id="ffile" hidden></label>
      ${matchMedia('(pointer:coarse)').matches ? '<label class="btn soft sm">Hacer foto<input type="file" accept="image/*" capture="user" id="fcam" hidden></label>' : ''}
      <button type="button" class="btn ghost sm" id="fdel"${p.foto ? '' : ' hidden'}>Quitar</button></div></div></div>
    <label class="field"><span>Nombre que verán los demás</span><input class="in" name="nombre" maxlength="40" required value="${esc(p.nombre)}" placeholder="Ej.: Lucía M."><small>Puedes poner solo tu nombre y la inicial del apellido.</small></label>
    ${EST && !EST.edad ? `<label class="field"><span>Fecha de nacimiento</span><input class="in" type="date" name="nac" required max="${addDays(-365 * 16 - 4)}"><small>No la ve nadie. Hay que tener al menos 16 años. No se puede cambiar después.</small></label>` : ''}
    ${nuevo && pre ? '<details class="rest"><summary>Revisar el resto de tu perfil <small>(ya relleno con tu cuenta)</small></summary>' : '<div>'}
    <div class="two"><label class="field"><span>Hándicap</span><input class="in" type="number" name="hcp" step="0.1" min="-10" max="54" inputmode="decimal" value="${p.hcp ?? ''}" placeholder="18,4"></label>
      <label class="field"><span>Provincia</span><select class="in" name="prov"><option value="">Elige</option>${PROVS.map(x => `<option${p.provincia === x ? ' selected' : ''}>${esc(x)}</option>`).join('')}</select></label></div>
    <div class="field"><span>Campos donde te gusta jugar <small style="display:inline;color:var(--muted)">(hasta 8)</small></span><input class="in" id="cq" placeholder="Busca un club" autocomplete="off"><div class="sugg glass" id="cs" hidden></div><div class="chips" id="cc"></div></div>
    <label class="field"><span>Sobre ti <small style="display:inline;color:var(--muted)">(opcional)</small></span><textarea class="in" name="bio" maxlength="280" placeholder="Cuándo sueles jugar, qué formatos te gustan…">${esc(p.bio || '')}</textarea></label>
    <div class="sec" style="margin:8px 0 6px"><h2 style="font-size:20px">Para los torneos</h2></div>
    <p class="lede" style="margin:0 0 10px">Privado: no lo ve nadie. Sirve para que Torneos te marque los que encajan contigo.</p>
    <div class="two"><label class="field"><span>Sexo de competición</span><select class="in" name="sexo"><option value="">Sin indicar</option><option value="M"${priv.sexo === 'M' ? ' selected' : ''}>Masculino</option><option value="F"${priv.sexo === 'F' ? ' selected' : ''}>Femenino</option></select></label>
      <label class="field"><span>Federación autonómica</span><select class="in" name="fed"><option value="">Sin indicar</option>${CCAA.map(x => `<option${priv.fed === x ? ' selected' : ''}>${esc(x)}</option>`).join('')}</select></label></div>
    <div class="field"><span>Clubes de los que eres socio <small style="display:inline;color:var(--muted)">(para los torneos solo para socios)</small></span><input class="in" id="sq" placeholder="Busca tu club" autocomplete="off"><div class="sugg glass" id="ss" hidden></div><div class="chips" id="sc"></div></div>
    <div class="sec" style="margin:8px 0 6px"><h2 style="font-size:20px">Contacto</h2></div>
    <p class="lede" style="margin:0 0 10px">Solo lo ven tus amigos y los jugadores con los que quedas, salvo que lo hagas público.</p>
    <div class="two"><label class="field"><span>WhatsApp</span><input class="in" type="tel" name="wa" inputmode="tel" maxlength="17" value="${esc(c.whatsapp || '')}" placeholder="600 123 456"></label>
      <label class="field"><span>Correo</span><input class="in" type="email" name="em" maxlength="120" value="${esc(c.email || '')}"></label></div>
    <div class="switch"><div><b>Contacto visible para todos</b><small>${EST && EST.mayor ? 'Cualquier jugador con cuenta lo verá.' : 'Solo para mayores de 18. Así protegemos a los más jóvenes.'}</small></div><input type="checkbox" name="pub" aria-label="Contacto visible para todos"${c.publico ? ' checked' : ''}${EST && EST.mayor ? '' : ' disabled'}></div>
    <div class="switch"><div><b>Aparecer en «Jugadores»</b><small>Si lo apagas, solo te verán tus amigos y con quien juegues.</small></div><input type="checkbox" name="vis" aria-label="Aparecer en Jugadores"${p.visible !== false ? ' checked' : ''}></div>
    <div class="switch"><div><b>Avisarme por correo</b><small>Cuando alguien pida unirse a tu partida, te acepten o te pidan amistad. Como mucho 12 al día.</small></div><input type="checkbox" name="av" aria-label="Avisarme por correo"${!EST || EST.avisos !== false ? ' checked' : ''}></div>
    ${nuevo && pre ? '</details>' : '</div>'}
    ${nuevo ? `<label class="okrow"><input type="checkbox" name="ok"><span>Tengo 16 años o más y acepto las <a href="/#terminos" target="_blank" rel="noopener">normas de Banderín Social</a> y la <a href="/#privacidad" target="_blank" rel="noopener">política de privacidad</a>. Los demás jugadores verán mi nombre, hándicap, provincia y campos.</span></label>` : ''}
    <p class="err" id="eerr" hidden></p>
    <button class="btn primary block" type="submit" style="margin-top:14px">${nuevo ? (pre ? 'Activar mi perfil' : 'Crear mi perfil') : 'Guardar'}</button>
  </form>`;
  const f = view.querySelector('#ef'), cq = f.querySelector('#cq'), cs = f.querySelector('#cs'), cc = f.querySelector('#cc');
  const drawC = () => { cc.innerHTML = campos.map((x, i) => `<span class="chip">${esc(x)}<button type="button" data-rm="${i}" aria-label="Quitar ${esc(x)}">×</button></span>`).join(''); cq.disabled = campos.length >= 8; };
  drawC();
  // Foto: 'keep' sin cambios, Blob nueva, null para quitarla.
  let foto = 'keep';
  const fprev = f.querySelector('#fprev'), fdel = f.querySelector('#fdel');
  const pintaFoto = url => { fprev.innerHTML = av({ ...p, user_id: ME.id, foto: null, _fotoLocal: url }, 'l'); };
  const elegir = async inp => { const file = inp.files && inp.files[0]; inp.value = ''; if (!file) return;
    try { foto = await prepararFoto(file); pintaFoto(URL.createObjectURL(foto)); fdel.hidden = false; }
    catch (e) { toast('No se ha podido leer esa foto. Prueba con otra (JPG o PNG).'); } };
  f.querySelector('#ffile').onchange = e => elegir(e.target);
  const fcam = f.querySelector('#fcam'); if (fcam) fcam.onchange = e => elegir(e.target);
  fdel.onclick = () => { foto = null; pintaFoto(null); fdel.hidden = true; };
  const sq = f.querySelector('#sq'), ss = f.querySelector('#ss'), sc = f.querySelector('#sc');
  const drawS = () => { sc.innerHTML = socio.map((x, i) => `<span class="chip">${esc(x)}<button type="button" data-rm="${i}" aria-label="Quitar ${esc(x)}">×</button></span>`).join(''); sq.disabled = socio.length >= 10; };
  drawS();
  sc.onclick = e => { const b = e.target.closest('[data-rm]'); if (b) { socio.splice(+b.dataset.rm, 1); drawS(); } };
  sq.oninput = () => { const L = findTClubs(sq.value, socio); ss.hidden = !L.length; ss.innerHTML = clubSugg(L); };
  ss.onclick = e => { const b = e.target.closest('[data-c]'); if (!b) return; socio.push(b.dataset.c); sq.value = ''; ss.hidden = true; drawS(); };
  cc.onclick = e => { const b = e.target.closest('[data-rm]'); if (b) { campos.splice(+b.dataset.rm, 1); drawC(); } };
  cq.oninput = () => { const L = findClubs(cq.value, campos); cs.hidden = !L.length; cs.innerHTML = clubSugg(L); };
  cs.onclick = e => { const b = e.target.closest('[data-c]'); if (!b) return; campos.push(b.dataset.c); cq.value = ''; cs.hidden = true; drawC(); if (!f.prov.value) f.prov.value = CLUBS.get(b.dataset.c) || ''; };
  f.onsubmit = async e => {
    e.preventDefault(); const er = f.querySelector('#eerr'); er.hidden = true;
    const nombre = f.nombre.value.trim(), hcp = f.hcp.value === '' ? null : Math.round(+f.hcp.value * 10) / 10;
    const wa = f.wa.value.trim(), em = f.em.value.trim();
    const bad = f.ok && !f.ok.checked ? 'Para crear tu perfil tienes que aceptar las normas y la política de privacidad.' : nombre.length < 2 ? 'Escribe tu nombre.' : f.nac && !f.nac.value ? 'Pon tu fecha de nacimiento.' : f.nac && f.nac.value > addDays(-365 * 16 - 4) ? 'Hay que tener al menos 16 años.' :
      hcp != null && (hcp < -10 || hcp > 54) ? 'El hándicap va de -10 a 54.' : wa && !/^\+?[0-9 ]{9,17}$/.test(wa) ? 'El WhatsApp no parece válido.' : em && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(em) ? 'El correo no parece válido.' : '';
    if (bad) { er.hidden = false; er.textContent = bad; const d = f.querySelector('details.rest'); if (d && /hándicap|WhatsApp|correo no/i.test(bad)) d.open = true; return; }
    const btn = f.querySelector('[type=submit]'); btn.disabled = true;
    try {
      if (f.nac && EST && !EST.edad) { await q(SB.from('social_privado').insert({ user_id: ME.id, nacimiento: f.nac.value })); EST.edad = true; EST.mayor = f.nac.value <= addDays(-365 * 18 - 5); }
      let fotoPath = MYP ? MYP.foto || null : null;
      if (foto instanceof Blob) {
        const ext = foto.type === 'image/webp' ? 'webp' : 'jpg', path = ME.id + '/' + Date.now() + '.' + ext;
        const up = await SB.storage.from('avatares').upload(path, foto, { contentType: foto.type, upsert: false, cacheControl: '86400' });
        if (up.error) throw new Error('No se ha podido subir la foto. Inténtalo de nuevo.');
        fotoPath = path;
      } else if (foto === null) fotoPath = null;
      await q(SB.from('social_perfiles').upsert({ user_id: ME.id, nombre, hcp, provincia: f.prov.value || null, campos, bio: f.bio.value.trim() || null, visible: f.vis.checked, avisos: f.av.checked, foto: fotoPath }));
      if (foto !== 'keep') borrarFotos(fotoPath);
      if (wa || em) await q(SB.from('social_contacto').upsert({ user_id: ME.id, whatsapp: wa || null, email: em || null, publico: !!f.pub.checked }));
      else await q(SB.from('social_contacto').delete().eq('user_id', ME.id));
      // Mismo perfil en «Mi cuenta»: se guarda en la cuenta y Torneos lo usa al volver a la portada.
      const ano = f.nac && f.nac.value ? +f.nac.value.slice(0, 4) : nacAno || (pre && pre.nac) || null;
      const perfil = { ...(pre || {}), v: 1, hcp, nac: ano, sexo: f.sexo.value || null, fed: f.fed.value || null, clubs: socio.slice(), ts: Date.now() };
      const nd = { v: 1, sigo: { v: 1, clubs: [], prov: [] }, saved: [], played: [], ...(datos || {}), perfil, ts: Date.now() };
      await q(SB.from('perfiles').upsert({ user_id: ME.id, datos: nd, actualizado: new Date().toISOString() }));
      try { localStorage.setItem('banderin.perfil', JSON.stringify(perfil)); } catch (e3) { }
      await refresh(); toast(nuevo ? (pre ? '¡Ya estás en Social!' : '¡Perfil creado!') : 'Guardado'); location.hash = nuevo ? '#partidas' : '#perfil';
    } catch (e2) { er.hidden = false; er.textContent = errMsg(e2); btn.disabled = false; }
  };
}

// ───────── Solo con cuenta ─────────
function vGate() {
  setTab('');
  view.innerHTML = `<section class="shero gate"><p class="eb">Banderín Social</p><h1>Encuentra con quién jugar.</h1>
    <p>Social es para golfistas con cuenta de Banderín. Entra o crea tu cuenta gratis en un minuto.</p>
    <ul><li><i>1</i><span><b>Partidas abiertas</b> en tu zona, filtradas por tu hándicap.</span></li><li><i>2</i><span><b>Busca pareja</b> para los torneos por parejas de Banderín.</span></li><li><i>3</i><span><b>Amigos y perfil de jugador</b>, con tu contacto solo para quien tú quieras.</span></li></ul>
    <div class="acts"><button class="btn gold" data-login>Entrar</button><a class="btn ghost" href="/#perfil">Crear cuenta gratis</a></div></section>
    <p class="lede" style="text-align:center;margin-top:14px">Hay que tener al menos 16 años.</p><div id="esc"></div>`;
  window.BanderinEscaparate && window.BanderinEscaparate($('#esc'), { titulo: true });
}
function vPreparando() {
  setTab('');
  view.innerHTML = `<div class="empty glass panel" style="margin-top:18px"><b>Social se está preparando.</b>Muy pronto podrás crear tu perfil de jugador y publicar partidas.<br><button class="btn ghost" id="lo">Cerrar sesión</button></div>`;
  $('#lo').onclick = () => SB.auth.signOut();
}

// ───────── Navegación ─────────
async function route() {
  const h = decodeURIComponent(location.hash.slice(1)) || 'partidas';
  const [v, ...rest] = h.split('/'); const arg = rest.join('/');
  window.scrollTo(0, 0); clearInterval(CHAT);
  if (!ME || !SB) { vGate(); view.focus({ preventScroll: true }); return; }
  if (NOSQL) { vPreparando(); return; }
  try {
    if (v === 'partida') await vPartida(arg);
    else if (v === 'publicar') vPublicar(arg);
    else if (v === 'jugadores') await vJugadores(arg || null);
    else if (v === 'jugador') await vJugador(arg);
    else if (v === 'mias') await vMias();
    else if (v === 'perfil') await vPerfil(arg);
    else await vPartidas();
    if (v === 'partida' || v === 'jugador') $('#fab').hidden = true;
  } catch (e) { console.error(e); view.innerHTML = `<div class="empty"><b>Algo ha fallado.</b>${esc(errMsg(e))}</div>`; }
  view.focus({ preventScroll: true });
}
addEventListener('hashchange', route);
async function refresh() {
  try { await estado(); } catch (e) { console.error(e); }
  DEMO = false; chrome(); badges();
}
async function start() {
  if (!SB) { chrome(); route(); return; }
  const { data } = await SB.auth.getSession(); ME = data.session ? data.session.user : null;
  await refresh(); route();
  SB.auth.onAuthStateChange(async (ev, session) => {
    const u = session ? session.user : null;
    if ((u && u.id) === (ME && ME.id)) return;
    ME = u; await refresh();
    route(); // ya no se fuerza el formulario: el perfil se pide solo al publicar, unirse o añadir amigos
  });
}
start();
})();
