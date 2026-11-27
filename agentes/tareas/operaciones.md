# Tarea diaria · Operaciones (07:47)
Eres el agente de operaciones de Banderín. Sigue `agentes/tareas/COMUN.md` (arranque y cierre) y tu ficha `agentes/equipo/operaciones.md`.
1. `python3 agentes/tools/comprobar.py`. Si sale 0: registra ok con el resumen de las cifras (torneos, % sin provincia, avisos enviados) y termina.
2. Por cada 🟡 o 🔴: investiga la causa (`gh run view <id> --repo juanarenduelesb-byte/banderin --log`, el código del pipeline, `cerebro/09`).
3. Arréglalo si es pequeño y comprobable (habilidad arreglar-con-cuidado). Después de un arreglo de datos, relanza «Actualizar torneos» y espera a que termine (sondea cada 30 s, máx. 20 min) y vuelve a pasar comprobar.py.
4. Si no se puede arreglar: incidencia en `agentes/incidencias/` (habilidad incidencia) y, si afecta a usuarios hoy, la notificación empieza por «⚠️».
5. Revisa las incidencias abiertas: ¿alguna ya está resuelta? Ciérrala con la causa.
6. Golf Directo: si faltan 5 días o menos para que caduque el permiso escrito de `pipeline/red.py`, comprueba con WebFetch `https://www.golfdirecto.com/robots.txt` si permite a BanderinBot (o a todos) las rutas `/api/v2/public/tournament/last` y `/api/v2/public/club`. Si no lo permite, pregunta en PREGUNTAS.md y avisa a Juan; no amplíes la fecha del permiso tú.
