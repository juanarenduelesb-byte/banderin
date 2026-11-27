import sys; sys.path.insert(0, '/home/claude/reels')
from rd import *
OUT = 'banderin-reel-nuevo-4-cuanto-cuesta.mp4'; TEMPO = 1.1
KEYS = ['cuesta', 'precio', '35', 'gratis', 'mitad', '50', 'euros', 'apuntarte', 'banderín']
_ph = ["¿Cuánto|cuesta|jugar|un torneo|de golf?", "De los|que publican|precio,|35=treinta y cinco|son gratis.", "Y la mitad|de los de pago,|cuestan|menos de|50=cincuenta|euros.", "Lo ves|antes|de apuntarte.", "Banderín.", "Todos|los torneos|de golf|de España."]
TOKENS = []
for i, p in enumerate(_ph):
    for w in p.split('|'):
        show, _, spoken = w.partition('='); TOKENS.append((show, len(spoken or show) + 1, i))
wk = [t for t in rng('2026-11-21', '2026-11-22') if t.get('price') is not None and t.get('cl', '9') >= HOY and t['cat'] != 'Juvenil']
ROWS = []; seen = set()
for t in sorted(wk, key=lambda t: t['price']):
    k = round(t['price'] // 20)
    if k in seen: continue
    seen.add(k); r = row(t, 'Gratis' if t['price'] == 0 else f"{t['price']:.0f} €"); ROWS.append(r)
ROWS = ROWS[:5]
def SCENES(ph, DUR):
    return [
     dict(type='text', t0=0, t1=ph[1][0], y=560, html='¿Cuánto cuesta<br>jugar un <span class="gold it">torneo?</span>', size=130, flash=True),
     dict(type='counter', t0=ph[1][0], t1=ph[2][0], to=35, dur=1.7, eyebrow='De los que publican precio', label='torneos <span class="gold it">gratis.</span>', y=330, flash=True),
     dict(type='bars', t0=ph[2][0], t1=ph[3][0], y=280, eyebrow='327 torneos con precio publicado', title='¿Cuánto <span class="gold it">cuestan?</span>', items=[['Gratis', 35], ['Menos de 20 €', 74], ['20 – 40 €', 29], ['40 – 60 €', 70], ['60 – 80 €', 74], ['Más de 80 €', 45]]),
     dict(type='cards', t0=ph[3][0], t1=ph[4][0], y=250, eyebrow='Este finde · el precio, a la vista', title='Lo ves <span class="gold it">antes de apuntarte.</span>', rows=ROWS, gap=.3),
     dict(type='end', t0=ph[4][0], t1=DUR + 1)]
