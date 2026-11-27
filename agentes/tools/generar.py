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
L += ["", "## Cómo funciona", "",
 "**Sin IA, gratis (GitHub Actions):** actualización de torneos y avisos (3 veces al día), salud tras cada actualización (abre un issue «incidencia» si algo falla y GitHub te avisa por correo), métricas cada lunes, seguridad y copias. Ver [tareas/README.md](tareas/README.md).", "",
 "**Con IA (tareas programadas de Claude, unas 10 a la semana):** operaciones lunes y jueves (arregla incidencias), atención lunes y jueves, redes martes, jueves y sábado, analista los lunes, estratega los jueves, posicionamiento los días 1 y 15, comercial los días 8 y 22.", "",
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
# Oficina: agentes.json con el mismo esquema que la oficina de empresa-IA
of = dict(generado='agentes/tools/generar.py', reglas_oficina=O['reglas'], departamentos=O.get('departamentos', {}), agentes={}, habilidades={})
for k, a in O['agentes'].items():
    of['agentes'][k] = dict(nombre=a['nombre'], rol=a['rol'], dep=a.get('dep', 'dir'), lead=a.get('lead', False), nivel=f"Autonomía {AUT.get(k,{}).get('actual', a['nivel'])} · {a['cadencia']}",
        mision=a['mision'], responsabilidades=a['responsabilidades'], entregables=a['entregables'], procedimiento=a['procedimiento'],
        reglas=a['no_puede'] + a.get('senior', [])[:0], habilidades=a['habilidades'], criterio=a.get('senior', []), errores=a.get('errores', []),
        kpis=a.get('kpis', [a['metrica']]), limites=a.get('limites', []) + a['no_puede'], colabora=a.get('colabora', []), especialista=a.get('especialista', []))
for h, d in O['habilidades'].items():
    of['habilidades'][h] = dict(nombre=d['nombre'], cuando=d['cuando'], pasos=d['pasos'], resultado=d['resultado'], control=d['control'])
os.makedirs(os.path.join(ROOT, 'oficina'), exist_ok=True)
w(os.path.join(ROOT, 'oficina', 'agentes.json'), json.dumps(of, ensure_ascii=False, indent=1) + '\n')
# Módulos que usa el grafo del cerebro (agentes/tools/org_data/)
od = os.path.join(R, 'tools', 'org_data'); os.makedirs(od, exist_ok=True)
w(os.path.join(od, '__init__.py'), '# Generado por generar.py\n')
w(os.path.join(od, 'agentes.py'), '# Generado por generar.py\nAGENTES = ' + repr([dict(id=k, nombre=a['nombre'], dep=a.get('dep', 'dir'), habilidades=a['habilidades'], colabora=[(c['id'], c['motivo']) for c in a.get('colabora', [])], especialista=[]) for k, a in O['agentes'].items()]) + '\nDEPS = ' + repr({k: v['nombre'] for k, v in O.get('departamentos', {}).items()}) + '\n')
w(os.path.join(od, 'habilidades.py'), '# Generado por generar.py\nHABILIDADES = ' + repr([dict(id=h, nombre=d['nombre']) for h, d in O['habilidades'].items()]) + '\n')
w(os.path.join(od, 'especialistas.py'), '# Generado por generar.py\nESPECIALISTAS = []\n')
FU = [('F-GD', 'Golf Directo (lista pública de torneos y clubes)'), ('F-NC', 'NextCaddy'), ('F-RFEG', 'RFEG'), ('F-FED', 'Calendarios de federaciones autonómicas')]
w(os.path.join(od, 'fuentes.py'), '# Generado por generar.py\nFUENTES = ' + repr([dict(id=i, titulo=t) for i, t in FU]) + '\n')
PR = [('P01', 'Actualizar torneos', 'actualizar.yml, 3 veces al día'), ('P02', 'Avisos por correo', 'avisos.py tras cada actualización'), ('P03', 'Salud', 'salud.yml tras cada actualización'),
      ('P04', 'Métricas semanales', 'metricas.yml, lunes'), ('P05', 'Vigilancia de seguridad', 'vigilancia.yml, diario'), ('P06', 'Copia de seguridad', 'copia.yml, semanal'),
      ('P07', 'Reels y carruseles', 'agente de redes'), ('P08', 'Atención a usuarios', 'agente de atención'), ('P09', 'Propuestas de mejora', 'agente estratega'),
      ('P10', 'Posicionamiento en Google', 'agente de posicionamiento'), ('P11', 'Alianzas', 'agente comercial'), ('P12', 'Informe semanal', 'agente analista')]
w(os.path.join(od, 'procesos.py'), '# Generado por generar.py\nPROCESOS = ' + repr([dict(id=i, nombre=n, depende=[], especialistas=[], desc=d) for i, n, d in PR]) + '\n')
w(os.path.join(ROOT, 'cerebro', 'procesos.md'), '# Procesos de Banderín\n\nLo que funciona solo, con su código o su agente.\n\n| Id | Proceso | Cómo |\n|---|---|---|\n' + ''.join(f'| {i} | {n} | {d} |\n' for i, n, d in PR))
# Oficina: bloque de datos de oficina/index.html (entre «DATOS DE …» y «ESTADO Y ALMACÉN»)
IP = os.path.join(ROOT, 'oficina', 'index.html')
if os.path.exists(IP):
    J = lambda x: json.dumps(x, ensure_ascii=False)
    DEPS_ = O.get('departamentos', {})
    blk = ['// ======================= DATOS DE BANDERÍN (generado por agentes/tools/generar.py desde agentes/org.json) =======================']
    blk.append('var DEP=' + J([dict(id=k, n=v['nombre'], c=v['color'], d=v['desc']) for k, v in DEPS_.items()]) + ';')
    blk.append('var SK=' + J({h: (d['cuando'] + ' ' + ' '.join(d['pasos']))[:420] for h, d in O['habilidades'].items()}) + ';')
    blk.append('var A=' + J([[k, a.get('dep', 'dir'), 1 if a.get('lead') else 0, a['nombre'], a['rol'], a['mision'], a['habilidades'], ' '.join(a.get('senior', [])[:2])] for k, a in O['agentes'].items()]) +
               '.map(function(a){return {id:a[0],dep:a[1],lead:!!a[2],n:a[3],r:a[4],does:a[5],skills:a[6],brief:a[7]}});')
    blk.append("function ag(id){return A.find(function(a){return a.id===id})}\nfunction dep(id){return DEP.find(function(d){return d.id===id})}\nfunction ini(n){return n.split(' ').filter(function(w){return w.length>2||/^[A-Z]/.test(w)}).slice(0,2).map(function(w){return w[0]}).join('').toUpperCase()}")
    BR = [
     'BANDERÍN (banderin.es): web gratuita con todos los torneos de golf amateur de España, actualizada tres veces al día, que dice qué torneos encajan con cada jugador. Fundador y único que decide: Juan Álvarez-Rendueles. Proyecto de Esclusa.',
     'ESTADO (27/11/2026): 1.151 torneos próximos (unos 876 de Golf Directo, el resto de NextCaddy y federaciones). 7 suscriptores activos a los avisos (varios de prueba). 0 ingresos. Meta propuesta: 300 suscriptores activos antes del 1/03/2027.',
     'ACUERDO CON GOLF DIRECTO (no se rompe nunca): solo la lista pública de torneos y la de clubes; solo fechas del torneo y de inscripción; nada de precios, jugadores ni resultados; «golfdirecto.com» visible junto al nombre. Solo Juan les escribe. Permiso escrito en red.py hasta el 3/12/2026; después manda su robots.txt.',
     'REGLAS: robots.txt siempre y sin suplantar navegadores. Nada de datos personales en el repositorio (es público). Ningún agente envía mensajes a terceros, borra datos de usuarios, gasta dinero ni toca secretos: lo propone y decide Juan.',
     'AUTOMÁTICO SIN IA: actualizar torneos y avisos (06:20, 13:20, 20:20), salud tras cada actualización (abre issues «incidencia»), métricas cada lunes, vigilancia de seguridad diaria, copia semanal.',
     'AGENTES PROGRAMADOS: operaciones (lun y jue), atención (lun y jue), redes (mar, jue, sáb), analista (lun), estratega (jue), posicionamiento (días 1 y 15), comercial (días 8 y 22). Las propuestas se aprueban con la etiqueta «aprobada» en GitHub.',
     'VOZ: español de España, tú, frases cortas, humor de golfista sin burla, datos reales y con fecha, cifras con punto de miles (1.151) y coma decimal (18,4). Nunca logos ni personajes de otras marcas.',
     'MARCA: verde campo #123323, crema #F4EFE3, oro #F2D27E. Tipografías: Libre Caslon Display, Public Sans, Instrument Sans.']
    blk.append('var BRAIN=' + J(BR) + ".join('\\n');")
    blk.append("var DOCS=[['readme','Cerebro',0,'Todo lo que hay que saber de Banderín.']];\nvar LINKS=[];")
    blk.append('var ROUT_DEF=' + J([
        dict(id='r1', name='Resumen de la semana', ag='analista', days=[1], h='09:30', task='Lee agentes/historico/semanas (el último informe) y resume en 5 líneas cómo va Banderín frente a la meta y qué tres decisiones esperan a Juan.'),
        dict(id='r2', name='Idea de la semana', ag='estratega', days=[4], h='12:00', task='Propón una idea de otro deporte que funcione en golf y que use datos que Banderín ya tiene, con cómo se mediría.'),
        dict(id='r3', name='Decisiones de la semana', ag='dec', days=[5], h='17:00', task='A partir de lo hecho esta semana, propone entradas para cerebro/decisiones.md de lo que parezca una decisión, marcadas como propuesta.')]) + ';')
    blk.append('var PLAN=' + J([['2026-11-27', 'Equipo de agentes en marcha'], ['2026-12-03', 'Caduca el permiso escrito de Golf Directo'], ['2026-12-15', 'Revisión de los agentes'], ['2027-01-15', 'Revisión de la meta'], ['2027-03-01', 'Meta: 300 suscriptores']]) + ';')
    blk.append("var CTL={'2026-12-03':'Golf Directo: robots.txt','2027-03-01':'Meta 300 suscriptores'};\nvar FEST={'2026-12-08':'Festivo','2026-12-25':'Navidad','2027-01-01':'Año Nuevo','2027-01-06':'Reyes'};\n")
    h = open(IP, encoding='utf-8').read()
    i = h.index('// ======================= DATOS DE'); j = h.index('// ======================= ESTADO Y ALMACÉN')
    h2 = h[:i] + '\n'.join(blk) + '\n' + h[j:]
    if h2 != h: open(IP, 'w', encoding='utf-8').write(h2)
    print('oficina: datos actualizados en index.html')
