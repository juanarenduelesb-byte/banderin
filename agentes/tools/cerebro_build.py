#!/usr/bin/env python3
"""Genera oficina/brain.json (el cerebro de la oficina) a partir de este repositorio.
Adaptado de tools/brain_build.py de empresa-IA. Uso: python3 agentes/tools/cerebro_build.py
Lee los Markdown (cerebro/, agentes/, README, CLAUDE.md, marketing/, docs…), los trocea por secciones, saca enlaces,
las decisiones de cerebro/decisiones.md y las preguntas abiertas de agentes/PREGUNTAS.md, y construye el grafo."""
import json, os, re, sys, datetime
T = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, T)
ROOT = os.path.dirname(os.path.dirname(T))
SKIP = ('site/', 'oficina/', '.git/', 'node_modules/', 'agentes/tools/', '.github/')
MAX = 2200
def group(p):
    if '/' not in p: return 0
    if p.startswith('cerebro/'): return 1
    if p.startswith('agentes/equipo/') or p.startswith('agentes/habilidades/'): return 2
    if p.startswith('agentes/'): return 3
    return 4
def title_of(p, t):
    m = re.search(r'^#\s+(.+)$', t, re.M); return (m.group(1).strip() if m else os.path.basename(p)[:-3]).replace('`', '')
def summary_of(t):
    for para in re.split(r'\n\s*\n', t):
        x = para.strip()
        if x and not x.startswith(('#', '|', '```', '<', '-', '*', '>')): return re.sub(r'\s+', ' ', x)[:240]
    return ''
def chunks_of(text):
    out, head, buf = [], '', []
    def flush():
        body = '\n'.join(buf).strip()
        while len(body) > MAX:
            cut = body.rfind('\n\n', 0, MAX); cut = cut if cut > MAX // 3 else MAX
            out.append((head, body[:cut].strip())); body = body[cut:].strip()
        if body: out.append((head, body))
    for line in text.splitlines():
        m = re.match(r'^(#{1,3})\s+(.+)$', line)
        if m: flush(); buf = []; head = m.group(2).strip()
        else: buf.append(line)
    flush(); return out
def decisiones():
    t = open(os.path.join(ROOT, 'cerebro', 'decisiones.md'), encoding='utf-8').read(); res = []
    for m in re.finditer(r'^- \*\*(D-\d{3}) · ([^·]+?) · (.+?)\*\*\s*(.*)$', t, re.M):
        raw = m.group(4).strip(); est = 'Aprobada' if 'Aprobada' in raw else ('Propuesta' if 'ropuesta' in raw else '')
        res.append(dict(id=m.group(1), t=m.group(3).rstrip('.'), f={'Fecha': m.group(2).strip(), 'Decisión': m.group(3).rstrip('.'), 'Motivo': raw, 'Estado': est}, raw=m.group(3) + ' ' + raw))
    return res
def pendientes():
    t = open(os.path.join(ROOT, 'agentes', 'PREGUNTAS.md'), encoding='utf-8').read()
    ab = t.split('## Abiertas', 1)[-1].split('## Cerradas', 1)[0]; out = []
    for m in re.finditer(r'^- \*\*(\d{4}-\d{2}-\d{2}) · ([^·]+?) · (.+?)\*\*', ab, re.M):
        d = datetime.date.fromisoformat(m.group(1)) + datetime.timedelta(days=7)
        out.append([m.group(3).strip(), 'Juan (lo pide ' + m.group(2).strip() + ')', d.strftime('%d/%m/%Y')])
    return out
def main(dst):
    files = []
    for base, dirs, names in os.walk(ROOT):
        rel = os.path.relpath(base, ROOT); rel = '' if rel == '.' else rel + '/'
        if any(rel.startswith(s) for s in SKIP) or any(x.startswith('.') for x in rel.split('/')[:-1]): continue
        files += [rel + n for n in sorted(names) if n.endswith('.md')]
    files.sort(); ids = {p: 'd%02d' % i for i, p in enumerate(files)}; names = {os.path.basename(p): p for p in files}
    docs, chunks, links = [], [], set()
    for p in files:
        text = open(os.path.join(ROOT, p), encoding='utf-8').read()
        docs.append(dict(id=ids[p], p=p, t=title_of(p, text), g=group(p), s=summary_of(text), n=len(text)))
        for h, body in chunks_of(text): chunks.append(dict(d=ids[p], h=h, t=body))
        here = os.path.dirname(p)
        for tg in re.findall(r'\]\(([^)#\s]+\.md)', text):
            q = os.path.normpath(os.path.join(here, tg)).replace('\\', '/')
            if q in ids and q != p: links.add(tuple(sorted((ids[p], ids[q]))))
        for tg in re.findall(r'`([\w./-]+\.md)`', text):
            q = tg if tg in ids else names.get(os.path.basename(tg))
            if q in ids and q != p: links.add(tuple(sorted((ids[p], ids[q]))))
    dec = decisiones(); pend = pendientes()
    from org_data.procesos import PROCESOS
    procs = [[x['id'], x['nombre'], x['desc']] for x in PROCESOS]
    import grafo
    G, rotas = grafo.construir(docs, chunks, sorted(links), dec); A = grafo.analizar(G, chunks, rotas, dec)
    os.makedirs(os.path.join(ROOT, 'cerebro', 'grafo'), exist_ok=True)
    open(os.path.join(ROOT, 'cerebro', 'grafo', 'INFORME.md'), 'w', encoding='utf-8').write(grafo.informe(G, A, chunks))
    out = dict(built=datetime.date.today().isoformat(), docs=docs, links=sorted(links), chunks=chunks, decisions=dec, pending=pend, processes=procs, graph=grafo.a_json(G, A))
    json.dump(out, open(dst, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    print('%d documentos, %d secciones, %d enlaces, %d decisiones, %d pendientes · grafo: %d nodos' % (len(docs), len(chunks), len(links), len(dec), len(pend), len(G.nodes)))
if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'oficina', 'brain.json'))
