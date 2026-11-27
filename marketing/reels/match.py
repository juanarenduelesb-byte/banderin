OUT = 'banderin-reel-match.mp4'; TEMPO = 1.1; LEAD = 0.35
KEYS = ['tres', 'banderín.', 'patrocinador.»', 'mayor', 'invierno.', 'veintiséis.', 'green.', 'match.', 'avisa', 'etiqueta', 'urgente.']
_ph = ["Llevas|tres semanas|sin jugar|un torneo.", "Así que haces|lo que haría|cualquiera.", "Abres|Banderín.", "Pro-Am|de Marbella.", "«Busco|a alguien|con patrocinador.»",
 "Siguiente.", "Campeonato|sub dieciocho.", "«Eres un poco|mayor|para mí.»", "Siguiente.", "Torneo Abierto|de Invierno.", "Sábado,|nueve de|la mañana.",
 "Hándicap|hasta|veintiséis.", "Buen green.", "Es un match.", "Y si sale otro|en tu zona,|te avisa|al correo.", "Etiqueta|a quien|necesita|un torneo|urgente."]
TOKENS = []
for i, p in enumerate(_ph):
    for w in p.split('|'): TOKENS.append((w, len(w) + 1, i))
MAXW = 3; TAIL = 1.6
def SCENES(ph, DUR):
    return [
     dict(type='intro', t0=0, t1=ph[2][0], shakeAt=ph[1][0]),
     dict(type='open', t0=ph[2][0], t1=ph[3][0], flash=True),
     dict(type='card', t0=ph[3][0], t1=ph[6][0], img='m1', name='Pro-Am de Marbella', meta='Marbella · 4 jugadores · Scramble', bio='«Busco a alguien con patrocinador.»', bioAt=ph[4][0], outAt=ph[5][0], dir=-1, hits=[ph[5][0] + .05]),
     dict(type='card', t0=ph[6][0], t1=ph[9][0], img='m2', name='Campeonato Sub-18', meta='Juvenil · Medal Play', bio='«Eres un poco mayor para mí.»', bioAt=ph[7][0], outAt=ph[8][0], dir=-1, hits=[ph[8][0] + .05]),
     dict(type='card', t0=ph[9][0], t1=ph[13][0], img='m0', name='Abierto de Invierno', meta='A 18 km · Individual Stableford', bio='', chips=[[ph[10][0], '📅 Sáb · 9:00'], [ph[11][0], '🏌️ Hcp hasta 26'], [ph[12][0], '⛳ Buen green']],
          outAt=ph[13][0] - .25, dir=1, pops=[ph[10][0], ph[11][0], ph[12][0]]),
     dict(type='match', t0=ph[13][0], t1=ph[14][0], flash=True),
     dict(type='notif', t0=ph[14][0], t1=ph[15][0], nAt=ph[14][0] + .5, pops=[ph[14][0] + .5]),
     dict(type='cta', t0=ph[15][0], t1=DUR + 1, eAt=ph[15][0] + 1.2, nocap=True)]
