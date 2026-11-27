OUT = 'banderin-reel-expediente-torneo-perdido.mp4'; TEMPO = 1.1; MOOD = 'doc'; LEAD = 0.45
KEYS = ['paco', 'nada', 'pdf', 'otro', 'catorce', 'cerrada', 'ayer', '111', 'ninguno', 'banderín', 'avisa', 'escapado', 'comentarios', '23:47']
_ph = ["Madrid.", "Domingo,", "23:47.", "Un|golfista|pregunta|en el|grupo:", "«¿Alguien|sabe|si hay|torneo|el sábado?»",
 "Paco|responde|con un|audio|de cuatro|minutos.", "No dice|nada.", "Abre|la web|de la|federación.", "Luego,|un PDF.", "Luego,", "otro.",
 "Catorce|pestañas|después…", "lo|encuentra.", "Inscripción|cerrada.", "Ayer.",
 "Solo en|octubre,|en Madrid,|hubo|111|torneos.", "Él|no jugó|ninguno.", "Esto|no tenía|por qué|pasar.",
 "Banderín|junta|todos los|torneos|de España|en un|solo sitio.", "Y te|avisa|antes de|que|cierren.", "¿Cuántos|se te han|escapado|a ti?", "Te leo|en|comentarios."]
W = {'23:47.': 22, '111': 18}
TOKENS = []
for i, p in enumerate(_ph):
    for w in p.split('|'): TOKENS.append((w, W.get(w, len(w) + 1), i))
MAXW = 3; TAIL = 2.4
def SCENES(ph, DUR):
    global REVEAL
    REVEAL = ph[18][0]
    return [
     dict(type='open', t0=0, t1=ph[3][0], kicker='Basado en hechos que te han pasado', city='Madrid', time='DOMINGO · 23:47', tAt=ph[1][0]),
     dict(type='chat', t0=ph[3][0], t1=ph[7][0], chap='CAP. 1 · LA PREGUNTA', y=230, group='Golf los domingos', members='Tú, Paco, Luis, Marta y 10 más',
          q='¿Alguien sabe si hay torneo el sábado? 🙏', q1=ph[4][0] - .1, q2=ph[5][0], who='Paco', len='4:12', nd=ph[6][0] + .25, stamp='SIN RESPUESTA'),
     dict(type='tabs', t0=ph[7][0], t1=ph[13][0], chap='CAP. 2 · LA BÚSQUEDA', y=330, n=14, nAt=ph[11][1] - .2, foundAt=ph[12][0],
          pdfAt=[ph[8][0] + .3, ph[10][0], ph[10][0] + .3],
          pdfs=['calendario_2026.pdf', 'circular_14_def.pdf', 'calendario_DEF_v3_FINAL.pdf'],
          tabn=['Federación · Calendario', 'calendario_2026.pdf', 'circular_14_def.pdf', 'Club · Competiciones', 'calendario_DEF_v3.pdf', 'torneo golf sábado madrid', 'Club · Noticias'],
          found='Sábado · Torneo de Otoño<br><span style="font-weight:500;font-size:34px">Inscripción hasta el sábado anterior</span>'),
     dict(type='closed', t0=ph[13][0], t1=ph[15][0], chap='CAP. 3 · EL DESENLACE', y=470, date='SÁBADO · 9:00', name='Torneo de Otoño', sub='Club de golf · Madrid',
          when='AYER', stampAt=ph[13][0] + .25, ayerAt=ph[14][0], shake=ph[13][0] + .45),
     dict(type='stat', t0=ph[15][0], t1=ph[17][0], chap='CAP. 4 · LAS CIFRAS', y=360, kicker='Octubre · Comunidad de Madrid', n=111, label='torneos de golf.', label2='Él jugó:', n2='0', n2At=ph[16][0]),
     dict(type='line', t0=ph[17][0], t1=ph[18][0], y=690, size=132, words=[['Esto'], ['no'], ['tenía'], '/', ['por'], ['qué'], '/', ['pasar.', 'red']], stag=.13),
     dict(type='phone', t0=ph[18][0], t1=ph[20][0], flash=True, y=290, scroll=520, scrollAt=1.0, noteAt=ph[19][0], noteY=170,
          note=['correo · ahora', 'Cierra la inscripción mañana', 'Torneo de Otoño · Madrid. Aún estás a tiempo.']),
     dict(type='line', t0=ph[20][0], t1=ph[21][0], y=600, size=136, words=[['¿Cuántos'], ['se'], ['te'], '/', ['han'], ['escapado'], '/', ['a'], ['ti?', 'gold']], stag=.1),
     dict(type='end', t0=ph[21][0], t1=DUR + 1, html='Te leo en <span class="gold">comentarios.</span>')]
