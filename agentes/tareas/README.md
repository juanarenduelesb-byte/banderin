# Tareas programadas de los agentes

Cada agente es una tarea programada de Claude (claude.ai → Tareas programadas) que arranca una sesión nueva, clona este repositorio y sigue `COMUN.md` y su archivo de tarea. Todas avisan al móvil al terminar y tienen aprobación automática.

| Agente | Cuándo (Madrid) | Id de la tarea |
|---|---|---|
| Operaciones | Lunes y jueves 07:47 | trig_01GhUaFpUMM2dy8pnmp5RVyW |
| Atención | Lunes y jueves 09:13 | trig_011gUcuFHoQAF2RyJNcy7nbD |
| Redes sociales | Martes, jueves y sábado 10:23 | trig_01Fmd7MMTrwaxtJaa6E6dBWo |
| Analista | Lunes 08:16 | trig_018uLTXM33xWgtKG7YGzDzkB |
| Posicionamiento | Días 1 y 15, 11:07 | trig_01Wa6bLfhTTwQheoXdUhAcgz |
| Comercial | Días 8 y 22, 11:43 | trig_01DLDUzXzRFMEThciYKwhatN |
| Estratega | Jueves 10:51 | trig_019bprbDWpKC5qpQ3GQazeBz |

Para cambiar lo que hace un agente, cambia su archivo aquí o su ficha en `org.json` (y regenera): la tarea programada solo apunta a estos archivos.

## Automatizaciones sin IA (GitHub Actions, gratis, sin tokens)

| Qué | Cuándo | Archivo |
|---|---|---|
| Actualizar torneos y enviar avisos | 06:20, 13:20 y 20:20 | `.github/workflows/actualizar.yml` |
| Salud: comprueba todo y abre/cierra issues «incidencia» (GitHub te avisa por correo) | Tras cada actualización y 09:35 | `.github/workflows/salud.yml` |
| Métricas semanales (D1, torneos) → `agentes/historico/` | Lunes 07:05 | `.github/workflows/metricas.yml` |
| Seguridad (cabeceras, HTTPS, actividad sospechosa) | Diario | `.github/workflows/vigilancia.yml` |
| Copia cifrada de D1 y Supabase | Semanal | `.github/workflows/copia.yml` |

Regla: lo que se puede comprobar o contar con código, lo hace el código. Los agentes de Claude solo entran para arreglar, escribir, crear o decidir.
