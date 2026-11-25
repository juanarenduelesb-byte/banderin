// Banderín · programador. Lanza la actualización de torneos tres veces al día (mañana, mediodía y noche).
// Existe porque las tareas programadas de GitHub llegan tarde o no llegan; las de Cloudflare son puntuales.
// No tiene página pública: solo se ejecuta con los horarios de wrangler.toml.
const URL = 'https://api.github.com/repos/juanarenduelesb-byte/banderin/actions/workflows/actualizar.yml/dispatches';

export default {
  async scheduled(event, env, ctx) {
    if (!env.GH_TOKEN) { console.log('Falta GH_TOKEN: no se lanza nada'); return; }
    const r = await fetch(URL, {
      method: 'POST',
      headers: { Authorization: 'Bearer ' + env.GH_TOKEN, Accept: 'application/vnd.github+json', 'User-Agent': 'banderin-programador', 'X-GitHub-Api-Version': '2022-11-28' },
      body: JSON.stringify({ ref: 'main', inputs: { auto: '1' } }),
    });
    console.log('Actualización lanzada', event.cron, r.status);
    if (r.status !== 204) throw new Error('GitHub respondió ' + r.status + ': ' + (await r.text()).slice(0, 200));
  },
  async fetch() { return new Response('No encontrado', { status: 404 }); },
};
