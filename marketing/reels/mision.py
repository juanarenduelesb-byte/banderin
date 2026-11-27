import random, math
OUT = 'banderin-reel-mision.mp4'; TEMPO = 1.1; LEAD = 0.35
KEYS = ['misión:', 'torneo', 'catorce', 'cerrada.', 'fallida.', 'truco.', 'banderín', 'todos', 'superada.', 'etiqueta']
_ph = ["Nueva|misión:", "jugar|un torneo|este sábado.", "Paso uno:", "encontrar uno.", "Web de la|federación.", "Web del club.", "El grupo|de WhatsApp.",
 "Catorce|pestañas|abiertas.", "Por fin|lo encuentras.", "Inscripción|cerrada.", "Misión|fallida.", "Reintentar.", "Esta vez,", "usas|el truco.",
 "Banderín|punto es.", "Todos|los torneos|de España.", "Con su plazo|de inscripción.", "Misión|superada.", "Etiqueta|a tu compañero|de partida."]
TOKENS = []
for i, p in enumerate(_ph):
    for w in p.split('|'): TOKENS.append((w, len(w) + 1, i))
MAXW = 3; TAIL = 1.6
# --- mapa: 1 punto por torneo (datos reales por comunidad, 26/11) ---
POLY = [(-9.3,43.2),(-8,43.7),(-5.8,43.6),(-3.8,43.45),(-1.8,43.4),(-1.4,43.3),(0.7,42.8),(3.2,42.4),(3.2,41.9),(2.1,41.3),(0.9,41.0),(0.2,40.2),(-0.3,39.5),(0.2,38.8),(-0.5,38.3),(-0.7,37.6),(-1.6,37.2),(-2.1,36.7),(-4.4,36.7),(-5.6,36.0),(-6.3,36.6),(-6.9,37.2),(-7.4,37.2),(-7.5,38.0),(-7.0,38.9),(-7.5,39.6),(-6.9,40.2),(-6.8,41.0),(-6.2,41.6),(-6.6,41.9),(-8.1,41.8),(-8.9,41.9),(-8.9,42.5)]
REG = {'Región de Murcia':(120,-1.3,37.9,.45,.3),'Andalucía':(285,-4.8,37.3,1.4,.45),'Comunidad de Madrid':(76,-3.75,40.45,.3,.25),'Illes Balears':(56,2.95,39.6,.3,.15),
 'Galicia':(49,-8.1,42.7,.45,.4),'Castilla-La Mancha':(22,-3.0,39.4,.9,.5),'Cataluña':(224,1.9,41.8,.55,.4),'Comunitat Valenciana':(137,-0.5,39.0,.35,.6),'Principado de Asturias':(39,-5.9,43.35,.4,.12),
 'Castilla y León':(49,-4.6,41.7,1.0,.5),'Cantabria':(6,-4.0,43.2,.25,.1),'Canarias':(12,0,0,0,0),'Aragón':(16,-0.8,41.5,.5,.6),'País Vasco':(9,-2.6,43.1,.25,.1),'Extremadura':(1,-6.2,39.2,.3,.3),'La Rioja':(2,-2.5,42.3,.2,.1)}
def inside(x, y, P=POLY):
    c = False
    for i in range(len(P)):
        (x1, y1), (x2, y2) = P[i], P[i - 1]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1: c = not c
    return c
def proj(lon, lat): return [round(90 + (lon + 9.6) / 13.0 * 900, 1), round(480 + (44.0 - lat) / 8.3 * 760 * 1.0, 1)]
def _dots():
    R = random.Random(7); out = []
    for k, (n, lo, la, sx, sy) in REG.items():
        for i in range(n):
            if k == 'Canarias': out.append([round(150 + R.random() * 220, 1), round(1210 + R.random() * 60, 1), 0]); continue
            for _ in range(200):
                x, y = R.gauss(lo, sx * .6), R.gauss(la, sy * .6)
                if k == 'Illes Balears' or inside(x, y): break
            out.append(proj(x, y) + [0])
    R.shuffle(out)
    for i, d in enumerate(out): d[2] = round(i / len(out), 3)
    return out
def SCENES(ph, DUR):
    return [
     dict(type='mission', t0=0, t1=ph[2][0], subAt=ph[1][0]),
     dict(type='objective', t0=ph[2][0], t1=ph[4][0], objAt=ph[3][0]),
     dict(type='tabs', t0=ph[4][0], t1=ph[8][0], tabs=[[ph[4][0] + .1, 'rfegolf.es · Calendario', 'Calendario 2026 (PDF, 34 págs.)'], [ph[5][0] + .1, 'Web del club', 'Próximamente…'],
          [ph[6][0] + .1, 'Golf Sábados 🏌️ (47)', 'Pepe: ¿alguien sabe si hay algo el sábado?'], [ph[7][0] + .1, '+11 pestañas', '']], cntAt=ph[7][0], hits=[ph[4][0] + .1, ph[5][0] + .1, ph[6][0] + .1, ph[7][0] + .1]),
     dict(type='found', t0=ph[8][0], t1=ph[10][0], stampAt=ph[9][0] + .1, hits=[ph[9][0] + .1]),
     dict(type='fail', t0=ph[10][0], t1=ph[12][0], flash=True, btnAt=ph[11][0]),
     dict(type='cheat', t0=ph[12][0], t1=ph[15][0], typeAt=ph[14][0] - .05, okAt=ph[14][1], pops=[ph[14][0] + .05 + i * .09 for i in range(11)], hits=[ph[14][1]]),
     dict(type='map', t0=ph[15][0], t1=ph[17][0], dots=_dots(), poly=[proj(*q) for q in POLY], popDur=1.8, chipAt=ph[16][0]),
     dict(type='passed', t0=ph[17][0], t1=ph[18][0], flash=True),
     dict(type='cta', t0=ph[18][0], t1=DUR + 1, eAt=ph[18][0] + .9, nocap=True)]
