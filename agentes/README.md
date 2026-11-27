<!-- Generado por agentes/tools/generar.py desde agentes/org.json. No editar a mano: cambia org.json y regenera. -->

# Equipo de agentes de Banderín

Siete agentes que trabajan solos con tareas programadas de Claude. Cada uno tiene ficha (qué hace, qué puede y qué no), habilidades (cómo lo hace), memoria (lo que aprende), autonomía (cuánto puede hacer sin Juan) e histórico (qué ha hecho). Todos leen el [cerebro](../cerebro/README.md) y cumplen las [reglas](REGLAS.md).

**Estado de hoy:** [ESTADO.md](ESTADO.md) · **Preguntas para Juan:** [PREGUNTAS.md](PREGUNTAS.md) · **Pendientes de montaje:** [PENDIENTES.md](PENDIENTES.md)

| Agente | Para qué | Cuándo | Autonomía | Métrica |
|---|---|---|---|---|
| [Operaciones (vigilante)](equipo/operaciones.md) | Que Banderín funcione cada día | Lunes y jueves, 07:47 (la salud diaria la hace código) | A3 | Días con todo en verde. Incidencias detectadas por el agente antes que por Juan (objetivo: 100 %). |
| [Redes sociales](equipo/redes.md) | Que Banderín se conozca en Instagram | Martes, jueves y sábado, 10:23 | A3 | Visualizaciones medias por reel y seguidores nuevos por semana; a medio plazo, altas de avisos desde Instagram. |
| [Posicionamiento en Google](equipo/posicionamiento.md) | Que Banderín salga cuando alguien busca torneos | Días 1 y 15 de cada mes, 11:07 | A3 | Páginas indexadas y clics desde Google (Search Console, cuando esté conectado); mientras tanto, páginas útiles publicadas y sin errores. |
| [Analista y estratega de negocio](equipo/analista.md) | Saber si Banderín crece y por qué | Lunes, 08:16 (con los datos que deja el código a las 07:05) | A1 | Que cada lunes haya informe con datos fiables y tres decisiones; que Juan responda a la mayoría. |
| [Comercial y alianzas](equipo/comercial.md) | Encontrar socios que hagan crecer Banderín | Días 8 y 22 de cada mes, 11:43 | A1 | Oportunidades cualificadas por semana (objetivo 3) y respuestas positivas cuando Juan las envía. |
| [Atención a usuarios](equipo/atencion.md) | Que ningún usuario se quede sin respuesta | Lunes y jueves, 09:13 | A1 | Mensajes con borrador de respuesta en menos de 24 h (objetivo 100 %). |
| [Estratega de producto](equipo/estratega.md) | Que Banderín sea cada vez más útil | Jueves, 10:51 | A1 para proponer · A3 para construir lo aprobado | Propuestas aprobadas y construidas; efecto medido en la métrica norte o en uso. |

## Cómo funciona

**Sin IA, gratis (GitHub Actions):** actualización de torneos y avisos (3 veces al día), salud tras cada actualización (abre un issue «incidencia» si algo falla y GitHub te avisa por correo), métricas cada lunes, seguridad y copias. Ver [tareas/README.md](tareas/README.md).

**Con IA (tareas programadas de Claude, unas 10 a la semana):** operaciones lunes y jueves (arregla incidencias), atención lunes y jueves, redes martes, jueves y sábado, analista los lunes, estratega los jueves, posicionamiento los días 1 y 15, comercial los días 8 y 22.

## Cómo apruebas cosas (Juan)

- **Propuestas de mejora:** en GitHub → Issues, ponle la etiqueta `aprobada` (o `rechazada`) o escribe tu comentario. El estratega construye las aprobadas el jueves siguiente.
- **Correos:** quedan como borradores en tu Gmail. Los envías tú.
- **Preguntas:** en [PREGUNTAS.md](PREGUNTAS.md). Contesta debajo de cada una o díselo a Claude en el chat.
- **Decisiones semanales:** en el informe del lunes (`historico/semanas/`).

## Carpetas

| Carpeta | Qué hay |
|---|---|
| `org.json` | Fuente de verdad de agentes y habilidades (se edita aquí y se regenera) |
| `equipo/` | Una ficha por agente (generada) |
| `habilidades/` | Una ficha por habilidad (generada) |
| `memoria/` | Lecciones de cada agente (las escriben ellos) |
| `historico/registro.jsonl` | Una línea por ejecución |
| `historico/semanas/` | Informes semanales del analista |
| `autonomia.json` | Nivel A0–A4 de cada agente y cuándo sube o baja |
| `incidencias/` | Fallos abiertos y cerrados |
| `propuestas/` | Propuestas del estratega (y su issue) |
| `bandeja/` | Borradores comerciales para enviar |
| `comercial/`, `atencion/` | Archivos de trabajo de esos agentes |
| `tareas/` | Instrucciones exactas de cada tarea programada |
| `tools/` | generar.py, registrar.py, comprobar.py |
