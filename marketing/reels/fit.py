OUT = 'banderin-reel-no-es-para-ti.mp4'; TEMPO = 1.1; LEAD = 0.35
KEYS = ['socios.»', 'senior.', 'treinta', 'femenino.»', 'cero', 'banderín', 'perfil', 'encaja', 'antes', 'etiqueta']
_ph = ["Te apuntas|a un torneo.", "Llegas|al club.", "«Lo siento,|es solo|para socios.»", "Te apuntas|a otro.", "«Es senior.", "Usted tiene|treinta y ocho.»",
 "Otro más.", "«Caballero…", "es femenino.»", "Tres sábados.", "Cero golpes.", "Por eso|Banderín|tiene tu|perfil|de jugador.", "Pones tu edad,|tu club|y tu hándicap.",
 "Y cada torneo|te dice|si encaja|contigo.", "Antes de|inscribirte.", "Etiqueta|al que siempre|se apunta|sin leer."]
TOKENS = []
for i, p in enumerate(_ph):
    for w in p.split('|'): TOKENS.append((w, len(w) + 1, i))
MAXW = 3; TAIL = 1.6
def SCENES(ph, DUR):
    return [
     dict(type='deny', t0=0, t1=ph[3][0], name='Torneo Social de Otoño', sub='Sábado · 9:00 · Salida 1', chip='📍 Llegas al club · 8:45', chipAt=ph[1][0], quote='«Lo siento, es solo para socios.»', qAt=ph[2][0], stamp='SOLO SOCIOS', stampAt=ph[2][1] - .35, hits=[ph[2][1] - .3]),
     dict(type='deny', t0=ph[3][0], t1=ph[6][0], name='Copa Senior', sub='Sábado · 9:30 · Stableford', chip='🏌️ Bolas nuevas, guante nuevo', chipAt=ph[3][0] + .5, quote='«Es senior. Usted tiene 38.»', qAt=ph[4][0], stamp='+50 AÑOS', stampAt=ph[5][1] - .3, hits=[ph[5][1] - .25]),
     dict(type='deny', t0=ph[6][0], t1=ph[9][0], name='Liga de Otoño', sub='Sábado · 10:00 · Individual', chip='😎 Esta vez sí', chipAt=ph[6][0] + .3, quote='«Caballero… es femenino.»', qAt=ph[7][0], stamp='FEMENINO', stampAt=ph[8][1] - .3, hits=[ph[8][1] - .25]),
     dict(type='tally', t0=ph[9][0], t1=ph[11][0], days=['7', '14', '21'], zAt=ph[10][0], hits=[ph[10][0] + .05]),
     dict(type='profile', t0=ph[11][0], t1=ph[13][0], flash=True, fields=[['Edad', '38'], ['Club', 'Tu club'], ['Hándicap', '18,4']], fillAt=ph[12][0] + .1, gap=.55,
          pops=[ph[12][0] + .1, ph[12][0] + .65, ph[12][0] + 1.2]),
     dict(type='fit', t0=ph[13][0], t1=ph[15][0], yesAt=ph[14][0], rows=[['Torneo Social de Otoño', 'Sábado · 9:00', False, 'solo socios'], ['Copa Senior', 'Sábado · 9:30', False, 'torneo senior'],
          ['Liga de Otoño', 'Sábado · 10:00', False, 'torneo femenino'], ['Torneo Abierto de Invierno', 'Sábado · 9:00', True, '']],
          pops=[ph[13][0] + .6, ph[13][0] + .95, ph[13][0] + 1.3], hits=[ph[14][0]]),
     dict(type='cta', t0=ph[15][0], t1=DUR + 1, l1='Etiqueta 👇', l2='al que siempre se apunta sin leer', eAt=ph[15][1] - .2, nocap=True)]
