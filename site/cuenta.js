'use strict';
/* Banderín · cuentas de usuario (Supabase Auth, región Frankfurt).
   - Correo y contraseña con verificación del correo, o «Continuar con Google».
   - Lo que hoy se guarda en el navegador (perfil, lo que sigues, guardados,
     jugados y la llave de los avisos) se guarda también en la cuenta y se
     sincroniza entre dispositivos.
   - La librería de Supabase solo se descarga si hay sesión o si alguien abre
     «Entrar»: para el resto de visitantes la web no pesa más.
   Depende de app.js (raw, store, PERF, SIGO, saved, played, AV, L, $, render…). */

const CU = window.CUENTA || {};
// Para los avisos con un toque: correo verificado de la sesión y su token (solo viajan a /api/avisos/cuenta).
window.cuEmail = () => (USER && USER.email_confirmed_at ? USER.email : '');
window.cuSesion = async () => {
  if (!SB || !USER || !USER.email_confirmed_at) return null;
  const { data } = await SB.auth.getSession();
  return data && data.session ? { email: USER.email, tok: data.session.access_token } : null;
};
let SB = null, USER = null, cuSaveT = null, cuApplying = false, cuMode = 'entrar';
const cuOn = () => !!(CU.url && CU.key);
const cuRef = () => { try { return new URL(CU.url).hostname.split('.')[0]; } catch (e) { return ''; } };
const cuHasSession = () => { try { return !!localStorage.getItem('sb-' + cuRef() + '-auth-token'); } catch (e) { return false; } };
const cuBack = () => location.origin + (LANG === 'en' ? '/en/' : '/');

function cuLoad() {
  if (SB) return Promise.resolve(SB);
  return new Promise((ok, ko) => {
    const s = document.createElement('script');
    s.src = '/vendor/supabase.js';
    s.onload = () => {
      SB = window.supabase.createClient(CU.url, CU.key, {
        auth: { flowType: 'pkce', persistSession: true, autoRefreshToken: true, detectSessionInUrl: true },
      });
      SB.auth.onAuthStateChange((ev, session) => {
        const u = session ? session.user : null;
        const changed = (u && u.id) !== (USER && USER.id);
        USER = u;
        if (ev === 'PASSWORD_RECOVERY') cuOpen('nueva');
        if (changed && USER) cuPull();
        cuDraw();
      });
      ok(SB);
    };
    s.onerror = ko;
    document.head.appendChild(s);
  });
}

// Token anti-robots para Supabase (solo si Turnstile está configurado; Supabase lo exige al activar su CAPTCHA).
async function cuCaptcha() { const t = window.botToken ? await window.botToken() : ''; return t ? { captchaToken: t } : {}; }

/* ---------- datos: local ⇄ cuenta ---------- */
function cuLocal() {
  return { v: 1, perfil: PERF || null, sigo: SIGO, saved: [...saved], played: [...played.values()],
           avisos: AV && AV.tok ? { tok: AV.tok, email: AV.email || '' } : null, ts: Date.now() };
}
function cuMerge(a, b) {  // a = local, b = cuenta
  const out = { v: 1 };
  const pa = a.perfil, pb = b.perfil;
  out.perfil = !pa ? pb || null : !pb ? pa : ((pa.ts || 0) >= (pb.ts || 0) ? pa : pb);
  const sa = a.sigo || {}, sb = b.sigo || {};
  out.sigo = { v: 1, clubs: [...new Set([...(sb.clubs || []), ...(sa.clubs || [])])], prov: [...new Set([...(sb.prov || []), ...(sa.prov || [])])] };
  out.saved = [...new Set([...(b.saved || []), ...(a.saved || [])])];
  const pm = new Map((b.played || []).map(p => [p.url, p]));
  (a.played || []).forEach(p => pm.set(p.url, p));
  out.played = [...pm.values()];
  out.avisos = a.avisos || b.avisos || null;
  out.ts = Date.now();
  return out;
}
function cuApply(d) {
  cuApplying = true;
  try {
    PERF = d.perfil || null; if (PERF) raw.set('perfil', PERF); else raw.del('perfil');
    SIGO = d.sigo && Array.isArray(d.sigo.clubs) ? d.sigo : { v: 1, clubs: [], prov: [] }; raw.set('sigo', SIGO);
    saved.clear(); (d.saved || []).forEach(u => saved.add(u)); store.set('saved', [...saved]);
    played.clear(); (d.played || []).forEach(p => p && p.url && played.set(p.url, p)); savePlayed();
    if (d.avisos && d.avisos.tok && !(AV && AV.tok)) { AV = { tok: d.avisos.tok, email: d.avisos.email }; raw.set('avisos', AV); }
  } finally { cuApplying = false; }
  render(); renderQuick(); markMe(); if (typeof drawAvisos === 'function') drawAvisos(); if (typeof avFabSync === 'function') avFabSync();
  if (location.hash === '#perfil') renderPerfil();
}
async function cuPull() {
  if (!SB || !USER) return;
  const { data, error } = await SB.from('perfiles').select('datos').eq('user_id', USER.id).maybeSingle();
  if (error) { console.warn('cuenta', error.message); return; }
  const merged = data ? cuMerge(cuLocal(), data.datos || {}) : cuLocal();
  cuApply(merged);
  await cuPush(merged);
  if (typeof syncAvisos === 'function') syncAvisos();
}
async function cuPush(d) {
  if (!SB || !USER) return;
  const { error } = await SB.from('perfiles').upsert({ user_id: USER.id, datos: d || cuLocal(), actualizado: new Date().toISOString() });
  if (error) console.warn('cuenta', error.message);
}
function cuSoon() { if (!USER || cuApplying) return; clearTimeout(cuSaveT); cuSaveT = setTimeout(() => cuPush(), 1200); }
// Cada cambio que la web guarda en el navegador se guarda también en la cuenta.
{
  const rs = raw.set, rd = raw.del, ss = store.set;
  raw.set = function (k, v) { rs.call(raw, k, v); if (['perfil', 'sigo', 'avisos'].includes(k)) cuSoon(); };
  raw.del = function (k) { rd.call(raw, k); if (['perfil', 'sigo', 'avisos'].includes(k)) cuSoon(); };
  store.set = function (k, v) { ss.call(store, k, v); if (['saved', 'played'].includes(k)) cuSoon(); };
}
function cuClearLocal() {
  cuApplying = true;
  ['perfil', 'sigo', 'saved', 'played', 'avisos'].forEach(k => { raw.del(k); delete MEM[k]; });
  PERF = null; SIGO = { v: 1, clubs: [], prov: [] }; saved.clear(); played.clear(); AV = null;
  cuApplying = false;
  render(); renderQuick(); markMe(); if (typeof drawAvisos === 'function') drawAvisos(); if (typeof avFabSync === 'function') avFabSync();
  if (location.hash === '#perfil') renderPerfil();
}

/* ---------- ventana de acceso ---------- */
const CU_ERR = {
  'Invalid login credentials': 'Correo o contraseña incorrectos.',
  'Email not confirmed': 'Antes de entrar, confirma tu correo con el enlace que te enviamos.',
  'User already registered': 'Ya hay una cuenta con ese correo. Entra o recupera la contraseña.',
  'Password should be at least': 'La contraseña es demasiado corta.',
  'For security purposes': 'Por seguridad, espera un minuto antes de volver a intentarlo.',
  'rate limit': 'Demasiados intentos. Espera unos minutos.',
  'New password should be different': 'La nueva contraseña tiene que ser distinta de la anterior.',
  'weak': 'Esa contraseña es demasiado fácil de adivinar. Prueba con otra más larga.',
};
function cuMsg(e) {
  const m = (e && (e.message || e.error_description)) || '';
  for (const k in CU_ERR) if (m.indexOf(k) >= 0) return L(CU_ERR[k]);
  return L('No ha funcionado. Inténtalo de nuevo en unos minutos.');
}
function cuOpen(mode) {
  if (!cuOn()) return;
  cuMode = mode || 'entrar';
  ['entrar', 'crear', 'olvido', 'nueva', 'hecho'].forEach(m => { const el = $('cu-' + m); if (el) el.hidden = m !== cuMode; });
  $('cuTabs').hidden = !['entrar', 'crear'].includes(cuMode);
  document.querySelectorAll('#cuTabs button').forEach(b => b.setAttribute('aria-selected', String(b.dataset.m === cuMode)));
  document.querySelectorAll('#cuModal .perr').forEach(p => { p.hidden = true; });
  $('cuModal').hidden = false; document.body.classList.add('lock');
  const f = $('cu-' + cuMode).querySelector('input'); if (f) setTimeout(() => f.focus(), 60);
  cuLoad().catch(() => {});
}
function cuClose() { $('cuModal').hidden = true; if (!$('detail').classList.contains('open') && $('modal').hidden) document.body.classList.remove('lock'); }
function cuDone(title, text) { $('cuDoneT').textContent = title; $('cuDoneP').textContent = text; cuOpen('hecho'); }
function cuErr(id, e) { const p = $(id); p.textContent = typeof e === 'string' ? e : cuMsg(e); p.hidden = false; }
async function cuBusy(btn, fn) { btn.disabled = true; try { await fn(); } finally { btn.disabled = false; } }

$('cuX').onclick = cuClose;
$('cuDoneOk').onclick = cuClose;
$('cuModal').addEventListener('click', e => { if (e.target === $('cuModal')) cuClose(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape' && !$('cuModal').hidden) cuClose(); });
document.querySelectorAll('#cuTabs button').forEach(b => { b.onclick = () => cuOpen(b.dataset.m); });
document.querySelectorAll('[data-cu]').forEach(b => { b.onclick = e => { e.preventDefault(); cuOpen(b.dataset.cu); }; });
if (!CU.google) document.querySelectorAll('.cu-google, .cu-or').forEach(el => { el.hidden = true; });
document.querySelectorAll('.cu-google').forEach(b => {
  b.onclick = () => cuBusy(b, async () => {
    await cuLoad();
    sessionStorage.setItem('banderin.cu_vuelta', '1');
    const { error } = await SB.auth.signInWithOAuth({ provider: 'google', options: { redirectTo: cuBack() } });
    if (error) cuErr(cuMode === 'crear' ? 'cuCrearErr' : 'cuEntrarErr', error);
  });
});
$('cuEntrarF').onsubmit = e => {
  e.preventDefault();
  const em = $('cuEntrarEmail').value.trim(), pw = $('cuEntrarPw').value;
  if (!em || !pw) return cuErr('cuEntrarErr', L('Escribe tu correo y tu contraseña.'));
  cuBusy(e.submitter || $('cuEntrarF').querySelector('button[type=submit]'), async () => {
    await cuLoad();
    const { error } = await SB.auth.signInWithPassword({ email: em, password: pw, options: await cuCaptcha() });
    if (error) return cuErr('cuEntrarErr', error);
    $('cuEntrarPw').value = ''; cuClose(); location.hash = 'perfil';
  });
};
$('cuCrearF').onsubmit = e => {
  e.preventDefault();
  const em = $('cuCrearEmail').value.trim(), pw = $('cuCrearPw').value;
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em)) return cuErr('cuCrearErr', L('Revisa el correo: no parece válido.'));
  if (pw.length < 10) return cuErr('cuCrearErr', L('La contraseña necesita al menos 10 caracteres.'));
  if (!$('cuCrearOk').checked) return cuErr('cuCrearErr', L('Para crear la cuenta tienes que tener 14 años o más y aceptar la política de privacidad.'));
  cuBusy(e.submitter || $('cuCrearF').querySelector('button[type=submit]'), async () => {
    await cuLoad();
    const { data, error } = await SB.auth.signUp({ email: em, password: pw, options: { emailRedirectTo: cuBack() + '?cuenta=verificada', ...(await cuCaptcha()) } });
    if (error) return cuErr('cuCrearErr', error);
    $('cuCrearPw').value = '';
    if (data && data.session) { cuClose(); location.hash = 'perfil'; return; }
    cuDone(L('Revisa tu correo'), L('Te hemos enviado un enlace a {e} para verificar tu cuenta. Después podrás entrar con tu contraseña.', { e: em }));
  });
};
$('cuOlvidoF').onsubmit = e => {
  e.preventDefault();
  const em = $('cuOlvidoEmail').value.trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em)) return cuErr('cuOlvidoErr', L('Revisa el correo: no parece válido.'));
  cuBusy(e.submitter || $('cuOlvidoF').querySelector('button[type=submit]'), async () => {
    await cuLoad();
    const { error } = await SB.auth.resetPasswordForEmail(em, { redirectTo: cuBack() + '?cuenta=nueva', ...(await cuCaptcha()) });
    if (error) return cuErr('cuOlvidoErr', error);
    cuDone(L('Revisa tu correo'), L('Si hay una cuenta con {e}, te llegará un enlace para elegir una contraseña nueva.', { e: em }));
  });
};
$('cuNuevaF').onsubmit = e => {
  e.preventDefault();
  const a = $('cuNuevaPw').value, b = $('cuNuevaPw2').value;
  if (a.length < 10) return cuErr('cuNuevaErr', L('La contraseña necesita al menos 10 caracteres.'));
  if (a !== b) return cuErr('cuNuevaErr', L('Las dos contraseñas no coinciden.'));
  cuBusy(e.submitter || $('cuNuevaF').querySelector('button[type=submit]'), async () => {
    await cuLoad();
    const { error } = await SB.auth.updateUser({ password: a });
    if (error) return cuErr('cuNuevaErr', error);
    $('cuNuevaPw').value = $('cuNuevaPw2').value = '';
    cuDone(L('Contraseña cambiada'), L('Ya puedes usar tu nueva contraseña.'));
  });
};

/* ---------- tarjeta «Cuenta» en Mi perfil y botón de la cabecera ---------- */
function cuDraw() {
  if (typeof window.drawAvisos === 'function') try { window.drawAvisos(); } catch (e) {}
  const box = $('pcuenta'); if (!box) return;
  $('pcuSoon').hidden = cuOn();
  $('pcuOff').hidden = !!USER || !cuOn();
  $('pcuOn').hidden = !USER;
  $('pcuLegacy').hidden = cuOn();
  if (USER) {
    $('pcuEmail').textContent = USER.email || '';
    const g = (USER.app_metadata && (USER.app_metadata.providers || [USER.app_metadata.provider])) || [];
    $('pcuVia').textContent = g.includes('google') ? L('Con Google') : L('Con correo y contraseña');
    $('pcuPw').hidden = !g.includes('email');
  }
  if (typeof pLayout === 'function') pLayout();
  const me = $('me');
  if (me) {
    me.classList.toggle('logged', !!USER);
    const sp = me.querySelector('span');
    if (sp) sp.textContent = USER ? L('Mi cuenta') : L('Mi perfil');
  }
}
$('pcuPw').onclick = () => cuOpen('nueva');
$('pcuSalir').onclick = () => cuBusy($('pcuSalir'), async () => {
  await cuLoad(); await cuPush(); await SB.auth.signOut(); USER = null; cuClearLocal(); cuDraw();
});
$('pcuBorrar').onclick = () => {
  const b = $('pcuBorrar');
  if (!b.classList.contains('confirm')) { b.classList.add('confirm'); b.textContent = L('Pulsa otra vez: se borra todo y no se puede deshacer'); return; }
  cuBusy(b, async () => {
    await cuLoad();
    if (AV && AV.tok) await api('/api/avisos/baja', { method: 'POST', tok: AV.tok }).catch(() => {});
    const { error } = await SB.rpc('borrar_mi_cuenta');
    if (error) { b.textContent = L('No se ha podido borrar. Inténtalo de nuevo.'); return; }
    await SB.auth.signOut().catch(() => {});
    USER = null; cuClearLocal(); b.classList.remove('confirm'); b.textContent = L('Eliminar mi cuenta');
    cuDone(L('Cuenta eliminada'), L('Hemos borrado tu cuenta y todos sus datos.'));
  });
};

/* ---------- arranque ---------- */
(function cuStart() {
  cuDraw();
  if (!cuOn()) return;
  const q = new URLSearchParams(location.search);
  const back = q.has('code') || q.has('error_description') || /access_token|error_description/.test(location.hash) || sessionStorage.getItem('banderin.cu_vuelta');
  if (!back && !cuHasSession()) return;
  cuLoad().then(async () => {
    const { data } = await SB.auth.getSession();
    USER = data && data.session ? data.session.user : null;
    const how = q.get('cuenta');
    if (q.has('code') || q.has('error_description') || how) {
      const err = q.get('error_description');
      history.replaceState(null, '', location.pathname + '#perfil');
      sessionStorage.removeItem('banderin.cu_vuelta');
      if (err) cuDone(L('No se ha podido entrar'), err);
      else if (how === 'nueva' && USER) cuOpen('nueva');
      else if (how === 'verificada' && !USER) cuDone(L('Correo verificado'), L('Tu cuenta está lista. Entra con tu correo y tu contraseña.'));
      route();
    }
    if (USER) cuPull();
    cuDraw();
  }).catch(() => {});
})();
