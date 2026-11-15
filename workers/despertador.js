// Banderín · despertador
// GitHub retrasa horas (o se salta) las tareas programadas de Actions. Este Worker de Cloudflare
// se ejecuta a su hora exacta con un «Cron Trigger» y le pide a GitHub que lance «Actualizar torneos».
// Lanzarlo de más es seguro: el proceso no publica si no hay cambios y no reenvía avisos.
//
// Configuración (panel de Cloudflare → Workers → banderin-despertador):
//   · Secreto GH_TOKEN: token «fine-grained» de GitHub solo para el repositorio banderin,
//     con el permiso «Actions: Read and write». Nada más.
//   · Triggers → Cron: 20 4 * * *   y   30 12 * * *   (hora UTC: 5:20 y 13:30 en Madrid en invierno)

const REPO = 'juanarenduelesb-byte/banderin';
const WORKFLOW = 'actualizar.yml';

async function lanzar(env) {
  const r = await fetch(`https://api.github.com/repos/${REPO}/actions/workflows/${WORKFLOW}/dispatches`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${env.GH_TOKEN}`,
      Accept: 'application/vnd.github+json',
      'User-Agent': 'banderin-despertador',
      'X-GitHub-Api-Version': '2022-11-28',
    },
    body: JSON.stringify({ ref: 'main' }),
  });
  if (r.status !== 204) throw new Error(`GitHub respondió ${r.status}: ${await r.text()}`);
}

export default {
  async scheduled(event, env, ctx) {
    ctx.waitUntil(lanzar(env));
  },
  // Visitar la dirección del Worker no lanza nada: solo dice si está vivo.
  async fetch() {
    return new Response('Banderín · despertador activo', { headers: { 'content-type': 'text/plain; charset=utf-8' } });
  },
};
