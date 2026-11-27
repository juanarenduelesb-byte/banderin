OUT = 'banderin-reel-resumen-golf.mp4'; TEMPO = 1.12; MOOD = 'wrap'; LEAD = 0.4
KEYS = ['2.245', '288', '24', '104', 'sábado', 'andalucía', 'guadalmina.', '64.', 'stableford.', '7', '10.', '320', 'tú?', 'banderín.', 'banderín']
_ph = ["Este|es el|resumen|del golf|en España.", "Dos meses|de datos|de Banderín.", "2.245|torneos.", "En|288|clubes.", "El día|más loco:", "el 24|de octubre.",
 "104|torneos.", "El mismo|día.", "El sábado|manda:", "casi|cuatro veces|más torneos|que el|lunes.", "Andalucía|se lleva|más de uno|de cada tres.",
 "El club|que más|torneos|organiza:", "Guadalmina.", "64.", "El formato|favorito:", "Stableford.", "7|de cada|10.", "¿El torneo|más caro?", "320|euros.",
 "¿Y tú?", "¿Cuántos|has jugado?", "Banderín.", "Todos los|torneos|de España."]
W = {'2.245': 30, '288': 20, '24': 12, '104': 16, '64.': 16, '320': 18, '7': 6, '10.': 6}
TOKENS = []
for i, p in enumerate(_ph):
    for w in p.split('|'): TOKENS.append((w, W.get(w, len(w) + 1), i))
MAXW = 3; TAIL = 2.2
def SCENES(ph, DUR):
    return [
     dict(type='cover', t0=0, t1=ph[2][0], bg='#123323', fg='#F4F1E8', kick='Otoño 2026', lines=['Tu resumen', 'del golf', 'en España.'], size=168,
          sub='9 oct – 30 nov · datos de Banderín', subAt=ph[1][0],
          shapes=[['ring', '#FFD98A', 700, 1150, 360], ['star', '#FF6A5C', 120, 1300, 220], ['circle', '#7B5CD6', 760, 180, 160]]),
     dict(type='num', t0=ph[2][0], t1=ph[4][0], bg='#FF6A5C', kick='Torneos en Banderín', n=2245, label='torneos', n2=288, label2='clubes', n2At=ph[3][0], y=420,
          shapes=[['circle', '#FFD98A', 720, 1250, 420], ['wave', '#123323', 80, 1420, 200]]),
     dict(type='date', t0=ph[4][0], t1=ph[8][0], bg='#FFD98A', fg='#123323', from_='left', kick='El día más loco', mon='OCTUBRE', day='24', calAt=ph[5][0],
          n=104, nAt=ph[6][0], label='torneos', tag='el mismo día', tagAt=ph[7][0], shapes=[['star', '#FF6A5C', 860, 170, 150]]),
     dict(type='versus', t0=ph[8][0], t1=ph[10][0], bg='#6E4FD0', kick='Torneos según el día', title='El sábado<br>manda.', items=[['Sábado', 637, '#FFD98A'], ['Lunes', 170, 'rgba(255,255,255,.5)']],
          max=637, h=560, growAt=ph[9][0], badge='×3,7', badgeAt=ph[9][0] + 1.1, shapes=[['ring', '#FF6A5C', 820, 120, 200]]),
     dict(type='share', t0=ph[10][0], t1=ph[11][0], bg='#2F62F0', kick='Torneos por comunidad', title='Andalucía', pct=.369, big='más de 1 de cada 3', bigAt=ph[10][0] + 1.0,
          foot='Datos de Banderín. Andalucía es también donde más fuentes cubre.', shapes=[['star', '#FFD98A', 860, 200, 170], ['pill', '#FF6A5C', 760, 640, 140]]),
     dict(type='club', t0=ph[11][0], t1=ph[14][0], bg='#F4F1E8', fg='#123323', from_='zoom', kick='El club que más torneos organiza', name='Real Club de Golf Guadalmina', size=124,
          nameAt=ph[12][0], c=64, cAt=ph[13][0], cy=1060, rest=[['Escuela Pública La Cartuja', '49'], ['San Roque Club y Santa Elena', '42']],
          shapes=[['circle', '#FFD98A', 760, 330, 260]]),
     dict(type='dots', t0=ph[14][0], t1=ph[17][0], bg='#1F5139', kick='El formato favorito', word='Stableford', size=190, wordAt=ph[15][0], on=7, fillAt=ph[16][0],
          big='7 de cada 10', foot='Entre los torneos que indican su formato.', shapes=[['ring', '#FFD98A', 840, 640, 180]]),
     dict(type='price', t0=ph[17][0], t1=ph[19][0], bg='#E8473B', from_='left', kick='El más caro', title='¿Cuánto<br>cuesta?', what='Gran Final PGA de España<br>Santa Elena Golf', p=320, pAt=ph[18][0],
          shapes=[['star', '#FFD98A', 100, 1450, 200], ['circle', '#123323', 820, 1500, 150]]),
     dict(type='ask', t0=ph[19][0], t1=ph[21][0], bg='#FFD98A', fg='#123323', from_='zoom', l1='¿Y tú?', l2='¿Cuántos<br>has jugado?', l3='Cuéntamelo en comentarios 👇', a1=ph[19][0], a2=ph[20][0], nocap=True,
          shapes=[['ring', '#FF6A5C', 80, 260, 220], ['star', '#6E4FD0', 820, 1350, 200]]),
     dict(type='end', t0=ph[21][0], t1=DUR + 1, bg='#123323', from_='zoom', bar=False, html='Todos los torneos<br>de España.')]
