import sys; sys.path.insert(0, '/home/claude/reels')
from rd import *
import datetime
OUT = 'banderin-viral-1-ni-un-dia-sin-golf.mp4'; TEMPO = 1.15
KEYS = ['entre', 'semana', 'ni', 'solo', 'día', 'torneo', '47', 'días', 'navidad', 'banderín', 'tuyo']
_ph = ["¿Crees|que no|hay|torneos|de golf|entre semana?", "Mira.", "Del|18=dieciocho|de noviembre|al|3=tres|de enero,", "no hay|ni un|solo|día|sin torneo.", "47=Cuarenta y siete|días seguidos.", "Navidad|incluida.", "Banderín.", "Busca|el tuyo."]
TOKENS = []
for i, p in enumerate(_ph):
    for w in p.split('|'):
        show, _, spoken = w.partition('='); TOKENS.append((show, len(spoken or show) + 1, i))
d0 = datetime.date(2026, 11, 18)
COUNTS = []
for i in range(47):
    x = (d0 + datetime.timedelta(i)).isoformat(); COUNTS.append(len(rng(x, x)))
assert min(COUNTS) >= 1, COUNTS
def SCENES(ph, DUR):
    step = (ph[5][0] - ph[2][0] - .35) / 37
    return [
     dict(type='text', t0=0, t1=ph[1][0], y=640, size=124, stag=.1, eyebrow='Golf en España', words=[['¿Crees'], ['que'], ['no'], ['hay'], '/', ['torneos'], ['entre', 'gold'], ['semana?', 'gold']], flash=True),
     dict(type='text', t0=ph[1][0], t1=ph[2][0], y=760, size=240, align='center', stag=.1, flash=True, words=[['Mira.', 'gold']]),
     dict(type='cal', t0=ph[2][0], t1=ph[7][0], y=170, start='2026-11-18', counts=COUNTS, step=step, ch=104, eyebrow='Del 18 de noviembre al 3 de enero', label='días seguidos <span class="gold it">con torneo.</span>',
          tags={36: 'NOCHEB.', 37: 'NAVIDAD', 43: 'NOCHEV.', 44: 'AÑO NUEVO'}, flash=True),
     dict(type='end', t0=ph[7][0], t1=DUR + 1, html='Ni un día <span class="gold it">sin golf.</span>')]
