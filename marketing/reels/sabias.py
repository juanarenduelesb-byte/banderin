OUT = 'banderin-reel-sabias-que.mp4'; TEMPO = 1.1; LEAD = 0.35
KEYS = ['crema', 'meteorito', 'tres', 'setenta', 'paraguas', 'tornado', 'zanahorias', 'paredes?', 'funciona?', 'banderín', 'todos', 'gratis.', 'ninguno.', 'meteorito']
_ph = ["¿Sabías que|ponerte|crema solar", "no te protege|de un meteorito|de tres mil|toneladas", "cayendo a|setenta mil|kilómetros|por hora?", "¿Sabías que|abrir|un paraguas", "no sirve de nada|dentro de|un tornado|de categoría cinco?",
 "¿Y que comer|zanahorias", "no te deja|ver a través|de las paredes?", "Pero,|¿sabes lo que|sí funciona?", "Banderín|punto es.", "Todos los torneos|de golf|de España,|en una sola web.", "Gratis.",
 "Para que|no te pierdas|ninguno.", "Eso sí:|del meteorito|no te salva.", "Mándaselo|a quien se entera|de los torneos|cuando ya|han pasado."]
TOKENS = []
for i, p in enumerate(_ph):
    for w in p.split('|'): TOKENS.append((w, len(w) + 1, i))
MAXW = 3; TAIL = 1.6
def SCENES(ph, DUR):
    return [
     dict(type='photo', t0=0, t1=ph[3][0], img='s0', tag='¿SABÍAS QUE…?', st=[[ph[0][0] + .9, '🧴 FPS 50', 120, 1020, -6], [ph[1][0] + .9, '☄️ 3.000 toneladas', 330, 1160, 4], [ph[2][0] + .5, '70.000 km/h', 200, 1300, -3], [ph[2][1] - .3, 'Protección: 0 %', 420, 860, 6]], hits=[ph[2][1] - .3]),
     dict(type='photo', t0=ph[3][0], t1=ph[5][0], img='s1', tag='¿SABÍAS QUE…?', st=[[ph[3][0] + .6, '☂️ Paraguas', 150, 1060, -5], [ph[4][0] + 1.2, '🌪️ Categoría 5', 380, 1200, 4], [ph[4][1] - .3, 'Utilidad: ninguna', 260, 860, -4]], hits=[ph[4][1] - .3]),
     dict(type='photo', t0=ph[5][0], t1=ph[7][0], img='s2', tag='¿Y QUE…?', st=[[ph[5][0] + .5, '🥕 Zanahoria', 160, 1100, -5], [ph[6][1] - .5, 'Visión rayos X: 0', 300, 880, 5]], hits=[ph[6][1] - .5]),
     dict(type='pivot', t0=ph[7][0], t1=ph[8][0], qAt=ph[7][0] + .45),
     dict(type='reveal', t0=ph[8][0], t1=ph[12][0], flash=True, nAt=ph[9][0], gAt=ph[10][0], okAt=ph[11][0], hits=[ph[10][0]], pops=[ph[11][0] + .1, ph[11][0] + .5]),
     dict(type='photo', t0=ph[12][0], t1=ph[13][0], img='s0', tag='LETRA PEQUEÑA', small=True, st=[[ph[12][0] + .9, 'Anti-meteoritos: no incluido', 160, 1000, -5]], hits=[ph[12][0] + .9]),
     dict(type='cta', t0=ph[13][0], t1=DUR + 1, eAt=ph[13][0] + 1.2, nocap=True)]
