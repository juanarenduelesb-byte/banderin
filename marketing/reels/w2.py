import sys; sys.path.insert(0, '/home/claude/reels')
OUT = 'banderin-viral-5-excusas-de-golfista.mp4'; TEMPO = 1.1
KEYS = ['excusas', 'invierno', 'diciembre', '379', 'entero', 'avisamos', 'gratis', 'caro', '35', 'cerca', '17', 'comunidades', 'banderín']
_ph = ["Excusas|de golfista|para no|jugar|torneos.", "Y por qué|no valen.", "«En invierno|no hay|torneos.»", "Solo|en diciembre,|379=trescientos setenta y nueve.", "«Nunca|me entero.»", "Te avisamos|gratis|cuando abre|la inscripción.",
       "«Es muy|caro.»", "35=Treinta y cinco|son gratis.", "«No hay|ninguno|cerca.»", "Hay torneos|en las|17=diecisiete|comunidades.", "Se acabaron|las excusas.", "Banderín."]
TOKENS = []
for i, p in enumerate(_ph):
    for w in p.split('|'):
        show, _, spoken = w.partition('='); TOKENS.append((show, len(spoken or show) + 1, i))
def ex(n, a, b, html):
    return dict(type='text', t0=a, t1=b, y=600, size=132, eyebrow=f'Excusa nº {n}', html=html, flash=True, stamp='NO VALE', stampAt=max(.5, b - a - .55), stampY=1120)
def SCENES(ph, DUR):
    return [
     dict(type='text', t0=0, t1=ph[2][0], y=560, size=128, stag=.1, eyebrow='Golfistas, esto va por vosotros', words=[['Excusas', 'gold'], ['para'], '/', ['no'], ['jugar'], '/', ['torneos.']], sub='Y por qué no valen.', flash=True),
     ex(1, ph[2][0], ph[3][0], '«En invierno<br>no hay <span class="gold it">torneos.</span>»'),
     dict(type='cal', t0=ph[3][0], t1=ph[4][0], y=170, start='2026-12-01', counts=DEC, step=(ph[4][0] - ph[3][0] - .6) / 31, ch=104, eyebrow='Diciembre de 2026', label='días <span class="gold it">con torneo.</span> 379 torneos.'),
     ex(2, ph[4][0], ph[5][0], '«Nunca<br>me <span class="gold it">entero.</span>»'),
     dict(type='notifs', t0=ph[5][0], t1=ph[6][0], y=640, items=[['ahora', 'Abre la inscripción', 'Torneo de Navidad Olivar · Madrid · 5 dic'], ['ahora', 'Cierra el 3 de diciembre', 'Torneo Navidad Vistabella · Alicante · 6 dic']]),
     ex(3, ph[6][0], ph[7][0], '«Es muy<br><span class="gold it">caro.</span>»'),
     dict(type='counter', t0=ph[7][0], t1=ph[8][0], to=35, dur=.9, eyebrow='De los que publican precio', label='torneos <span class="gold it">gratis.</span>', y=420),
     ex(4, ph[8][0], ph[9][0], '«No hay<br>ninguno <span class="gold it">cerca.</span>»'),
     dict(type='counter', t0=ph[9][0], t1=ph[10][0], to=17, dur=.8, eyebrow='Torneos en', label='<span class="gold it">comunidades.</span>', y=230, map=dict(x=40, y=760, s=.95, o=.9, wave=.9)),
     dict(type='text', t0=ph[10][0], t1=ph[11][0], y=640, size=150, align='center', stag=.12, flash=True, words=[['Se'], ['acabaron'], '/', ['las'], ['excusas.', 'gold']]),
     dict(type='end', t0=ph[11][0], t1=DUR + 1, html='¿Cuál era <span class="gold it">la tuya?</span>')]
import datetime
from rd import rng
DEC = [len(rng(x, x)) for x in [(datetime.date(2026, 12, 1) + datetime.timedelta(i)).isoformat() for i in range(31)]]
