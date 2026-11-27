import sys; sys.path.insert(0, '/home/claude/reels')
OUT = 'banderin-viral-3-nombres-de-torneo.mp4'; TEMPO = 1.15
KEYS = ['torneo', 'verdad', 'sunday', 'funday', 'barbacoa', 'límites', 'divino', 'carnaval', 'existen', 'fecha', 'campo', 'enlace', 'banderín']
_ph = ["Esto|es un|torneo|de golf.", "De verdad.", "Sunday|Funday.", "Barbacoa.", "Fuera|de límites.", "Golf|Divino.", "Carnaval.", "Todos|existen.", "Con|fecha,|campo|y enlace.", "En|Banderín."]
TOKENS = []
for i, p in enumerate(_ph):
    for w in p.split('|'):
        show, _, spoken = w.partition('='); TOKENS.append((show, len(spoken or show) + 1, i))
def nm(a, name, eb, sub):
    return dict(type='text', t0=a[0], t1=a[1], y=640, size=150, align='center', stag=.1, flash=True, eyebrow=eb, sub=sub, words=[[x, 'gold'] if i else [x] for i, x in enumerate(name.split(' '))] if False else [[name, 'gold']])
def SCENES(ph, DUR):
    return [
     dict(type='text', t0=0, t1=ph[1][0], y=620, size=128, stag=.1, eyebrow='Torneos de golf', words=[['Esto'], ['es'], ['un'], '/', ['torneo', 'gold'], ['de'], ['golf.', 'gold']], flash=True),
     dict(type='text', t0=ph[1][0], t1=ph[2][0], y=760, size=210, align='center', stag=.1, flash=True, words=[['De', 'gold'], ['verdad.', 'gold']]),
     nm((ph[2][0], ph[3][0]), 'Sunday Funday', 'Dom 22 nov', 'Club de Golf Capdepera · Mallorca'),
     nm((ph[3][0], ph[4][0]), 'Barbacoa', 'Lun 23 nov', 'La Roca Golf · Barcelona'),
     nm((ph[4][0], ph[5][0]), 'Fuera de límites', 'Sáb 21 nov', 'Club de Golf La Peraleja · Murcia'),
     nm((ph[5][0], ph[6][0]), 'Golf Divino', 'Sáb 21 nov', 'Sherry Golf Jerez · Cádiz'),
     nm((ph[6][0], ph[7][0]), 'Carnaval', 'Dom 14 mar', 'Club de Golf Cierro Grande'),
     dict(type='text', t0=ph[7][0], t1=ph[8][0], y=700, size=170, align='center', stag=.12, flash=True, words=[['Todos'], '/', ['existen.', 'gold']]),
     dict(type='phone', t0=ph[8][0], t1=ph[9][0], view='lista', q='Sunday', scroll=0, y=300),
     dict(type='end', t0=ph[9][0], t1=DUR + 1, html='Todos los torneos, <span class="gold it">incluso estos.</span>')]
