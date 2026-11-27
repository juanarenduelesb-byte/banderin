# Banderín · contexto para Claude

Banderín (banderin.es) reúne todos los torneos de golf amateur de España y dice cuáles encajan con cada jugador.
Fundador y único que decide: Juan Álvarez-Rendueles. Responde siempre en español de España, corto y directo, como un mentor exigente.

## Dónde está cada cosa
- `cerebro/` lo que hay que saber (empieza por `cerebro/README.md`); `cerebro/decisiones.md` es el registro de decisiones.
- `agentes/` el equipo de 7 agentes autónomos: reglas, fichas, habilidades, memoria, histórico, autonomía. Estado en `agentes/ESTADO.md`.
- `site/` la web (Cloudflare Pages desde `main`) · `pipeline/` actualización de torneos y avisos · `functions/`, `lib/` API · `db/` esquemas · `workers/` programador.
- `marketing/reels/` motor de reels.

## Reglas que no se rompen
- Acuerdo con Golf Directo (cerebro/01): solo lista y fechas; nada de precios, jugadores ni resultados; «golfdirecto.com» visible. Solo Juan les escribe.
- Robots.txt siempre; nunca suplantar un navegador.
- Nada de secretos ni datos personales en el repositorio (es público). Nunca copiar correos de suscriptores.
- Ningún agente envía mensajes a terceros, borra datos de usuarios, gasta dinero ni cambia secretos: lo propone.
- Cambios de código: `node pipeline/validate.mjs` y `python3 agentes/tools/comprobar.py --rapido` en verde antes de subir. Si cambias `site/index.html`, `python3 pipeline/seo.py`.
- Si cambias `agentes/org.json`, regenera con `python3 agentes/tools/generar.py`.
- Commit y push después de cada cambio, con `git pull --rebase` antes (la actualización automática sube datos a menudo).
- GitHub desde estas sesiones: API REST con `gh api` (GraphQL no está disponible).
