OUT = 'banderin-reel-fichajes.mp4'; TEMPO = 1.1; LEAD = 0.35
KEYS = ['fichajes.', 'dieciocho', 'excusas:', 'noventa', 'tres', 'senior', 'pareja.', 'navidad.', 'cerrada.', 'oficial.', 'banderín.', 'comentarios.']
_ph = ["Última hora|en el mercado|de fichajes.", "Jugador|amateur,", "treinta y ocho|años.", "Hándicap|dieciocho|coma cuatro.", "Excusas:", "noventa y nueve.", "Tres torneos|pujan por él.",
 "La Copa Senior|se retira:", "no cumple|la edad.", "La Liga|de Parejas,", "tampoco:", "no tiene|pareja.", "Y entra|el Torneo|de Navidad.", "Sábado,|a diez kilómetros,|inscripción abierta.",
 "Operación|cerrada.", "Oficial.", "Su agente:", "Banderín.", "¿Y tú,", "a qué torneo|fichas|este finde?", "Te leo|en comentarios."]
TOKENS = []
for i, p in enumerate(_ph):
    for w in p.split('|'): TOKENS.append((w, len(w) + 1, i))
MAXW = 3; TAIL = 1.6
def SCENES(ph, DUR):
    return [
     dict(type='breaking', t0=0, t1=ph[1][0]),
     dict(type='card', t0=ph[1][0], t1=ph[6][0], ageAt=ph[2][0], hcpAt=ph[3][0], excAt=ph[5][0], pops=[ph[2][0], ph[3][0]], hits=[ph[5][0]]),
     dict(type='offers', t0=ph[6][0], t1=ph[14][0], x1=ph[8][0], x2=ph[11][0], inAt=ph[12][0], detAt=ph[13][0], hits=[ph[8][0], ph[11][0]], pops=[ph[12][0] + .1]),
     dict(type='oficial', t0=ph[14][0], t1=ph[16][0], stampAt=ph[14][0] + .15, ofAt=ph[15][0], flash=True, hits=[ph[14][0] + .15, ph[15][0]]),
     dict(type='agent', t0=ph[16][0], t1=ph[18][0], logoAt=ph[17][0], pops=[ph[17][0]]),
     dict(type='cta', t0=ph[18][0], t1=DUR + 1, eAt=ph[20][0], nocap=False)]
