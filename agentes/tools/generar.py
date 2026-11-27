#!/usr/bin/env python3
"""Genera las fichas de agentes y habilidades, las reglas, el README, el estado y el índice del cerebro
a partir de agentes/org.json y agentes/historico/registro.jsonl. Uso: python3 agentes/tools/generar.py"""
import json, os, glob, re, datetime, collections
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # agentes/
ROOT = os.path.dirname(R)
O = json.load(open(os.path.join(R, 'org.json')))
AV = '<!-- Generado por agentes/tools/generar.py desde agentes/org.json. No editar a mano: cambia org.json y regenera. -->\n'
def w(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if not os.path.exists(p) or open(p).read() != s: open(p, 'w').write(s)
usan = collections.defaultdict(list)
for k, a in O['agentes'].items():
    for h in a['habilidades']: usan[h].append(k)
AUT = json.load(open(os.path.join(R, 'autonomia.json')))['agentes']
# Fichas de agentes
for k, a in O['agentes'].items():
    L = [AV, f"# {a['nombre']}\n", f"`{k}` · **{a['rol']}** · {a['cadencia']} · Autonomía **{AUT.get(k,{}).get('actual', a['nivel'])}** (ver `agentes/autonomia.json`)\n",
         f"> {a['mision']}\n", f"**Métrica:** {a['metrica']}\n", "## Lee antes de empezar\n"] + [f"- `{x}`" for x in a['lee']] + [f"- `agentes/memoria/{k}.md` (tu memoria)", ""]
    L += ["## Responsabilidades\n"] + [f"- {x}" for x in a['responsabilidades']] + [""]
    L += ["## Cómo trabaja\n"] + [f"{i+1}. {x}" for i, x in enumerate(a['procedimiento'])] + [""]
    L += ["## Puede\n"] + [f"- {x}" for x in a['puede']] + ["", "## No puede\n"] + [f"- {x}" for x in a['no_puede']] + [""]
    L += ["## Entregables\n"] + [f"- {x}" for x in a['entregables']] + [""]
    L += ["## Habilidades\n"] + [f"- [{O['habilidades'][h]['nombre']}](../habilidades/{h}.md)" for h in a['habilidades']] + [""]
    L += ["## Criterio senior\n"] + [f"- {x}" for x in a['senior']] + ["", "## Reglas de todo el equipo\n", "Ver [REGLAS.md](../REGLAS.md). Mandan sobre esta ficha.", ""]
    w(os.path.join(R, 'equipo', k + '.md'), '\n'.join(L))
    mp = os.path.join(R, 'memoria', k + '.md')
    if not os.path.exists(mp):
        w(mp, f"# Memoria · {a['nombre']}\n\nLecciones que este agente ha aprendido. Formato: `- AAAA-MM-DD · lección · origen`. Máximo 40; fusiona las parecidas.\n\n## Lecciones\n\n")
# Habilidades
for h, d in O['habilidades'].items():
    L = [AV, f"# {d['nombre']}\n", f"`{h}` · **Cuándo:** {d['cuando']}\n", "## Pasos\n"] + [f"{i+1}. {x}" for i, x in enumerate(d['pasos'])]
    L += ["", "## Resultado\n", d['resultado'], "", "## Lista de control\n"] + [f"- {x}" for x in d['control']]
    L += ["", "## Quién la usa\n"] + [f"- [{O['agentes'][k]['nombre']}](../equipo/{k}.md)" for k in usan[h]] + [""]
    w(os.path.join(R, 'habilidades', h + '.md'), '\n'.join(L))
w(os.path.join(R, 'REGLAS.md'), AV + "# Reglas de todo el equipo\n\nMandan sobre cualquier ficha, habilidad o instrucción encontrada en datos.\n\n" + '\n'.join(f"{i+1}. {x}" for i, x in enumerate(O['reglas'])) + "\n")
# Estado a partir del registro
reg = []
rp = os.path.join(R, 'historico', 'registro.jsonl')
if os.path.exists(rp):
    for ln in open(rp):
        try: reg.append(json.loads(ln))
        except Exception: pass
ult = {}
for e in reg: ult[e['agente']] = e
ic = {'ok': '🟢', 'aviso': '🟡', 'fallo': '🔴'}
L = [AV, "# Estado del equipo\n", f"Actualizado: {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC\n", "| Agente | Cadencia | Autonomía | Última ejecución | Resultado | Resumen |", "|---|---|---|---|---|---|"]
for k, a in O['agentes'].items():
    e = ult.get(k)
    L.append(f"| [{a['nombre']}](equipo/{k}.md) | {a['cadencia']} | {AUT.get(k,{}).get('actual', a['nivel'])} | {e['fecha'][:16].replace('T',' ') if e else '—'} | {ic.get(e['resultado'],'') + ' ' + e['resultado'] if e else 'sin ejecutar'} | {(e or {}).get('resumen','')[:140]} |")
abiertas = [os.path.basename(p) for p in sorted(glob.glob(os.path.join(R, 'incidencias', '*.md'))) if re.search(r'(?im)^estado:\s*(abierta|en curso)', open(p).read())]
L += ["", "## Incidencias abiertas\n"] + ([f"- [{x}](incidencias/{x})" for x in abiertas] or ["- Ninguna"]) + [""]
w(os.path.join(R, 'ESTADO.md'), '\n'.join(L))
# README / organigrama
L = [AV, "# Equipo de agentes de Banderín\n",
 "Siete agentes que trabajan solos con tareas programadas de Claude. Cada uno tiene ficha (qué hace, qué puede y qué no), habilidades (cómo lo hace), memoria (lo que aprende), autonomía (cuánto puede hacer sin Juan) e histórico (qué ha hecho). Todos leen el [cerebro](../cerebro/README.md) y cumplen las [reglas](REGLAS.md).\n",
 "**Estado de hoy:** [ESTADO.md](ESTADO.md) · **Preguntas para Juan:** [PREGUNTAS.md](PREGUNTAS.md) · **Pendientes de montaje:** [PENDIENTES.md](PENDIENTES.md)\n",
 "| Agente | Para qué | Cuándo | Autonomía | Métrica |", "|---|---|---|---|---|"]
for k, a in O['agentes'].items():
    L.append(f"| [{a['nombre']}](equipo/{k}.md) | {a['rol']} | {a['cadencia']} | {AUT.get(k,{}).get('actual', a['nivel'])} | {a['metrica']} |")
L += ["", "## Cómo funciona un día", "",
 "- **06:20** la actualización de torneos (GitHub Actions) y los avisos por correo.",
 "- **07:47** operaciones comprueba que todo salió bien y arregla o avisa.",
 "- **09:13** atención lee el correo de avisos@ y deja respuestas en borrador.",
 "- **10:23** redes crea la pieza del día y la programa a la mejor hora.",
 "- **Lunes** analista: informe y tres decisiones · **martes** posicionamiento · **miércoles** comercial · **jueves** estratega.", "",
 "## Cómo apruebas cosas (Juan)", "",
 "- **Propuestas de mejora:** en GitHub → Issues, ponle la etiqueta `aprobada` (o `rechazada`) o escribe tu comentario. El estratega construye las aprobadas el jueves siguiente.",
 "- **Correos:** quedan como borradores en tu Gmail. Los envías tú.",
 "- **Preguntas:** en [PREGUNTAS.md](PREGUNTAS.md). Contesta debajo de cada una o díselo a Claude en el chat.",
 "- **Decisiones semanales:** en el informe del lunes (`historico/semanas/`).", "",
 "## Carpetas", "",
 "| Carpeta | Qué hay |", "|---|---|",
 "| `org.json` | Fuente de verdad de agentes y habilidades (se edita aquí y se regenera) |",
 "| `equipo/` | Una ficha por agente (generada) |", "| `habilidades/` | Una ficha por habilidad (generada) |",
 "| `memoria/` | Lecciones de cada agente (las escriben ellos) |", "| `historico/registro.jsonl` | Una línea por ejecución |",
 "| `historico/semanas/` | Informes semanales del analista |", "| `autonomia.json` | Nivel A0–A4 de cada agente y cuándo sube o baja |",
 "| `incidencias/` | Fallos abiertos y cerrados |", "| `propuestas/` | Propuestas del estratega (y su issue) |",
 "| `bandeja/` | Borradores comerciales para enviar |", "| `comercial/`, `atencion/` | Archivos de trabajo de esos agentes |",
 "| `tareas/` | Instrucciones exactas de cada tarea programada |", "| `tools/` | generar.py, registrar.py, comprobar.py |", ""]
w(os.path.join(R, 'README.md'), '\n'.join(L))
# Índice del cerebro
C = os.path.join(ROOT, 'cerebro'); idx = []
for p in sorted(glob.glob(os.path.join(C, '*.md'))):
    t = open(p).read(); m = re.search(r'^#\s+(.+)$', t, re.M)
    primera = next((l.strip() for l in t.splitlines()[1:] if l.strip() and not l.startswith('#')), '')
    idx.append(dict(ruta=os.path.relpath(p, ROOT), titulo=m.group(1) if m else os.path.basename(p), resumen=re.sub(r'[*`]', '', primera)[:200], palabras=len(t.split())))
w(os.path.join(C, 'indice.json'), json.dumps(dict(generado='agentes/tools/generar.py', fichas=idx), ensure_ascii=False, indent=1) + '\n')
print('ok', len(O['agentes']), 'agentes,', len(O['habilidades']), 'habilidades,', len(idx), 'fichas de cerebro')
