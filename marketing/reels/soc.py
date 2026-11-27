import sys, datetime; sys.path.insert(0, '/home/claude/reels')
from rd import *
OUT = 'banderin-reel-social.mp4'; TEMPO = 1.1; G = 'gold'
KEYS = ['uno', 'pareja', 'banderín', 'social', 'cerca', 'hándicap', 'toque', 'correo', 'chat', 'publica', 'perfil', 'contacto', 'gratis', 'jugar']
_ph = ["¿Os|falta|uno|para la|partida|del|sábado?", "¿O|buscas|pareja|para un|torneo?", "Llega|Banderín|Social.",
 "Partidas|abiertas|cerca|de ti,", "con el|hándicap|que buscan.", "Pides|plaza|con un|toque.", "Cuando|te aceptan,|te avisamos|por|correo.",
 "Y quedáis|en el|chat|de la|partida.", "¿Te falta|gente?", "Publica|tu partida|en un|minuto.", "Tu|perfil:", "hándicap,", "campos|y foto.",
 "Tu|contacto,|solo para|quien|juega|contigo.", "Gratis,|con tu|cuenta|de|Banderín.", "Banderín|Social.", "Encuentra|con quién|jugar."]
TOKENS = []
for i, p in enumerate(_ph):
    for w in p.split('|'): TOKENS.append((w, len(w) + 1, i))
HOY2 = datetime.date.today().isoformat()
par = [t for t in T if t.get('form') == 'Parejas' and t['s'] >= HOY2 and t['cat'] not in ('Juvenil', 'Profesional') and len(t['n']) <= 30]
par.sort(key=lambda t: t['s']); ROWS = []; seen = set()
for t in par:
    if t['club'] in seen: continue
    seen.add(t['club']); ROWS.append(row(t, tag='Busco pareja'))
ROWS = ROWS[:4]
S = '/social/#'
def SCENES(ph, DUR):
    return [
     dict(type='text', t0=0, t1=ph[1][0], y=600, size=150, stag=.12, eyebrow='Sábado · 9:30', words=[['¿Os'], ['falta'], '/', ['uno?', G]], flash=True),
     dict(type='cards', t0=ph[1][0], t1=ph[2][0], y=300, eyebrow='Torneos por parejas', title='¿Y tu <span class="gold it">pareja?</span>', rows=ROWS, gap=.18),
     dict(type='text', t0=ph[2][0], t1=ph[3][0], y=560, size=170, stag=.14, eyebrow='Nuevo en Banderín', words=[['Banderín'], '/', ['Social.', G]], flash=True),
     dict(type='phone', t0=ph[3][0], t1=ph[5][0], src=S + 'partidas', y=250, scroll=760, scrollAt=.6),
     dict(type='phone', t0=ph[5][0], t1=ph[6][0], src=S + 'partida/x1', y=250, tap=.75, sel='[data-join]'),
     dict(type='notifs', t0=ph[6][0], t1=ph[7][0], y=520, items=[['ahora', 'Estás dentro ⛳', 'Lucía M. te ha aceptado en su partida del sábado en Olivar de la Hinojosa.'], ['ahora', 'Nueva solicitud', 'Álvaro G. quiere unirse a tu partida.']]),
     dict(type='phone', t0=ph[7][0], t1=ph[8][0], src=S + 'partida/c1', y=250, scroll=820, scrollAt=.3),
     dict(type='phone', t0=ph[8][0], t1=ph[10][0], src=S + 'publicar', y=250, scroll=260, scrollAt=1.0),
     dict(type='phone', t0=ph[10][0], t1=ph[13][0], src=S + 'perfil', y=250),
     dict(type='text', t0=ph[13][0], t1=ph[14][0], y=520, size=112, stag=.1, eyebrow='Tu contacto', words=[['Solo'], ['lo'], ['ven'], '/', ['tus', G], ['amigos', G], '/', ['y'], ['quien'], ['juega'], '/', ['contigo.', G]]),
     dict(type='text', t0=ph[14][0], t1=ph[15][0], y=600, size=190, stag=.1, words=[['Gratis.', G]], sub='Con tu cuenta de Banderín. Desde los 16 años.', flash=True),
     dict(type='end', t0=ph[15][0], t1=DUR + 1, html='Encuentra <span class="gold it">con quién jugar.</span>')]
