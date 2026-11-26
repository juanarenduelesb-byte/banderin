// Comprueba los datos nuevos antes de publicarlos. Uso: node validate.mjs nuevo/data.js nuevo/pasados.js anterior/data.js
import fs from 'node:fs';
const load = (p) => { const w = {}; new Function('window', fs.readFileSync(p, 'utf8'))(w); return w; };
const [nuevo, pas, prev] = process.argv.slice(2);
const N = load(nuevo), P = load(pas), fail = (m) => { console.error('NO SE PUBLICA: ' + m); process.exit(1); };
if (!Array.isArray(N.TORNEOS) || !N.TORNEOS.length) fail('TORNEOS vacío');
for (const t of N.TORNEOS) {
  if (!t.n || !/^\d{4}-\d{2}-\d{2}$/.test(t.s) || !t.ccaa || !t.cat || !t.src || !/^https:\/\//.test(t.url)) fail('torneo mal formado: ' + JSON.stringify(t).slice(0, 200));
}
if (!N.REVISION || !Array.isArray(N.CAMBIOS) || !Array.isArray(N.COBERTURA)) fail('faltan REVISION, CAMBIOS o COBERTURA');
if (!Array.isArray(P.PASADOS) || !P.PASADOS.length) fail('PASADOS vacío');
const srcs = new Set(N.TORNEOS.map((t) => t.src));
for (const s of ['NextCaddy']) if (!srcs.has(s)) fail('falta la fuente ' + s); // Golf Directo ya no se lee (26/11/2026): solo quedan sus torneos congelados
if (prev && fs.existsSync(prev)) {
  const A = load(prev);
  const a = (A.TORNEOS || []).length, n = N.TORNEOS.length;
  if (a && n < 0.6 * a) fail(`solo ${n} torneos frente a ${a} de ayer`);
  console.log(`Torneos próximos: ${n} (ayer ${a}). Pasados: ${P.PASADOS.length}. Cambios: ${N.CAMBIOS.length}.`);
}
console.log('Validación correcta');
