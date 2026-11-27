OUT = 'banderin-reel-el-tiempo.mp4'; TEMPO = 1.1; LEAD = 0.35
KEYS = ['previsión', 'ciento', 'cincuenta', 'birdies:', 'cuarenta', 'veinticinco.', 'dieciséis,', 'catorce', 'lluvia,', 'naranja', 'cuela.', 'banderín']
_ph = ["Buenas noches.", "Vamos con|la previsión|del fin de semana.", "Se esperan|ciento cincuenta|y ocho torneos", "en toda España.", "Andalucía,|bajo un anticiclón|de birdies:", "cuarenta y seis|torneos.",
 "Cataluña,", "veinticinco.", "Madrid,|dieciséis,|con atascos|en el tee del uno.", "Galicia,", "catorce torneos.", "Y lluvia,|claro.", "Atención:", "alerta naranja|por excusas.",
 "«Es que|no sabía|que había torneo.»", "Ya no cuela.", "Previsión completa|en banderín|punto es.", "Compártelo|con el que|nunca se entera|de nada."]
TOKENS = []
for i, p in enumerate(_ph):
    for w in p.split('|'): TOKENS.append((w, len(w) + 1, i))
MAXW = 3; TAIL = 1.6
from mision import POLY, proj
TICKER = ["Andalucía Costa del Sol Open de España 2… · Mijas", "FINAL RKN Alumnos 2026 - Turno de Mañana… · Madrid", "Torneo Mensual Costa del Sol Golf Club · Málaga", "Ryder / Solheim P&P · Elche/Elx", "III Prueba Desafío Ribeira Sacra 2026 - … · Rio Cabe", "18 Hoyos Niños Torneo Ega Noviembre · Club de Golf Altorreal", "V Circuito Executive 5ª Categoria Final · Club de Golf Barcelona", "Memorial Day Tournament · Desert Springs Golf Club", "Gastronòmic de Restaurants by Gastronòmi… · Gaudí Golf Club", "Final del Circuit GalaxyGolf 2026 HILLS · Infinitum Golf", "Torneo Navidad Alhama Signature · Alhama Signature", "Torneig Brot d'Or · Club de Golf Castellterçol", "4 J. Circuito Vng 2026. Categoria Oro (0… · Puerto Real", "LIGA INFANTIL 9 hoyos 1ª jornada · Club de Golf Entrepinos"]
REGS = {'and': (-4.8, 37.4), 'cat': (1.6, 41.8), 'mad': (-3.7, 40.4), 'gal': (-8.0, 42.8)}
def SCENES(ph, DUR):
    P = [proj(*q) for q in POLY]; R = {k: proj(*v) for k, v in REGS.items()}
    return [
     dict(type='title', t0=0, t1=ph[2][0], poly=P, ticker=TICKER),
     dict(type='total', t0=ph[2][0], t1=ph[4][0], nAt=ph[2][0] + .3, n=158),
     dict(type='reg', t0=ph[4][0], t1=ph[6][0], at=R['and'], icon='☀️', n=46, nAt=ph[5][0], label='Anticiclón de birdies', hits=[ph[5][0]]),
     dict(type='reg', t0=ph[6][0], t1=ph[8][0], at=R['cat'], icon='🌤️', n=25, nAt=ph[7][0], label='Despejado', hits=[ph[7][0]]),
     dict(type='reg', t0=ph[8][0], t1=ph[9][0], at=R['mad'], icon='🚗', n=16, nAt=ph[8][0] + .5, label='Atascos en el tee del 1', hits=[ph[8][0] + .5]),
     dict(type='reg', t0=ph[9][0], t1=ph[12][0], at=R['gal'], icon='🌧️', n=14, nAt=ph[10][0], label='Lluvia (claro)', rainAt=ph[11][0], hits=[ph[10][0]]),
     dict(type='alert', t0=ph[12][0], t1=ph[16][0], flash=True, qAt=ph[14][0], stampAt=ph[15][0], hits=[ph[15][0] + .05]),
     dict(type='cta', t0=ph[16][0], t1=DUR + 1, eAt=ph[16][0] + .5, nocap=True)]
