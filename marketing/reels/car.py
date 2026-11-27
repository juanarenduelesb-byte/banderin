import sys, datetime; sys.path.insert(0, '/home/claude/reels')
from rd import *
OUT = 'banderin-reel-golf-caro.mp4'; TEMPO = 1.1; G = 'gold'
KEYS = ['carísimo', 'seguro', '314', '40', 'mitad', '129', '30', '11', '100', 'inscripción', 'socio', 'social', 'cuánto', 'comentarios', 'precio']
_ph = ["«El golf|es|carísimo.»", "¿Seguro?", "Hemos|mirado|los 314|torneos|de España|de los que|tenemos|el precio.", "La mitad|cuesta|40 €|o menos.",
 "129,", "30|o menos.", "Y solo|11|pasan|de 100.", "Ojo:", "es la|inscripción.", "Si no|eres|socio,|a veces|el green fee|va aparte.",
 "¿Y si|te falta|con quién|ir?", "En|Banderín|Social,", "cada|partida|dice|cuánto|cuesta|antes de|apuntarte.",
 "¿Cuánto|pagaste|por tu|último|torneo?", "Te leo|en|comentarios.", "Todos|los torneos,|con su|precio,|en|banderin.es"]
W = {'los 314': 22, '40 €': 12, '129,': 22, '30': 7, '11': 5, 'de 100.': 9, 'banderin.es': 20}
TOKENS = []
for i, p in enumerate(_ph):
    for w in p.split('|'): TOKENS.append((w, W.get(w, len(w) + 1), i))
H2 = datetime.date.today().isoformat()
P = [t for t in T if t['s'] >= H2 and isinstance(t.get('price'), (int, float)) and 8 <= t['price'] <= 30 and not any(x in t['n'].lower() for x in ('privad', 'member', 'grupo', 'escuela')) and len(t['n']) <= 34 and t['cat'] not in ('Juvenil', 'Profesional')]
P.sort(key=lambda t: t['s']); ROWS = []; seen = set(); provs = set()
for t in P:
    if t['club'] in seen or t['prov'] in provs: continue
    seen.add(t['club']); provs.add(t['prov']); pr = t['price']; ROWS.append(row(t, tag=(f'{pr:g} €'.replace('.', ','))))
ROWS = ROWS[:4]
def SCENES(ph, DUR):
    return [
     dict(type='text', t0=0, t1=ph[1][0], y=560, size=128, stag=.12, eyebrow='Lo que todo el mundo dice', words=[['«El'], ['golf'], ['es'], '/', ['carísimo.»', G]], flash=True),
     dict(type='text', t0=ph[1][0], t1=ph[2][0], y=640, size=210, stag=.1, words=[['¿Seguro?', G]], flash=True),
     dict(type='counter', t0=ph[2][0], t1=ph[3][0], y=520, to=314, dur=2.2, eyebrow='Torneos de toda España', label='con precio publicado'),
     dict(type='bars', t0=ph[3][0], t1=ph[4][0], y=300, eyebrow='Precio de inscripción', title='La mitad: <span class="gold it">40 € o menos.</span>', items=[['Hasta 30 €', 129], ['31 – 40 €', 31], ['41 – 100 €', 143], ['Más de 100 €', 11]]),
     dict(type='cards', t0=ph[4][0], t1=ph[6][0], y=300, eyebrow='Torneos reales de estos días', title='<span class="gold it">129</span> por 30 € o menos', rows=ROWS, gap=.16),
     dict(type='text', t0=ph[6][0], t1=ph[7][0], y=560, size=150, stag=.12, eyebrow='¿Y los caros?', words=[['Solo'], ['11'], '/', ['pasan'], ['de'], ['100 €', G]], flash=True),
     dict(type='text', t0=ph[7][0], t1=ph[10][0], y=500, size=120, stag=.1, eyebrow='Ojo', words=[['Es'], ['la'], '/', ['inscripción.', G]], sub='Si no eres socio, a veces el green fee va aparte.'),
     dict(type='phone', t0=ph[10][0], t1=ph[13][0], src='/social/#partida/x1', y=250, scroll=180, scrollAt=2.2),
     dict(type='text', t0=ph[13][0], t1=ph[15][0], y=520, size=120, stag=.1, eyebrow='Te leo en comentarios', words=[['¿Cuánto'], '/', ['pagaste'], ['por'], ['tu'], '/', ['último'], ['torneo?', G]]),
     dict(type='end', t0=ph[15][0], t1=DUR + 1, html='Todos los torneos, <span class="gold it">con su precio.</span>')]
