# 07 · Métricas

**Métrica norte:** suscriptores activos a los avisos (tabla `suscriptores`, `estado='activo'`, D1).

| Métrica | Dónde se mide | Línea base | Fecha |
|---|---|---|---|
| Suscriptores activos | D1 `suscriptores` | 7 (varios de prueba) | 27/11/2026 |
| Altas pendientes de confirmar | D1 | 1 | 27/11/2026 |
| Suscriptores con perfil | D1 `perfil IS NOT NULL` | 3 | 27/11/2026 |
| Cuentas de usuario | Supabase → Authentication | [POR CONFIRMAR] | — |
| Torneos próximos | `site/data.js` | 1.151 | 27/11/2026 |
| Torneos sin provincia | `build.py` (log) | 18 | 27/11/2026 |
| Correos de aviso enviados al día | log de `actualizar.yml` | 4–5 | 26–27/11/2026 |
| Visitas a la web | Cloudflare Web Analytics | [POR CONFIRMAR] (falta token de lectura) | — |
| Seguidores Instagram, alcance por reel | Metricool | [POR CONFIRMAR] | — |

**Cómo se calcula cada semana:** lo hace el agente analista (`agentes/equipo/analista.md`) y lo deja en `agentes/historico/semanas/`.
