OUT = 'banderin-reel-este-finde.mp4'
TEMPO = 1.1
KEYS = ['125', 'torneos', '44', 'andalucía', '13', 'madrid', 'alguno', 'todos', 'clic', 'inscribirte', 'banderín']
_ph = [
    "Este|fin|de|semana|se juegan|125=ciento veinticinco|torneos|de golf|en España.",
    "44=Cuarenta y cuatro,|en|Andalucía.",
    "13=Trece,",
    "en|Madrid.",
    "¿Y tú|sabías|de|alguno?",
    "En|Banderín|los tienes|todos.",
    "Filtra|por tu|ciudad,|y en un|clic|tienes|fecha,|campo,",
    "y el enlace|para|inscribirte.",
    "Banderín.",
    "Encuentra|tu próximo|torneo.",
]
TOKENS = []
for i, p in enumerate(_ph):
    for w in p.split('|'):
        show, _, spoken = w.partition('=')
        TOKENS.append((show, len(spoken or show) + 1, i))

ROWS = [
    dict(m='SÁB', dd='14', n='Circuito Heineken · Fourball', sub='Club Hato Verde · Sevilla', tag='Abierta', cls='ok'),
    dict(m='SÁB', dd='14', n='Tiger & Rabbit', sub='Club de Golf Son Servera · Mallorca', tag='Abierta', cls='ok'),
    dict(m='SÁB', dd='14', n='III Torneo Lotus', sub='Real Aero Club de Vigo', tag='Abierta', cls='ok'),
    dict(m='DOM', dd='15', n='Greensome Chapman', sub='Club de Golf Aranjuez · Madrid', tag='Abierta', cls='ok'),
    dict(m='DOM', dd='15', n='Gran Torneo Playa Serena', sub='Club de Golf Playa Serena · Almería', tag='Abierta', cls='ok'),
]

def SCENES(ph, DUR):
    a0, a1 = ph[0]; mid = round(a0 + (a1 - a0) * 0.62, 2)
    return [
        dict(type='counter', t0=0, t1=mid, to=125, dur=1.3, eyebrow='Sábado 14 · Domingo 15', label='torneos de golf <span class="gold it">este finde.</span>', y=230,
             map=dict(x=40, y=760, s=.95, o=.85, filter='2026-11-1[45]', wave=1.0), flash=True),
        dict(type='text', t0=mid, t1=ph[1][0], y=250, eyebrow='En toda España', html='Del Cantábrico <br>a <span class="gold it">Canarias.</span>', size=104,
             map=dict(x=40, y=640, s=1.08, o=1, filter='2026-11-1[45]', wave=.6)),
        dict(type='bars', t0=ph[1][0], t1=ph[4][0], y=300, eyebrow='Este finde, por comunidades', title='¿Dónde se <span class="gold it">juega?</span>',
             items=[['Andalucía', 44], ['Madrid', 13], ['Castilla y León', 13], ['C. Valenciana', 10], ['Cataluña', 10]]),
        dict(type='text', t0=ph[4][0], t1=ph[5][0], y=640, html='¿Y tú sabías<br>de <span class="gold it">alguno?</span>', size=150, flash=True),
        dict(type='cards', t0=ph[5][0], t1=ph[6][0], y=250, eyebrow='Banderín', title='Todos, en <span class="gold it">una lista.</span>', rows=ROWS, gap=.2),
        dict(type='phone', t0=ph[6][0], t1=ph[8][0], view='lista', q='Madrid', scroll=520, y=300),
        dict(type='end', t0=ph[8][0], t1=DUR + 1),
    ]
