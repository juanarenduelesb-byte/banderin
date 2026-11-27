import sys; sys.path.insert(0, '/home/claude/reels')
from rd import *
OUT = 'banderin-reel-donde-mas-torneos.mp4'; TEMPO = 1.1; G = 'gold'
KEYS = ['madrid', '614', 'málaga', '53', 'alicante', 'cádiz', '60', '68', 'murcia', '70', 'sábado', 'lunes', 'provincia', 'comentarios']
_ph = ["¿Dónde|se juegan|más|torneos|de golf|de España?", "Spoiler:", "no es|Madrid.", "Hemos|contado|los 614|torneos|de los|próximos|30 días.",
 "Quinta:", "Málaga,", "con 53.", "Cuarta|y tercera,|empatadas:", "Alicante|y Cádiz,|con 60.", "Segunda:", "Madrid,|con 68.",
 "Y primera…", "Murcia,|con 70.", "¿Y el día|con más|torneos?", "El sábado,|de lejos.", "El lunes,|casi|ninguno.",
 "¿Está|tu provincia?", "Dímelo|en|comentarios.", "Todos,|provincia|a provincia,|en|banderin.es"]
W = {'los 614': 26, '30 días.': 12, 'con 53.': 18, 'con 60.': 12, 'con 68.': 18, 'con 70.': 12, 'banderin.es': 20}
TOKENS = []
for i, p in enumerate(_ph):
    for w in p.split('|'): TOKENS.append((w, W.get(w, len(w) + 1), i))
def SCENES(ph, DUR):
    return [
     dict(type='text', t0=0, t1=ph[1][0], y=520, size=120, stag=.1, eyebrow='Torneos de golf en España', words=[['¿Dónde'], ['hay'], '/', ['más', G], ['torneos?', G]]),
     dict(type='text', t0=ph[1][0], t1=ph[3][0], y=600, size=170, stag=.12, eyebrow='Spoiler', words=[['No'], ['es'], '/', ['Madrid.', G]], flash=True),
     dict(type='counter', t0=ph[3][0], t1=ph[4][0], y=520, to=614, dur=2.4, eyebrow='Los próximos 30 días', label='torneos contados'),
     dict(type='text', t0=ph[4][0], t1=ph[7][0], y=600, size=170, stag=.1, eyebrow='Puesto 5', words=[['Málaga']], sub='53 torneos'),
     dict(type='text', t0=ph[7][0], t1=ph[9][0], y=560, size=150, stag=.12, eyebrow='Puestos 4 y 3 · empate', words=[['Alicante'], '/', ['y'], ['Cádiz']], sub='60 torneos cada una'),
     dict(type='text', t0=ph[9][0], t1=ph[11][0], y=600, size=170, stag=.1, eyebrow='Puesto 2', words=[['Madrid']], sub='68 torneos'),
     dict(type='text', t0=ph[11][0], t1=ph[13][0], y=580, size=200, stag=.1, eyebrow='Puesto 1', words=[['Murcia.', G]], sub='70 torneos', flash=True),
     dict(type='bars', t0=ph[13][0], t1=ph[16][0], y=260, eyebrow='Torneos por día de la semana', title='El sábado, <span class="gold it">de lejos.</span>', items=[['Lunes', 23], ['Martes', 75], ['Miércoles', 80], ['Jueves', 58], ['Viernes', 37], ['Sábado', 221], ['Domingo', 120]]),
     dict(type='text', t0=ph[16][0], t1=ph[18][0], y=540, size=130, stag=.1, eyebrow='Te leo en comentarios', words=[['¿Está'], '/', ['tu', G], ['provincia?', G]]),
     dict(type='end', t0=ph[18][0], t1=DUR + 1, html='Todos, <span class="gold it">provincia a provincia.</span>')]
