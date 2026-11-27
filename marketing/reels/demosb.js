// Supabase de demostración para el reel de Banderín Social: datos de ejemplo en memoria (no se publica).
(() => {
  const ME = { id: 'me', email: 'juan@ejemplo.es', user_metadata: {}, email_confirmed_at: '2026-01-01' };
  const today = new Date(); const iso = d => d.toISOString().slice(0, 10); const add = n => { const d = new Date(today); d.setDate(d.getDate() + n); return iso(d); };
  const H = (d, h, m) => { const x = new Date(today); x.setDate(x.getDate() + d); x.setHours(h, m, 0, 0); return x.toISOString(); };
  const sat = (() => { const d = today.getDay(); return (6 - d + 7) % 7 || 7; })();
  const P = (id, n, hcp, prov, campos, bio) => ({ user_id: id, nombre: n, hcp, provincia: prov, campos, bio, visible: true, creado: '', actualizado: id, foto: null });
  const DB = window.__DB = {
    social_privado: [{ user_id: 'me', nacimiento: '1990-03-10' }],
    social_perfiles: [
      P('me', 'Juan A.', 6.4, 'Madrid', ['Real Club de la Puerta de Hierro', 'Centro Nacional de Golf'], 'Sábados por la mañana. Fourball y scramble.'),
      P('u1', 'Lucía M.', 14.2, 'Madrid', ['Golf Olivar de la Hinojosa'], 'Juego los sábados temprano.'),
      P('u2', 'Carlos R.', 9.8, 'Madrid', ['Golf Santander'], 'Competición amateur.'),
      P('u3', 'Marta P.', 21.5, 'Madrid', ['Club de Golf Las Rejas'], 'Aprendiendo y disfrutando.'),
      P('u4', 'Álvaro G.', 18.1, 'Madrid', ['Centro Nacional de Golf'], 'Siempre con ganas de un fourball.'),
      P('u5', 'Elena S.', 12.7, 'Madrid', ['Golf La Moraleja'], ''),
      P('u6', 'Pablo T.', 24.0, 'Madrid', ['Club de Golf Somosaguas'], '')],
    social_contacto: [{ user_id: 'me', whatsapp: '600 000 000', email: null, publico: false }],
    social_amistades: [{ de: 'u1', para: 'me', estado: 'aceptada', creado: '' }, { de: 'u5', para: 'me', estado: 'pendiente', creado: '' }],
    social_partidas: [
      { id: 'x1', precio: 45, autor: 'u1', campo: 'Golf Olivar de la Hinojosa', provincia: 'Madrid', fecha: add(sat), hora: '09:30:00', tipo: 'partida', torneo: null, torneo_url: null, plazas: 2, hcp_min: 4, hcp_max: 24, nota: 'Partida tranquila, andando. Nos falta uno.', solo_amigos: false, cerrada: false, creado: '' },
      { id: 'x2', precio: 60, autor: 'u2', campo: 'Golf Santander', provincia: 'Madrid', fecha: add(sat), hora: '08:40:00', tipo: 'partida', torneo: null, torneo_url: null, plazas: 1, hcp_min: null, hcp_max: 18, nota: 'Stableford, buen ritmo.', solo_amigos: false, cerrada: false, creado: '' },
      { id: 'x3', precio: 35, autor: 'u3', campo: 'Club de Golf Las Rejas', provincia: 'Madrid', fecha: add(sat + 1), hora: '10:00:00', tipo: 'torneo', torneo: 'Scramble por parejas', torneo_url: null, plazas: 1, hcp_min: null, hcp_max: null, nota: 'Busco pareja para el scramble.', solo_amigos: false, cerrada: false, creado: '' },
      { id: 'x4', precio: 25, autor: 'u6', campo: 'Centro Nacional de Golf', provincia: 'Madrid', fecha: add(sat + 1), hora: '11:20:00', tipo: 'partida', torneo: null, torneo_url: null, plazas: 3, hcp_min: null, hcp_max: 36, nota: '9 hoyos y cerveza al acabar.', solo_amigos: false, cerrada: false, creado: '' },
      { id: 'm1', precio: 80, autor: 'me', campo: 'Real Club de la Puerta de Hierro', provincia: 'Madrid', fecha: add(sat + 7), hora: '09:00:00', tipo: 'partida', torneo: null, torneo_url: null, plazas: 2, hcp_min: 10, hcp_max: 24, nota: 'Fourball, salida a las 9.', solo_amigos: false, cerrada: false, creado: '' },
      { id: 'c1', precio: 55, autor: 'u4', campo: 'Golf La Moraleja', provincia: 'Madrid', fecha: add(sat), hora: '12:10:00', tipo: 'partida', torneo: null, torneo_url: null, plazas: 2, hcp_min: null, hcp_max: null, nota: 'Partida de los sábados.', solo_amigos: false, cerrada: false, creado: '' }],
    social_solicitudes: [
      { partida: 'x1', jugador: 'u5', mensaje: '', estado: 'aceptada', creado: '' },
      { partida: 'm1', jugador: 'u4', mensaje: '¡Me apunto! Hándicap 18.', estado: 'pendiente', creado: H(0, 9, 12) },
      { partida: 'c1', jugador: 'me', mensaje: '', estado: 'aceptada', creado: '' },
      { partida: 'c1', jugador: 'u2', mensaje: '', estado: 'aceptada', creado: '' }],
    social_bloqueos: [], social_denuncias: [],
    social_mensajes: [
      { id: 1, partida: 'c1', autor: 'u4', texto: '¡Bienvenidos! Salimos a las 12:10.', creado: H(0, 18, 2) },
      { id: 2, partida: 'c1', autor: 'u2', texto: 'Perfecto. ¿Quedamos 20 min antes en la cancha de prácticas?', creado: H(0, 18, 5) },
      { id: 3, partida: 'me', autor: 'me', texto: '', creado: '' }].filter(m => m.texto).concat([
      { id: 4, partida: 'c1', autor: 'me', texto: 'Hecho. Yo llevo bolas de sobra 😉', creado: H(0, 18, 7) },
      { id: 5, partida: 'c1', autor: 'u4', texto: 'Genial, nos vemos el sábado ⛳', creado: H(0, 18, 9) }]),
    perfiles: [{ user_id: 'me', datos: { perfil: { hcp: 6.4, sexo: 'M', fed: 'Comunidad de Madrid', clubs: [], ts: 1 } } }],
  };
  let seq = 100;
  const parseOr = s => { const groups = [...s.matchAll(/and\(([^)]*)\)/g)].map(m => m[1].split(',').map(c => { const [col, op, ...v] = c.split('.'); return [col, v.join('.')]; })); return r => groups.some(g => g.every(([c, v]) => String(r[c]) === v)); };
  class Q {
    constructor(t) { this.t = t; this.f = []; this.op = 'select'; this.o = []; this.l = null; this.s = false; this.ret = false; }
    select() { if (this.op !== 'select') this.ret = true; return this; }
    maybeSingle() { this.one = true; return this; }
    eq(c, v) { this.f.push(r => r[c] === v); return this; } neq(c, v) { this.f.push(r => r[c] !== v); return this; }
    gt(c, v) { this.f.push(r => r[c] > v); return this; } in(c, a) { this.f.push(r => a.includes(r[c])); return this; } gte(c, v) { this.f.push(r => String(r[c]) >= String(v)); return this; }
    ilike(c, p) { const s = p.replace(/%/g, '').toLowerCase(); this.f.push(r => String(r[c]).toLowerCase().includes(s)); return this; }
    or(s) { this.f.push(parseOr(s)); return this; }
    order(c, o = {}) { this.o.push([c, o.ascending !== false]); return this; } limit(n) { this.l = n; return this; } single() { this.s = true; return this; }
    insert(v) { this.op = 'insert'; this.v = v; return this; } update(v) { this.op = 'update'; this.v = v; return this; } delete() { this.op = 'delete'; return this; } upsert(v) { this.op = 'upsert'; this.v = v; return this; }
    then(res, rej) { try { const o = this.run(); if (this.one && o && Array.isArray(o.data)) o.data = o.data[0] || null; res(o); } catch (e) { res({ data: null, error: { message: e.message } }); } }
    run() {
      const T = DB[this.t]; const m = r => this.f.every(f => f(r));
      if (this.op === 'select') {
        let rows = T.filter(m);
        if (this.t === 'social_partidas') rows = rows.filter(r => !DB.social_bloqueos.some(b => (b.quien === 'me' && b.a_quien === r.autor) || (b.a_quien === 'me' && b.quien === r.autor)));
        if (this.t === 'social_contacto') rows = rows.filter(r => r.user_id === 'me' || r.publico || DB.social_amistades.some(a => a.estado === 'aceptada' && ((a.de === 'me' && a.para === r.user_id) || (a.para === 'me' && a.de === r.user_id))) ||
          DB.social_partidas.some(p => (p.autor === 'me' && DB.social_solicitudes.some(s => s.partida === p.id && s.jugador === r.user_id && s.estado === 'aceptada')) || (p.autor === r.user_id && DB.social_solicitudes.some(s => s.partida === p.id && s.jugador === 'me' && s.estado === 'aceptada'))));
        for (const [c, asc] of this.o.slice().reverse()) rows.sort((a, b) => (String(a[c] ?? '') < String(b[c] ?? '') ? -1 : String(a[c] ?? '') > String(b[c] ?? '') ? 1 : 0) * (asc ? 1 : -1));
        if (this.l) rows = rows.slice(0, this.l);
        rows = rows.map(r => ({ ...r }));
        return { data: this.s ? rows[0] : rows, error: null };
      }
      if (this.op === 'insert') {
        const v = { ...this.v };
        if (this.t === 'social_mensajes') { v.id = seq++; v.autor = 'me'; v.creado = new Date().toISOString(); }
        if (this.t === 'social_partidas') { v.id = 'n' + (seq++); v.autor = 'me'; v.cerrada = false; v.creado = new Date().toISOString(); }
        if (this.t === 'social_solicitudes') { v.estado = 'pendiente'; v.creado = new Date().toISOString(); if (DB.social_solicitudes.some(s => s.partida === v.partida && s.jugador === v.jugador)) throw new Error('duplicate key'); }
        if (this.t === 'social_amistades') { const rev = DB.social_amistades.find(a => a.de === v.para && a.para === v.de); if (rev) { rev.estado = 'aceptada'; return { data: null, error: null }; } v.estado = 'pendiente'; }
        if (this.t === 'social_bloqueos') { DB.social_amistades = DB.social_amistades.filter(a => !((a.de === v.quien && a.para === v.a_quien) || (a.de === v.a_quien && a.para === v.quien))); }
        if (this.t === 'social_privado') { const y = +v.nacimiento.slice(0, 4); if (today.getFullYear() - y < 16) throw new Error('edad'); }
        T.push(v); return { data: this.ret ? (this.s ? { ...v } : [{ ...v }]) : null, error: null };
      }
      if (this.op === 'upsert') { const k = 'user_id'; const i = T.findIndex(r => r[k] === this.v[k]); if (i >= 0) T[i] = { ...T[i], ...this.v }; else T.push({ creado: '', actualizado: '', ...this.v }); return { data: null, error: null }; }
      if (this.op === 'update') {
        if (this.t === 'social_solicitudes' && this.v.estado === 'aceptada') { const r0 = T.find(m); const p = DB.social_partidas.find(p => p.id === r0.partida); if (T.filter(s => s.partida === p.id && s.estado === 'aceptada').length >= p.plazas) throw new Error('plazas'); }
        T.filter(m).forEach(r => Object.assign(r, this.v)); return { data: null, error: null };
      }
      if (this.op === 'delete') { DB[this.t] = T.filter(r => !m(r)); return { data: null, error: null }; }
    }
  }
  window.supabase = { createClient: () => ({
    from: t => new Q(t),
    storage: { from: () => ({ upload: async (path, blob, o) => { window.__up = { path, type: blob.type, size: blob.size, o }; return { data: { path }, error: null }; },
      createSignedUrls: async (paths) => ({ data: paths.map(p => ({ path: p, signedUrl: 'data:image/gif;base64,R0lGODlhAQABAAAAACw=' })), error: null }),
      list: async () => ({ data: [{ name: 'viejo.webp' }], error: null }), remove: async (n) => { window.__rm = n; return { data: n, error: null }; } }) },
    rpc: async n => n === 'social_escaparate' ? ({ data: [], error: null }) : ({ data: { edad: true, mayor: true, perfil: true, avisos: true }, error: null }),
    auth: { getSession: async () => ({ data: { session: { user: ME } } }), onAuthStateChange: (cb) => { setTimeout(() => cb('SIGNED_IN', { user: ME }), 50); return ({ data: { subscription: { unsubscribe() {} } } }); }, signOut: async () => ({}), signInWithPassword: async () => ({}) },
  }) };
})();
