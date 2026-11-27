import sys; sys.path.insert(0, '/home/claude/reels')
from rd import *
OUT = 'banderin-reel-nuevo-3-torneos-juveniles.mp4'; TEMPO = 1.1
KEYS = ['104', 'juveniles', '25', 'hijo', 'competir', 'alevines', 'infantiles', 'cadetes', 'enlace', 'inscribirlo', 'banderín']
_ph = ["104=Ciento cuatro|torneos|juveniles|en España.", "25=Veinticinco,", "solo|este|fin de semana.", "¿Tu hijo|quiere|competir?", "Ya|tiene|dónde.", "Alevines,|infantiles,|cadetes.", "Fecha,", "campo,|y el enlace|para|inscribirlo.", "Banderín.", "Todos|los torneos|de golf,|en un|solo sitio."]
TOKENS = []
for i, p in enumerate(_ph):
    for w in p.split('|'):
        show, _, spoken = w.partition('='); TOKENS.append((show, len(spoken or show) + 1, i))
jw = [t for t in rng('2026-11-21', '2026-11-22') if t['cat'] == 'Juvenil']
ROWS = []; seen = set()
for t in jw:
    if t['club'] in seen: continue
    seen.add(t['club']); ROWS.append(row(t, 'Juvenil'))
ROWS = ROWS[:4]
def SCENES(ph, DUR):
    return [
     dict(type='counter', t0=0, t1=ph[2][0], to=104, dur=1.3, eyebrow='Torneos juveniles', label='por toda <span class="gold it">España.</span>', y=230, map=dict(x=40, y=760, s=.95, o=.85, wave=1.0), flash=True),
     dict(type='bars', t0=ph[2][0], t1=ph[3][0], y=300, eyebrow='Torneos juveniles, por comunidades', title='¿Dónde se <span class="gold it">juega?</span>', items=[['Andalucía', 25], ['Castilla y León', 23], ['Cataluña', 13], ['Madrid', 11], ['Galicia', 6]]),
     dict(type='text', t0=ph[3][0], t1=ph[4][0], y=560, html='¿Tu hijo quiere<br><span class="gold it">competir?</span>', size=140, flash=True),
     dict(type='text', t0=ph[4][0], t1=ph[5][0], y=640, html='Ya tiene<br><span class="gold it">dónde.</span>', size=170),
     dict(type='cards', t0=ph[5][0], t1=ph[7][0], y=250, eyebrow='Este finde · 21 de noviembre', title='Alevines, infantiles, <span class="gold it">cadetes.</span>', rows=ROWS, gap=.6),
     dict(type='phone', t0=ph[7][0], t1=ph[8][0], view='lista', q='Juvenil', scroll=420, y=300),
     dict(type='end', t0=ph[8][0], t1=DUR + 1)]
