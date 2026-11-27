import sys; sys.path.insert(0, '/home/claude/reels')
from rd import *
OUT = 'banderin-reel-nuevo-2-puente-de-diciembre.mp4'; TEMPO = 1.1
KEYS = ['54', 'torneos', '21', 'andalucía', 'navidad', 'madrid', 'mallorca', 'galicia', 'rioja', 'lista', 'banderín']
_ph = ["Puente|de diciembre.", "54=Cincuenta y cuatro|torneos|de golf.", "21=Veintiuno,|solo|en Andalucía.", "¿Y torneos|de Navidad?", "En Madrid,|en Mallorca,|en Galicia,|en La Rioja.", "Todos|en una|lista.", "Con|fecha,|campo|y enlace.", "Banderín.", "Elige|el tuyo."]
TOKENS = []
for i, p in enumerate(_ph):
    for w in p.split('|'):
        show, _, spoken = w.partition('='); TOKENS.append((show, len(spoken or show) + 1, i))
P = '2026-12-0[5678]'
nav = {t['n']: t for t in T if 'avidad' in t['n'] and t['s'] >= '2026-12-05' and t['s'] <= '2026-12-08'}
want = ['Torneo Cesta de Navidad (2026)', 'Torneo de Navidad', 'Torneo de Navidad Olivar', 'XI Torneo de Navidad Concello de Boiro']
ROWS = [row(nav[n], 'Navidad') for n in want]
def SCENES(ph, DUR):
    return [
     dict(type='text', t0=0, t1=ph[1][0], y=560, html='Puente<br>de <span class="gold it">diciembre.</span>', size=150, map=dict(x=40, y=900, s=1.0, o=.6, filter=P, wave=.8), flash=True),
     dict(type='counter', t0=ph[1][0], t1=ph[2][0], to=54, dur=1.0, eyebrow='5 · 6 · 7 · 8 de diciembre', label='torneos de golf <span class="gold it">en el puente.</span>', y=230, map=dict(x=40, y=760, s=.95, o=.85, filter=P, wave=1.0)),
     dict(type='bars', t0=ph[2][0], t1=ph[3][0], y=300, eyebrow='Puente de diciembre, por comunidades', title='¿Dónde se <span class="gold it">juega?</span>', items=[['Andalucía', 21], ['C. Valenciana', 8], ['Cataluña', 6], ['Baleares', 5], ['Murcia', 4]]),
     dict(type='text', t0=ph[3][0], t1=ph[4][0], y=640, html='¿Y torneos<br>de <span class="gold it">Navidad?</span>', size=150, flash=True),
     dict(type='cards', t0=ph[4][0], t1=ph[6][0], y=250, eyebrow='Torneos de Navidad · 5 y 6 de diciembre', title='Madrid, Mallorca, <span class="gold it">Galicia, La Rioja.</span>', rows=ROWS, gap=.55),
     dict(type='phone', t0=ph[6][0], t1=ph[7][0], view='lista', q='Navidad', scroll=420, y=300),
     dict(type='end', t0=ph[7][0], t1=DUR + 1, html='Elige <span class="gold it">el tuyo.</span>')]
