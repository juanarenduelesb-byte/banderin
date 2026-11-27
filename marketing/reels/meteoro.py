OUT = 'banderin-reel-meteorito.mp4'; TEMPO = 1.08; LEAD = 0.35
KEYS = ['crema.', 'cincuenta.', 'meteorito.', 'doce', 'tres', 'setenta', 'mil', 'ciento', 'nada.', 'banderín', 'todos', 'mapa.', 'inscripción.', 'gratis.', 'ya.']
_ph = ["Un sábado|cualquiera.", "Te echas crema.", "Factor cincuenta.", "Pero,|a doce kilómetros|de altura,", "se acerca|un meteorito.", "Doce metros|de roca|y hierro.", "Tres mil|toneladas.",
 "Viaja a|setenta y dos mil|kilómetros|por hora.", "Su superficie|arde a más de|mil seiscientos|grados.", "Y al llegar|al suelo,", "libera la energía|de ciento cuarenta mil|toneladas|de dinamita.", "¿Y la crema?",
 "Factor cincuenta.", "No hace|absolutamente|nada.", "Lo que sí funciona|es banderín|punto es.", "Todos los torneos|de golf|de España,|en una sola web.", "Los de este|fin de semana.", "En un mapa.",
 "Y con la fecha|en que cierra|la inscripción.", "Gratis.", "Métete ya.", "Antes de que caiga|el meteorito."]
TOKENS = []
for i, p in enumerate(_ph):
    for w in p.split('|'): TOKENS.append((w, len(w) + 1, i))
MAXW = 3; TAIL = 1.6
def SCENES(ph, DUR):
    imp = ph[13][1] + .05
    return [
     dict(type='beach', t0=0, t1=ph[3][0], fpsAt=ph[2][0]),
     dict(type='space', t0=ph[3][0], t1=ph[11][0], mAt=ph[4][0], c=[ph[5][0], ph[6][0], ph[7][0], ph[8][0], ph[10][0]], hits=[ph[5][0], ph[6][0], ph[7][0], ph[8][0], ph[10][0]]),
     dict(type='close', t0=ph[11][0], t1=imp, badgeAt=ph[13][0], imp=imp),
     dict(type='boom', t0=imp, t1=ph[14][0], flash=True),
     dict(type='web', t0=ph[14][0], t1=ph[20][0], logoAt=ph[14][0], shots=[[ph[15][0], 'w1'], [ph[16][0], 'w2'], [ph[17][0], 'w3'], [ph[18][0], 'w4'], [ph[18][0] + 1.0, 'w6']], gAt=ph[19][0], hits=[ph[19][0]]),
     dict(type='cta', t0=ph[20][0], t1=DUR + 1, mAt=ph[21][0])]
