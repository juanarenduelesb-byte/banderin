import sys; sys.path.insert(0, '/home/claude/reels')
from rd import *
import random
OUT = 'banderin-viral-4-para-el-video.mp4'; TEMPO = 1.1; TAIL = 1.4
KEYS = ['reto', 'para', 'vídeo', 'torneo', 'juegas', 'tocado', 'comentarios', 'banderín']
_ph = ["Reto.", "Para|el vídeo|cuando|quieras.", "El torneo|que te|salga,|lo juegas|este|fin de semana.", "¿Cuál|te ha|tocado?", "Dímelo|en los|comentarios.", "Banderín."]
TOKENS = []
for i, p in enumerate(_ph):
    for w in p.split('|'):
        show, _, spoken = w.partition('='); TOKENS.append((show, len(spoken or show) + 1, i))
pool = [t for t in rng('2026-11-21', '2026-11-22') if t['cat'] not in ('Juvenil', 'Profesional') and not (t.get('cond') or {}).get('priv')
        and t.get('cl', '9') >= HOY and len(t['n']) <= 32 and 'Members' not in t['n'] and 'Socios' not in t['n'] and 'socios' not in t['n']]
random.Random(4).shuffle(pool)
ROWS = []; seen = set()
for t in pool:
    if t['club'] in seen: continue
    seen.add(t['club']); ROWS.append(row(t, (f"{t['price']:.0f} €" if t.get('price') else None) or t['ccaa'].replace('Comunidad de ', '').replace('Comunitat ', 'C. ').replace('Principado de ', '').replace('Illes ', '')[:12]))
ROWS = ROWS[:30]
def SCENES(ph, DUR):
    return [
     dict(type='text', t0=0, t1=ph[1][0], y=700, size=260, align='center', stag=.1, flash=True, words=[['RETO.', 'gold']]),
     dict(type='text', t0=ph[1][0], t1=ph[2][0], y=600, size=140, align='center', stag=.1, words=[['Para'], ['el'], '/', ['vídeo', 'gold'], ['cuando'], '/', ['quieras.', 'gold']]),
     dict(type='text', t0=ph[2][0], t1=ph[2][1] + .1, y=520, size=118, stag=.1, eyebrow='Las reglas', words=[['El'], ['torneo'], ['que'], '/', ['te'], ['salga,'], '/', ['lo', 'gold'], ['juegas', 'gold'], '/', ['este', 'gold'], ['finde.', 'gold']], flash=True),
     dict(type='shuffle', t0=ph[2][1] + .1, t1=ph[3][0], y=520, iv=.15, eyebrow='Sábado 21 · Domingo 22', title='Tu torneo <span class="gold it">es…</span>', rows=ROWS, flash=True),
     dict(type='text', t0=ph[3][0], t1=ph[5][0], y=600, size=140, align='center', stag=.12, flash=True, words=[['¿Cuál'], ['te'], '/', ['ha'], ['tocado?', 'gold']], sub='Comenta y etiqueta a tu pareja de juego.'),
     dict(type='end', t0=ph[5][0], t1=DUR + 1, html='Todos son reales. <span class="gold it">Inscríbete.</span>')]
