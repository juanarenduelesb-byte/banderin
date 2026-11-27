import sys; sys.path.insert(0, '/home/claude/reels')
from rd import *
OUT = 'banderin-reel-nuevo-1-este-finde.mp4'; TEMPO = 1.1
KEYS = ['136', 'torneos', '30', '18', 'andalucía', 'madrid', 'cataluña', 'alguno', 'todos', 'clic', 'inscribirte', 'banderín']
_ph = ["Este|fin|de|semana|se juegan|136=ciento treinta y seis|torneos|de golf|en España.", "30=Treinta,|en|Andalucía.", "18=Dieciocho,|en|Madrid.", "18=Dieciocho,|en|Cataluña.",
 "¿Y tú,|sabías|de|alguno?", "En|Banderín|los tienes|todos.", "Filtra|por tu|ciudad,|y en un|clic|tienes|fecha,|campo,", "y el enlace|para|inscribirte.", "Banderín.", "Encuentra|tu próximo|torneo."]
TOKENS = []
for i, p in enumerate(_ph):
    for w in p.split('|'):
        show, _, spoken = w.partition('='); TOKENS.append((show, len(spoken or show) + 1, i))
W = '2026-11-2[12]'
we = [t for t in rng('2026-11-21', '2026-11-22') if t.get('cl', '9') >= HOY and t['cat'] != 'Juvenil' and len(t['n']) <= 30 and len(t['club']) <= 32 and t['ccaa'] in ('Andalucía', 'Comunidad de Madrid', 'Cataluña', 'Galicia', 'Comunitat Valenciana', 'Castilla y León')]
ROWS = []; seen = set()
for t in sorted(we, key=lambda t: (t['s'], t['n'])):
    if t['ccaa'] in seen: continue
    seen.add(t['ccaa']); ROWS.append(row(t))
ROWS = ROWS[:5]
def SCENES(ph, DUR):
    mid = round(ph[0][0] + (ph[0][1] - ph[0][0]) * 0.62, 2)
    return [
     dict(type='counter', t0=0, t1=mid, to=136, dur=1.3, eyebrow='Sábado 21 · Domingo 22', label='torneos de golf <span class="gold it">este finde.</span>', y=230, map=dict(x=40, y=760, s=.95, o=.85, filter=W, wave=1.0), flash=True),
     dict(type='text', t0=mid, t1=ph[1][0], y=250, eyebrow='En toda España', html='Del Cantábrico <br>a <span class="gold it">Canarias.</span>', size=104, map=dict(x=40, y=640, s=1.08, o=1, filter=W, wave=.6)),
     dict(type='bars', t0=ph[1][0], t1=ph[4][0], y=300, eyebrow='Este finde, por comunidades', title='¿Dónde se <span class="gold it">juega?</span>', items=[['Andalucía', 30], ['Madrid', 18], ['Cataluña', 18], ['C. Valenciana', 16], ['Galicia', 13]]),
     dict(type='text', t0=ph[4][0], t1=ph[5][0], y=640, html='¿Y tú sabías<br>de <span class="gold it">alguno?</span>', size=150, flash=True),
     dict(type='cards', t0=ph[5][0], t1=ph[6][0], y=250, eyebrow='Banderín', title='Todos, en <span class="gold it">una lista.</span>', rows=ROWS, gap=.2),
     dict(type='phone', t0=ph[6][0], t1=ph[8][0], view='lista', q='Madrid', scroll=520, y=300),
     dict(type='end', t0=ph[8][0], t1=DUR + 1)]
