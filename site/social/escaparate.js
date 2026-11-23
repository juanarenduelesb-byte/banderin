// Banderín Social · escaparate: partidas abiertas (sin datos personales) y torneos por parejas,
// para la portada y para la entrada de Social. Quien no tiene cuenta solo ve campo, día y plazas.
(() => {
'use strict';
const EN = window.LANG === 'en';
const TR = { 'Banderín Social · Nuevo': 'Banderín Social · New', '¿Con quién juegas?': 'Who are you playing with?',
  'Encuentra gente para jugar, busca pareja para un torneo o publica tu partida y deja que te encuentren.': 'Find people to play with, look for a partner for a tournament, or post your round and let them find you.',
  'Crear cuenta gratis': 'Create a free account', 'Ver Social': 'See Social', 'Ver partidas': 'See rounds', 'Publicar partida': 'Post a round',
  'Partidas abiertas': 'Open rounds', 'Torneos por parejas: ¿te falta pareja?': 'Pairs tournaments: need a partner?', 'Partida': 'Round', 'Busca pareja': 'Partner wanted',
  'Completa': 'Full', 'libre': 'free', 'libres': 'free', 'Hándicap': 'Handicap', 'Cualquiera': 'Any', 'Unirme': 'Join', 'Busco pareja': 'I need a partner', 'Hoy': 'Today', 'Mañana': 'Tomorrow' };
const L = s => EN ? (TR[s] || s) : s;
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const CU = window.CUENTA || {};
const pad = n => String(n).padStart(2, '0'), iso = d => d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate());
const TODAY = iso(new Date()), TOM = (() => { const d = new Date(); d.setDate(d.getDate() + 1); return iso(d); })(), LIM = (() => { const d = new Date(); d.setDate(d.getDate() + 45); return iso(d); })();
const D = s => new Date(s + 'T12:00:00'), loc = EN ? 'en-GB' : 'es-ES';
const dow = s => new Intl.DateTimeFormat(loc, { weekday: 'short' }).format(D(s)).replace('.', ''), mon = s => new Intl.DateTimeFormat(loc, { month: 'short' }).format(D(s)).replace('.', '');
const hcp = h => String(Number(h).toFixed(1)).replace('.', EN ? '.' : ',');
const rango = p => p.hcp_min == null && p.hcp_max == null ? L('Cualquiera') : p.hcp_min != null && p.hcp_max != null ? hcp(p.hcp_min) + ' – ' + hcp(p.hcp_max) : p.hcp_min != null ? '≥ ' + hcp(p.hcp_min) : '≤ ' + hcp(p.hcp_max);
const tid = t => { let h = 2166136261; const u = t.url || ''; for (let i = 0; i < u.length; i++) { h ^= u.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0 } return h.toString(36) };
const logged = () => { try { const ref = new URL(CU.url).hostname.split('.')[0]; return !!localStorage.getItem('sb-' + ref + '-auth-token'); } catch (e) { return false; } };
const CSS = `.bs-rail{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;padding:2px 2px 10px;scrollbar-width:none}.bs-rail::-webkit-scrollbar{display:none}
.bs-card{flex:0 0 260px;scroll-snap-align:start;border-radius:24px;padding:14px;display:grid;grid-template-columns:58px 1fr;gap:12px;text-decoration:none;color:var(--ink);background:var(--card);border:1px solid var(--edge);box-shadow:var(--shadow);transition:transform .25s cubic-bezier(.3,1.3,.5,1)}
.bs-card:hover{transform:translateY(-3px)}
.bs-date{border-radius:16px;background:var(--hero);color:var(--hero-ink);text-align:center;padding:7px 2px 8px;align-self:start}
.bs-date small{display:block;font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--gold-l)}
.bs-date b{display:block;font-family:"Libre Caslon Display",Georgia,serif;font-weight:400;font-size:28px;line-height:1}
.bs-date span{display:block;font-size:11px;color:var(--hero-muted)}
.bs-card h4{margin:4px 0 2px;font-size:15px;line-height:1.25;letter-spacing:-.01em;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.bs-card p{margin:0;font-size:12.5px;color:var(--muted)}
.bs-tag{display:inline-block;font-size:11px;font-weight:700;border-radius:999px;padding:2px 8px;background:var(--tint);color:var(--accent)}
.bs-tag.g{background:rgba(201,168,106,.2);color:var(--gold)}
.bs-foot{display:flex;justify-content:space-between;align-items:center;margin-top:8px;font-size:12px;font-weight:600;color:var(--muted)}
.bs-foot em{font-style:normal;color:var(--accent);font-weight:700}
.bs-h{font-family:"Libre Caslon Display",Georgia,serif;font-weight:400;font-size:24px;color:var(--on-page);margin:22px 4px 10px}
.bs-hero{position:relative;overflow:hidden;border-radius:30px;padding:26px 26px 24px;background:radial-gradient(120% 150% at 100% 0%,#1E5A3E 0%,var(--hero) 58%);color:var(--hero-ink);box-shadow:0 30px 60px -30px rgba(0,0,0,.55);margin-top:40px}
.bs-hero::after{content:"";position:absolute;right:-50px;bottom:-70px;width:260px;height:260px;border-radius:50%;background:radial-gradient(circle,rgba(201,168,106,.32),transparent 70%);pointer-events:none}
.bs-hero .eb{font-size:12px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--gold-l);margin:0 0 6px}
.bs-hero h2{font-family:"Libre Caslon Display",Georgia,serif;font-weight:400;font-size:clamp(30px,4vw,44px);line-height:1.02;margin:0 0 8px;color:var(--hero-ink)}
.bs-hero p.t{margin:0;color:var(--hero-muted);font-size:16px;max-width:520px}
.bs-acts{display:flex;gap:8px;flex-wrap:wrap;margin-top:16px;position:relative;z-index:1}
.bs-btn{height:44px;padding:0 18px;border-radius:999px;display:inline-flex;align-items:center;font-size:15px;font-weight:600;text-decoration:none;border:1px solid rgba(244,241,232,.3);color:var(--hero-ink)}
.bs-btn.g{background:linear-gradient(180deg,#D9BC7E,#B8955A);color:#1B1408;border-color:transparent}`;
function css() { if (document.getElementById('bs-css')) return; const s = document.createElement('style'); s.id = 'bs-css'; s.textContent = CSS; document.head.append(s); }
const card = (f, h, tag, g, title, sub, foot, href) => `<a class="bs-card" href="${esc(href)}"><div class="bs-date"><small>${esc(dow(f))}</small><b>${D(f).getDate()}</b><span>${esc(mon(f))}${h ? ' · ' + esc(h.slice(0, 5)) : ''}</span></div><div><span class="bs-tag${g ? ' g' : ''}">${esc(tag)}</span><h4>${esc(title)}</h4><p>${esc(sub)}</p><div class="bs-foot">${foot}</div></div></a>`;
async function partidas() {
  if (!CU.url) return [];
  try {
    const r = await fetch(CU.url + '/rest/v1/rpc/social_escaparate', { method: 'POST', headers: { apikey: CU.key, Authorization: 'Bearer ' + CU.key, 'Content-Type': 'application/json' }, body: '{}' });
    if (!r.ok) return [];
    const d = await r.json(); return Array.isArray(d) ? d : [];
  } catch (e) { return []; }
}
function parejas() {
  return (window.TORNEOS || []).filter(t => t.form === 'Parejas' && t.s >= TODAY && t.s <= LIM && t.cat !== 'Juvenil' && t.cat !== 'Profesional').sort((a, b) => a.s.localeCompare(b.s)).slice(0, 10);
}
async function rails(el, o = {}) {
  css();
  const ps = await partidas(), ts = parejas(); let h = '';
  if (ps.length) h += `<h3 class="bs-h">${L('Partidas abiertas')}</h3><div class="bs-rail">${ps.map(p => card(p.fecha, p.hora, p.tipo === 'torneo' ? L('Busca pareja') : L('Partida'), p.tipo === 'torneo', p.tipo === 'torneo' && p.torneo ? p.torneo : p.campo, p.tipo === 'torneo' ? p.campo : (p.provincia || ''),
    `<span>${L('Hándicap')}: ${esc(rango(p))}</span><em>${p.libres > 0 ? p.libres + ' ' + L(p.libres === 1 ? 'libre' : 'libres') : L('Completa')}</em>`, '/social/')).join('')}</div>`;
  if (ts.length) h += `<h3 class="bs-h">${L('Torneos por parejas: ¿te falta pareja?')}</h3><div class="bs-rail">${ts.map(t => card(t.s, null, t.s === TODAY ? L('Hoy') : t.s === TOM ? L('Mañana') : t.prov, true, t.n, t.club, `<span>${esc(t.prov || '')}</span><em>${L('Busco pareja')} →</em>`, '/social/#publicar/t/' + tid(t))).join('')}</div>`;
  el.innerHTML = h;
}
window.BanderinEscaparate = rails;
// Portada: bloque de Social con su vista previa
const home = document.getElementById('bsoc');
if (home) {
  css(); const In = logged();
  home.innerHTML = `<div class="bs-hero"><p class="eb">${L('Banderín Social · Nuevo')}</p><h2>${L('¿Con quién juegas?')}</h2><p class="t">${L('Encuentra gente para jugar, busca pareja para un torneo o publica tu partida y deja que te encuentren.')}</p>
    <div class="bs-acts">${In ? `<a class="bs-btn g" href="/social/">${L('Ver partidas')}</a><a class="bs-btn" href="/social/#publicar">${L('Publicar partida')}</a>` : `<a class="bs-btn g" href="#perfil">${L('Crear cuenta gratis')}</a><a class="bs-btn" href="/social/">${L('Ver Social')}</a>`}</div></div><div id="bsocR"></div>`;
  rails(document.getElementById('bsocR'));
}
})();
