import sys; sys.path.insert(0, '/home/claude/reels')
OUT = 'banderin-viral-2-adivina-la-provincia.mp4'; TEMPO = 1.15
KEYS = ['provincia', 'madrid', 'cuarta', '86', 'girona', '92', 'murcia', '100', 'alicante', '113', 'comentarios', 'banderín']
_ph = ["¿Qué|provincia|tiene|más|torneos|de golf?", "No es|Madrid.", "Madrid,", "cuarta.", "86=ochenta y seis.", "Tercera,|Girona.", "92=noventa y dos.", "Segunda,|Murcia.", "100=cien.", "Y la|primera,", "Alicante.", "113=ciento trece|torneos.", "¿Y la|tuya?", "Dímelo|en los|comentarios.", "Banderín."]
TOKENS = []
for i, p in enumerate(_ph):
    for w in p.split('|'):
        show, _, spoken = w.partition('='); TOKENS.append((show, len(spoken or show) + 1, i))
def SCENES(ph, DUR):
    c = lambda a, b, to, pos, name, **k: dict(type='counter', t0=ph[a][0], t1=ph[b][0], to=to, dur=ph[a + 2][0] - ph[a][0] + .25 if False else (ph[b - 1][0] - ph[a][0] + .3), eyebrow=f'Puesto {pos}º', label=f'torneos en <span class="gold it">{name}.</span>', y=420, **k)
    return [
     dict(type='text', t0=0, t1=ph[1][0], y=560, size=118, stag=.09, sub='Torneos publicados desde hoy en Banderín', words=[['¿Qué'], ['provincia'], '/', ['tiene'], ['más', 'gold'], '/', ['torneos'], ['de'], ['golf?', 'gold']], flash=True),
     dict(type='text', t0=ph[1][0], t1=ph[2][0], y=700, size=170, align='center', stag=.12, flash=True, words=[['No'], ['es'], '/', ['Madrid.', 'gold']]),
     c(2, 5, 86, 4, 'Madrid', flash=True),
     c(5, 7, 92, 3, 'Girona', flash=True),
     c(7, 9, 100, 2, 'Murcia', flash=True),
     dict(type='counter', t0=ph[9][0], t1=ph[12][0], to=113, dur=ph[11][0] - ph[9][0] + .3, eyebrow='Puesto 1º', label='torneos en <span class="gold it">Alicante.</span>', y=230, map=dict(x=40, y=820, s=1.0, o=.85, wave=.9), flash=True),
     dict(type='text', t0=ph[12][0], t1=ph[14][0], y=620, size=150, align='center', stag=.14, words=[['¿Y'], ['la'], ['tuya?', 'gold'], '/', ['Comenta.', 'gold']], flash=True),
     dict(type='end', t0=ph[14][0], t1=DUR + 1, html='Encuentra tu <span class="gold it">provincia.</span>')]
