OUT = 'banderin-reel-cerca-de-mi.mp4'
NOVO = True
BPM = 124
B = 60 / BPM
def bt(n): return round(n * B, 3)
DUR = bt(42)
G = 'gold'
ROWS = [
    dict(m='SÁB', dd='14', n='Torneo Mid-Amateur Femenino', sub='Barberán y Collar · Madrid', tag='< 5 km', cls='ok'),
    dict(m='DOM', dd='15', n='Copa RFGM Costa del Sol', sub='Olivar de la Hinojosa · Madrid', tag='< 5 km', cls='ok'),
    dict(m='SÁB', dd='14', n='Absoluto de Pitch & Putt', sub='Montepríncipe · Boadilla del Monte', tag='15 km', cls='ok'),
    dict(m='SÁB', dd='14', n='Interclubes de Madrid', sub='Club de Golf La Dehesa · Villanueva', tag='26 km', cls='ok'),
    dict(m='SÁB', dd='14', n='Torneo Alevín «Illescas»', sub='Señorío de Illescas · Toledo', tag='35 km', cls='ok'),
    dict(m='DOM', dd='15', n='Parejas Greensome Chapman', sub='Club de Golf Aranjuez', tag='44 km', cls='ok'),
]
WE = '2026-11-1[45]'
def SCENES(ph, DUR):
    return [
        dict(type='counter', t0=0, t1=bt(4), to=127, dur=1.1, eyebrow='Sábado 14 · Domingo 15', label='torneos de golf <span class="gold">este finde.</span>', y=230,
             map=dict(x=40, y=780, s=.95, o=.85, filter=WE, wave=.9), flash=True),
        dict(type='text', t0=bt(4), t1=bt(7), y=620, size=128, stag=.065,
             words=[['Y'], ['seguro'], ['que'], '/', ['no', G], ['conoces', G], '/', ['ni'], ['la'], ['mitad.']],
             map=dict(x=40, y=1000, s=.9, o=.35, filter=WE, wave=0)),
        dict(type='text', t0=bt(7), t1=bt(10), y=230, size=104, eyebrow='En toda España', stag=.08,
             words=[['Del'], ['Cantábrico'], '/', ['a'], ['Canarias.', G]],
             map=dict(x=40, y=640, s=1.08, o=1, filter=WE, wave=.5)),
        dict(type='bars', t0=bt(10), t1=bt(15), y=300, eyebrow='Este finde, por comunidades', title='¿Dónde se <span class="gold">juega?</span>',
             items=[['Andalucía', 44], ['Madrid', 13], ['Castilla y León', 13], ['Cataluña', 12], ['C. Valenciana', 10]]),
        dict(type='text', t0=bt(15), t1=bt(18), y=700, size=150, align='center', stag=.12, flash=True,
             words=[['¿Y'], ['cerca'], '/', ['de'], ['ti?', G]],
             map=dict(x=40, y=520, s=1.0, o=.3, filter=WE, wave=.4)),
        dict(type='phone', t0=bt(18), t1=bt(26), view='lista', tap=1.0, sel='.locchip', scrollAt=2.4, scroll=640, y=300),
        dict(type='cards', t0=bt(26), t1=bt(32), y=380, eyebrow='Ejemplo: desde Madrid', title='Ordenados por <span class="gold">distancia.</span>', rows=ROWS, gap=.16),
        dict(type='text', t0=bt(32), t1=bt(36), y=560, size=120, stag=.14,
             words=[['Fecha.'], '/', ['Campo.'], '/', ['Enlace', G], ['para', G], '/', ['inscribirte.', G]],
             map=dict(x=40, y=1050, s=.85, o=.3, filter=WE, wave=0)),
        dict(type='text', t0=bt(36), t1=bt(38), y=720, size=150, align='center', stag=.1, flash=True,
             words=[['Gratis.', G]], sub='Sin registrarte. Sin letra pequeña.',
             map=dict(x=40, y=600, s=1.0, o=.3, filter=WE, wave=0)),
        dict(type='end', t0=bt(38), t1=DUR + 1, html='Encuentra tu <span class="gold">próximo torneo.</span>'),
    ]
