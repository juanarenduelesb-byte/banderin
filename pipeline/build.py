"""Construye data.js de Banderín a partir de las fuentes volcadas."""
import json, re, html, unicodedata, difflib, datetime as dt, urllib.request, urllib.parse, os, time
from zoneinfo import ZoneInfo

MAD = ZoneInfo('Europe/Madrid')
TODAY = dt.date.today().isoformat()
PAST = (dt.date.today() - dt.timedelta(days=45)).isoformat()
HORIZON = (dt.date.today() + dt.timedelta(days=420)).isoformat()
SCR = '/home/claude/scr/'

PROV_CCAA = {
 'Almería':'Andalucía','Cádiz':'Andalucía','Córdoba':'Andalucía','Granada':'Andalucía','Huelva':'Andalucía','Jaén':'Andalucía','Málaga':'Andalucía','Sevilla':'Andalucía',
 'Huesca':'Aragón','Teruel':'Aragón','Zaragoza':'Aragón','Asturias':'Principado de Asturias','Illes Balears':'Illes Balears',
 'Las Palmas':'Canarias','Santa Cruz de Tenerife':'Canarias','Cantabria':'Cantabria',
 'Ávila':'Castilla y León','Burgos':'Castilla y León','León':'Castilla y León','Palencia':'Castilla y León','Salamanca':'Castilla y León','Segovia':'Castilla y León','Soria':'Castilla y León','Valladolid':'Castilla y León','Zamora':'Castilla y León',
 'Albacete':'Castilla-La Mancha','Ciudad Real':'Castilla-La Mancha','Cuenca':'Castilla-La Mancha','Guadalajara':'Castilla-La Mancha','Toledo':'Castilla-La Mancha',
 'Barcelona':'Cataluña','Girona':'Cataluña','Lleida':'Cataluña','Tarragona':'Cataluña',
 'Alicante':'Comunitat Valenciana','Castellón':'Comunitat Valenciana','Valencia':'Comunitat Valenciana',
 'Badajoz':'Extremadura','Cáceres':'Extremadura','A Coruña':'Galicia','Lugo':'Galicia','Ourense':'Galicia','Pontevedra':'Galicia',
 'Madrid':'Comunidad de Madrid','Murcia':'Región de Murcia','Navarra':'Navarra','Álava':'País Vasco','Gipuzkoa':'País Vasco','Bizkaia':'País Vasco',
 'La Rioja':'La Rioja','Ceuta':'Ceuta','Melilla':'Melilla'}
PROV_ALIAS = {'baleares':'Illes Balears','islas baleares':'Illes Balears','illes balears':'Illes Balears','mallorca':'Illes Balears','alacant':'Alicante','alicante/alacant':'Alicante',
 'castello':'Castellón','castellon':'Castellón','castello/castellon':'Castellón','valencia/valencia':'Valencia','la coruna':'A Coruña','coruna':'A Coruña','a coruna':'A Coruña','coruña, a':'A Coruña',
 'orense':'Ourense','gerona':'Girona','lerida':'Lleida','guipuzcoa':'Gipuzkoa','vizcaya':'Bizkaia','alava':'Álava','araba':'Álava','rioja, la':'La Rioja','rioja':'La Rioja',
 'palmas, las':'Las Palmas','las palmas':'Las Palmas','tenerife':'Santa Cruz de Tenerife','s.c. tenerife':'Santa Cruz de Tenerife','santa cruz de tenerife':'Santa Cruz de Tenerife','principado de asturias':'Asturias','navarra':'Navarra','nafarroa':'Navarra'}
CODE_CCAA = {'AM':'Andalucía','77':'Castilla y León','CB':'Cataluña','LV':'Comunitat Valenciana','CM':'Comunidad de Madrid','GC':'Galicia','CP':'Canarias','MM':'Región de Murcia',
 '88':'Castilla-La Mancha','BP':'Illes Balears','02':'Principado de Asturias','VB':'País Vasco','01':'Aragón','11':'Cantabria','99':'Extremadura','44':'Navarra','RL':'La Rioja','ML':'Melilla'}

def strip(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s or '') if unicodedata.category(c) != 'Mn').lower()
def canon_prov(p):
    if not p: return None
    k = strip(p).strip()
    for name in PROV_CCAA:
        if strip(name) == k: return name
    return PROV_ALIAS.get(k)
def fix_town(t):
    t = (t or '').strip()
    t = re.sub(r',\s*de$', '', t)
    m = re.match(r'^(.*),\s*(el|la|los|las|o|a|os|as|l\'|les|els|l|es|sa)$', t, re.I)
    if m: t = m.group(2).capitalize() + ('' if m.group(2).endswith("'") else ' ') + m.group(1)
    return t[:1].upper() + t[1:] if t else t

ACR = {'CV','FGCV','RFGA','RFGM','FGM','FVG','FCGOLF','FAG','FBG','FGPA','RFEG','AESGOLF','P&P','PP','CSC','LV','PGA','SACE','WAGR','FGCLM','CLM','CG','RCG','RC','GC','CD','CDE','UGR','II','III','IV','VI','VII','VIII','IX','XI','XII','XIII','XIV','XV','XVI','XVII','XVIII','XIX','XX','XXI','XXII','XXV','XXX','HCP','MAPFRE','BMW','LGBT','ONCE','UVA','PRO-AM','PROAM','BBVA','DKV','AXA','CEU','UPM','ICADE','ESIC','UCM','USA','UK','EPC','LJG','GGS','PSG','NH','AC'}
SMALL = {'de','del','la','las','el','los','y','e','en','a','al','por','para','con','sin','i','d\'','les','els','o','da','do','dos','das'}
def nice(name):
    name = html.unescape(re.sub(r'\s+', ' ', name or '')).strip()
    name = re.sub(r'\s+[·—](?=\s|$)|[—]', ' -', name)  # el separador · o — de los clubes se muestra como guion (la l·l catalana se respeta)
    name = re.sub(r'(?:\s+-)+\s*$', '', re.sub(r'\s+', ' ', name)).strip()
    name = re.sub(r'^(?:[A-Za-z]\.? ){3,}', '', name)
    name = re.sub(r'^inscripciones?\s+(?:para\s+[^/]+/\s*)?', '', name, flags=re.I).strip() or name
    letters = [c for c in name if c.isalpha()]
    if not letters or sum(c.isupper() for c in letters) / len(letters) < 0.7: return name
    out = []
    for i, w in enumerate(name.split(' ')):
        core = re.sub(r'[^\wÀ-ÿ&\-]', '', w)
        if core.upper() in ACR or re.fullmatch(r'[IVXLC]+', core) and len(core) > 1: out.append(w); continue
        lw = w.lower()
        if i and lw in SMALL: out.append(lw); continue
        out.append(re.sub(r"(^|[\-/(\"'«“])([a-zà-ÿ])", lambda m: m.group(1) + m.group(2).upper(), lw))
    return ' '.join(out)

# ---------- Categorías y modalidades por nombre ----------
def infer(name, org_hint=None):
    n = strip(name)
    if re.search(r'adaptad|inclusiv', n): cat = 'Adaptado'
    elif re.search(r'profesional|pro-am|proam|catprotour|\bpga\b|open de espana|islantilla open|challenge tour', n): cat = 'Profesional'
    elif re.search(r'senior|seniors|super ?senior|aesgolf|veteran', n): cat = 'Senior'
    elif re.search(r'mid[- ]?amateur', n): cat = 'Mid-Amateur'
    elif re.search(r'juvenil|infantil|alevin|benjamin|cadete|sub[- ]?\d\d|junior|pequecircuito|escuela|interescolar|nin[oa]s|kids|boys|girls|padres e hijos|colegios', n): cat = 'Juvenil'
    elif re.search(r'universit', n): cat = 'Universitario'
    elif re.search(r'benefic|solidari|cancer|fundacion|asociacion espanola contra|sindrome|autismo|cruz roja|manos unidas', n): cat = 'Benéfico'
    elif re.search(r'interclub|clubes sin campo|\bcsc\b|equipos|liga de clubes|match ', n): cat = 'Clubes y equipos'
    elif re.search(r'campeonato|cto\.? |copa |ranking|puntuable|circuito .*(federac|cv|fvg|rfg|fgm)|final circuito|trofeo .*(federac)|grand prix|zonal', n) and org_hint == 'Federación': cat = 'Absoluto'
    elif re.search(r'circuito|tour|series|liga [a-z]+ golf', n) and org_hint != 'Federación': cat = 'Circuito comercial'
    elif org_hint == 'Federación': cat = 'Absoluto'
    else: cat = 'Social de club'
    sex = 'Femenino' if re.search(r'femenin|damas|senoras|ladies|mujer|solheim|chicas|girls', n) and not re.search(r'masculin|caballeros|ryder', n) else ('Masculino' if re.search(r'masculin|caballeros|\bmen\b', n) and not re.search(r'femenin|damas', n) else 'Mixto')
    form = 'Parejas' if re.search(r'parejas|dobles|fourball|four-ball|foursome|greensome|scramble|chapman|pairs|duo', n) else ('Equipos' if re.search(r'interclub|equipos|team|match |ryder|liga de clubes|clubes sin campo|cuadrangular', n) else 'Individual')
    campo = 'Pitch & Putt' if re.search(r'pitch|p&p|\bp ?& ?p\b|pitch and putt|par 3|pares 3', n) else 'Campo largo'
    return cat, sex, form, campo

def mod_from(text):
    t = strip(text or '')
    if 'match' in t: return 'Match Play'
    if 'scramble' in t: return 'Scramble'
    if 'greensome' in t or 'chapman' in t: return 'Greensome'
    if 'fourball' in t or 'four ball' in t or 'four-ball' in t or 'mejor bola' in t: return 'Fourball'
    if 'foursome' in t: return 'Foursome'
    if 'stableford' in t: return 'Stableford'
    if 'medal' in t or 'stroke' in t or 'medalplay' in t or 'strokeplay' in t: return 'Medal Play'
    return 'Sin indicar'

# ---------- Directorio RFEG y geocodificación ----------
RF = json.load(open(SCR + 'rfeg_clubs.json'))
rf_list = []
for slug, v in RF.items():
    t = [x for x in v['t'] if not re.match(r'^\d+ hoyos$|^patrocinador|^destacad|^ver club', x, re.I)]
    prov = canon_prov(t[-1]) if t else None
    town = fix_town(t[-2]) if len(t) >= 2 else None
    if town and canon_prov(town) == prov and len(t) == 2 and not re.search(r'golf|club', t[0], re.I): pass
    if town and re.search(r'golf|club|campo', town, re.I): town = None
    rf_list.append({'slug': slug, 'key': strip(slug.replace('-', ' ')), 'town': town, 'prov': prov})
STOP = {'club','de','golf','campo','el','la','los','las','real','c','g','cd','d','s','a','sa','sl','country','resort','and','y','hotel','spa','municipal','deportivo','c.d.','campo','cg','rcg','rc','del','golfe','i','course','pitch','putt'}
def toks(s): return {w for w in re.findall(r'[a-z0-9]+', strip(s)) if w not in STOP and len(w) > 1}
_match_cache = {}
def rfeg_match(name):
    if name in _match_cache: return _match_cache[name]
    tn = toks(name); best = None; bs = 0
    for r in rf_list:
        tr = toks(r['key'])
        if not tn or not tr: continue
        inter = len(tn & tr)
        if not inter: continue
        s = inter / max(len(tn), len(tr)) + 0.25 * difflib.SequenceMatcher(None, ' '.join(sorted(tn)), ' '.join(sorted(tr))).ratio()
        if s > bs: bs, best = s, r
    res = best if bs >= 0.6 else None
    _match_cache[name] = res
    return res

GEO_P = SCR + 'geo_cache.json'
GEO = json.load(open(GEO_P)) if os.path.exists(GEO_P) else {}
def geocode(town, prov):
    k = f'{town}|{prov}'
    if k in GEO: return GEO[k]
    res = None
    alts = [town, re.sub(r'\s*\(.*?\)', '', town or '')] + re.findall(r'\((.*?)\)', town or '') + re.split(r'[-/,]', town or '')
    if prov and canon_prov(town or '') == prov: alts.append({'Illes Balears':'Palma','Asturias':'Oviedo','Cantabria':'Santander','Navarra':'Pamplona','La Rioja':'Logroño','Las Palmas':'Las Palmas de Gran Canaria','Bizkaia':'Bilbao','Gipuzkoa':'San Sebastián','Álava':'Vitoria'}.get(prov, prov))
    seen = set()
    for q in alts:
        q = (q or '').strip()
        if not q or q.lower() in seen or len(q) < 3: continue
        seen.add(q.lower())
        if not q: continue
        try:
            u = 'https://geocoding-api.open-meteo.com/v1/search?' + urllib.parse.urlencode({'name': q, 'count': 10, 'language': 'es', 'countryCode': 'ES'})
            d = json.loads(urllib.request.urlopen(u, timeout=20).read())
            for x in d.get('results', []):
                adm = strip(x.get('admin2', '') + ' ' + x.get('admin1', ''))
                keys = {strip(prov)} | {k for k, v in PROV_ALIAS.items() if v == prov} | {'balear'} if prov == 'Illes Balears' else {strip(prov)} | {k for k, v in PROV_ALIAS.items() if v == prov}
                if prov and any(k and k in adm for k in keys):
                    res = [round(x['latitude'], 3), round(x['longitude'], 3)]; break
            time.sleep(0.15)
        except Exception:
            time.sleep(1)
        if res: break
    GEO[k] = res
    return res

OVR = {'golf de pals':('Pals','Girona'),'golf club peralada':('Peralada','Girona'),"club de golf d'aro":("Castell-Platja d'Aro",'Girona'),'serres de pals golf & sport club':('Pals','Girona'),
 'derio golf':('Derio','Bizkaia'),'campo de golf de meis':('Meis','Pontevedra'),'arenal golf':('Benalmádena','Málaga'),'e. g. montepríncipe':('Boadilla del Monte','Madrid'),
 'villa nueva golf resort':('Puerto Real','Cádiz'),'roda golf':('San Javier','Murcia'),'campo de golf la finca':('Algorfa','Alicante'),'higuerón marbella golf resort':('Fuengirola','Málaga'),
 'quinto coto golf':(None,None),'air golf club':('Vegas de Matute','Segovia')}
def locate(club_name, code=None, nc_city=None):
    key = strip(club_name).strip() if club_name else ''
    ov = next((v for k, v in OVR.items() if strip(k) == key), None)
    r = None if ov else rfeg_match(club_name)
    town = prov = None
    if ov: town, prov = ov
    elif r:
        town, prov = r['town'], r['prov']
        cc = CODE_CCAA.get((code or '')[:2])
        if cc and PROV_CCAA.get(prov) and PROV_CCAA.get(prov) != cc: town = prov = None
    if nc_city and not town: town = nc_city
    ccaa = PROV_CCAA.get(prov) if prov else None
    if not ccaa and code: ccaa = CODE_CCAA.get(code[:2])
    ll = geocode(town, prov) if town and prov else None
    return town, prov, ccaa, ll

# ---------- Fuentes ----------
T = []
def add(o):
    o.setdefault('e', o['s'])
    if o['e'] < PAST or o['s'] > HORIZON: return
    T.append(o)

# NextCaddy
NC = json.load(open(SCR + 'nc_tours.json'))
ncc = {c['code']: c for c in json.load(open(SCR + 'nc_clubs.json'))}
FEDNAME = {'AM00':'Real Federación Andaluza de Golf','CM00':'Real Federación de Golf de Madrid','7700':'Federación de Golf de Castilla y León','CP00':'Federación Canaria de Golf'}
MES = {'ene':1,'feb':2,'mar':3,'abr':4,'may':5,'jun':6,'jul':7,'ago':8,'sep':9,'oct':10,'nov':11,'dic':12}
for o in NC.values():
    core = o['core']
    if re.search(r'\bFestivo\b', o['n']) or re.search(r'\bcursos?\b|\bexamen\b|\bcharla\b|\breuni[oó]n\b|\basamblea\b|\bclinics?\b', strip(o['n'])): continue
    cm = re.search(r'\|\s*([A-Z0-9]{4})\s*\|', core)
    code = cm.group(1) if cm else None
    dates = re.findall(r'\|\s*(?:lun|mar|mi[eé]|jue|vie|s[aá]b|dom)\s*\|\s*(\d{1,2})\s*\|\s*(ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)\s*\|', core)
    s = o['date']; e = s
    if len(dates) >= 2:
        y = int(s[:4]); d2, m2 = int(dates[1][0]), MES[dates[1][1]]
        ey = y + (1 if m2 < int(s[5:7]) else 0)
        e = f'{ey}-{m2:02d}-{d2:02d}'
    clubname = o['club'] or (ncc.get(code, {}).get('name') if code else '')
    if 'por determinar' in strip(clubname): continue
    town, prov, ccaa, ll = locate(clubname, code, ncc.get(code, {}).get('city') if code else None)
    fed = 'Real Federación Andaluza de Golf' if 'Real Federación Andaluza' in core[:200] else ('Real Federación de Golf de Madrid' if 'Federación de Golf de Madrid' in core[:200] else ('Federación de Golf de Castilla y León' if 'Castilla y Le' in core[:200] else ('Federación Canaria de Golf' if 'Canaria' in core[:200] else None)))
    org = 'Federación' if o['kind'] == 'fed' or re.search(r'\|\s*(RFGA|FGM|FGCYL|FCG)\s*\|', core) else 'Club'
    cat, sex, form, campo = infer(o['n'], org)
    if re.search(r'Señoras', core) and not re.search(r'Caballeros', core): sex = 'Femenino'
    if re.search(r'Caballeros', core) and not re.search(r'Señoras', core): sex = 'Masculino'
    prices = [p for _, p in o['tarifas']]
    t = {'n': nice(o['n']), 's': s, 'e': e, 'club': nice(clubname), 'city': town, 'prov': prov, 'ccaa': ccaa or 'Por confirmar',
         'cat': cat, 'sex': sex, 'mod': mod_from(o['mod_raw']), 'form': form, 'campo': campo, 'org': org,
         'price': min(prices) if prices else None, 'url': f'https://www.nextcaddy.com/tour/{o["id"]}', 'direct': True,
         'src': 'NextCaddy', 'via': fed or FEDNAME.get(o['list']) or 'Club', 'plazas': o.get('plazas'), 'll': ll}
    if len(prices) > 1: t['priceNote'] = 'Desde ' + (f'{min(prices):.2f}'.rstrip('0').rstrip('.').replace('.', ',')) + ' €, hay ' + str(len(prices)) + ' tarifas'
    if o.get('op'): t['op'] = o['op']
    if o.get('cl'): t['cl'] = o['cl']
    if o.get('ins_email') and not o.get('op'): t['insNote'] = 'Inscripción por email'
    if o.get('sace'): t['sace'] = True
    if o.get('results'): t['res'] = True
    add(t)

# Golf Directo
_gdc, _gdo = '/home/claude/raw/gd/clubs.json', '/home/claude/raw/gd/official.json'
GDC = {c['_id']: c for c in json.load(open(_gdc))['data']} if os.path.exists(_gdc) else {}
GD = json.load(open(_gdo)) if os.path.exists(_gdo) else {}
def local(iso):
    if not iso: return None
    return dt.datetime.fromisoformat(iso.replace('Z', '+00:00')).astimezone(MAD).date().isoformat()
for x in GD.values():
    g = x.get('nextGame') or {}
    cl = GDC.get((g.get('club') or {}).get('_id'))
    if not cl or cl['country'] != 'ESP': continue
    if x.get('__privacy') != 'public' or (g.get('privacy') or {}).get('privacy') not in (None, 'public'): continue
    name = x['name']
    if re.search(r'\btest\b|prueba de diseño|modelo hdcp|^entreno|\breservas?\b(?! del?\b)|\bclases?\b|\bclinics?\b|\bcursos?\b', strip(name)): continue
    # Los torneos solo para socios se publican: interesan a los socios de ese club (la web los marca como «solo socios»).
    s = local(g.get('scheduleStartDate') if x.get('__isSingleGame') else (x.get('__calendarStartDateVisible') or g.get('scheduleStartDate')))
    e = local(x.get('__calendarEndDate')) if not x.get('__isSingleGame') else s
    e = e or s
    if not s: continue
    if e < s: e = s
    town, prov, ccaa, ll = locate(cl['name'], cl.get('federationCode'))
    b = g.get('booking') or {}
    hint = 'Federación' if re.search(r'\bfed|federaci|\bfvg\b|fcgolf|\bfag\b|\bfbg\b|campeonato de (galicia|arag|balear|asturias|cantabria|navarra|la rioja|extremadura|castilla|euskadi|pais vasco|catalunya|murcia)|campionat de catalunya|ranking gallego|liga gallega|copa (galicia|pais vasco|catalunya)|puntuable|circuito (gallego|aragon|balear|navarr|extreme|riojan|cantabr|asturian|murcian)', strip(name)) else 'Club'
    cat, sex, form, campo = infer(name, hint)
    gm = (g.get('gameConfig') or {}).get('gameMode') or ''
    mod = mod_from((g.get('pointMode') or '') + ' ' + gm)
    if gm and gm != 'individual':
        if re.search(r'scramble', gm, re.I): mod = 'Scramble'
        elif re.search(r'greensome|chapman', gm, re.I): mod = 'Greensome'
        elif re.search(r'four', gm, re.I): mod = 'Fourball' if 'ball' in gm.lower() else 'Foursome'
        form = 'Parejas' if not re.search(r'team|equipo', gm, re.I) else 'Equipos'
    t = {'n': nice(name), 's': s, 'e': e, 'club': nice(cl['name']), 'city': town, 'prov': prov, 'ccaa': ccaa or 'Por confirmar',
         'cat': cat, 'sex': sex, 'mod': mod, 'form': form, 'campo': 'Pitch & Putt' if re.search(r'p&p|pitch', strip((g.get('course') or {}).get('name', ''))) else campo,
         'org': hint, 'price': None, 'url': f'https://www.golfdirecto.com/micro/game/{g["_id"]}/summary', 'direct': True,
         'src': 'Golf Directo', 'via': 'Golf Directo', 'll': ll, 'gid': g['_id']}
    if b.get('isEnabled'):
        bs, be = local(b.get('startDate')), local(b.get('endDate'))
        if bs and be and be >= bs:
            t['op'], t['cl'] = bs, be
    else:
        t['insNote'] = 'Inscripción a través del club'
    add(t)

# Federación de Golf de la Comunitat Valenciana
CV = json.load(open('/home/claude/raw/fed/cv.json'))
for x in CV:
    if 'FUERA DE LA C.V' in (x.get('campo') or '').upper(): continue
    name = x['torneo']
    town, prov = fix_town(x.get('poblacion')), canon_prov(x.get('provincia'))
    ll = geocode(town, prov) if town and prov else None
    cat, sex, form, campo = infer(name, 'Federación')
    t = {'n': nice(name), 's': x['fecha'], 'e': x['fechafin'] or x['fecha'], 'club': x['campo'], 'city': town, 'prov': prov, 'ccaa': 'Comunitat Valenciana',
         'cat': cat, 'sex': {'1': 'Masculino', '2': 'Femenino'}.get(x.get('sexo'), sex), 'mod': 'Sin indicar', 'form': form, 'campo': campo, 'org': 'Federación',
         'price': float(x['pvp']) if x.get('pvp') not in (None, '', '0') else None, 'url': f'https://golfcv.com/torneo_seek/ver-torneo/?torneoid={x["torneoid"]}', 'direct': True,
         'src': 'Federación de Golf de la Comunitat Valenciana', 'via': 'Federación de Golf de la Comunitat Valenciana', 'll': ll,
         'plazas': int(x['nummaximo']) if (x.get('nummaximo') or '0').isdigit() and int(x['nummaximo']) else None}
    if x.get('finicio', '0000')[:4] != '0000': t['op'], t['cl'] = x['finicio'], x['ffin']
    if x.get('pvpespecial') and x['pvpespecial'] != x['pvp'] and x['pvpespecial'] not in ('0', ''): t['priceNote'] = f'{x["pvpespecial"]} € tarifa especial'
    add(t)

# Manuales verificados (organizadores sin plataforma común)
for m in json.load(open(SCR + 'manual.json')):
    town, prov = m.get('city'), m.get('prov')
    m['ll'] = geocode(town, prov) if town and prov else None
    m.setdefault('ccaa', PROV_CCAA.get(prov, 'Por confirmar'))
    add(m)

# Calendarios propios de federaciones (fed_extra.py)
EXTRA_P = '/home/claude/raw/fed2/extra.json'
EXTRA = json.load(open(EXTRA_P))['records'] if os.path.exists(EXTRA_P) else []
STRICT = {'Federación Vasca de Golf', 'Federación de Golf de Castilla-La Mancha', 'Federación de Golf del Principado de Asturias'}
GD_IDS = {t.get('gid') for t in T if t.get('gid')}
for x in EXTRA:
    if x.get('gid') and x['gid'] in GD_IDS: continue
    town = prov = ccaa = ll = None
    if x.get('club'): town, prov, ccaa, ll = locate(x['club'])
    if ccaa and ccaa != x['ccaa'] and x.get('only_ccaa'): continue
    if not ccaa and x['src'] in STRICT and x.get('only_ccaa'): continue
    if not prov and x.get('prov'):
        prov = x['prov']; ll = ll or geocode(prov, prov)
    cat, sex, form, campo = infer(x['n'], x.get('org', 'Federación'))
    t = {'n': nice(x['n']), 's': x['s'], 'e': x.get('e', x['s']), 'club': nice(x['club']) if x.get('club') else 'Por confirmar', 'city': town, 'prov': prov or 'Por confirmar',
         'ccaa': x['ccaa'], 'cat': cat, 'sex': sex, 'mod': mod_from(x['n']), 'form': form, 'campo': campo, 'org': x.get('org', 'Federación'),
         'price': None, 'url': x['url'], 'direct': x.get('direct', True), 'src': x['src'], 'via': x.get('via') or x['src'], 'll': ll}
    for k in ('op', 'cl', 'insNote', 'gid', 'res'):
        if x.get(k): t[k] = x[k]
    add(t)

# ---------- Duplicados ----------
def nkey(s): return ' '.join(sorted(toks(s)))
# Rasgos que distinguen torneos distintos del mismo día y club: categoría, sexo, número de prueba, turno, formato.
DISC = {
    'cat': r'benjamin(?:es)?|alevin(?:es)?|infantil(?:es)?|cadetes?|junior|juvenil(?:es)?|sub\s?-?\d\d|u\d\d|seniors?|mid[- ]?amateur|absolut[oa]s?|boys|girls|escuela|pequecircuito|profesional(?:es)?|pro[- ]?am',
    'sex': r'masculin[oa]s?|femenin[oa]s?|caballeros|damas|senoras|mixt[oa]s?|ladies|men|women',
    'num': r'\d+(?:a|o|er)?',
    'turno': r'manana|tarde',
    'form': r'parejas|individual|fourball|foursome|greensome|scramble|stableford|medal|match ?play|pitch|p ?& ?p',
}
def disc(n):
    t = strip(n)
    return {k: frozenset((re.sub(r'\D', '', m.group(0)) if k == 'num' else m.group(0).replace(' ', '')) for m in re.finditer(r'\b(?:' + rx + r')\b', t)) for k, rx in DISC.items()}
def distintos(a, b):
    """True si los nombres dicen claramente que son torneos distintos (p. ej. Alevín y Benjamín el mismo día)."""
    da, db = disc(a['n']), disc(b['n'])
    for k in da:
        if da[k] and db[k] and da[k] != db[k]:
            return True
    return False
import collections as _c
SEPARADOS = _c.Counter()
PRI = {'NextCaddy': 3, 'Federación de Golf de la Comunitat Valenciana': 3, 'RFEG': 4, 'Golf Directo': 2}
T.sort(key=lambda t: (t['s'], -PRI.get(t['src'], 1)))
kept = []
for t in T:
    dup = False
    for k in kept:
        if k['s'] != t['s']: continue
        same_place = (k.get('club') and t.get('club') and (toks(k['club']) & toks(t['club']))) or (k.get('city') and k.get('city') == t.get('city'))
        sim = difflib.SequenceMatcher(None, nkey(k['n']), nkey(t['n'])).ratio()
        tk, tt = toks(k['n']) - {'torneo','inscripciones','inscripcion'}, toks(t['n']) - {'torneo','inscripciones','inscripcion'}
        subset = tk and tt and (tk <= tt or tt <= tk) and min(len(tk), len(tt)) >= 2
        if not ((same_place and (sim > 0.72 or subset)) or sim > 0.9): continue
        # Misma plataforma y distinto enlace = la propia plataforma los publica como torneos distintos.
        if k['src'] == t['src'] and k['url'] != t['url']: SEPARADOS['misma fuente'] += 1; continue
        if distintos(k, t): SEPARADOS['categoría, sexo, prueba o turno distintos'] += 1; continue
        if True:
            dup = True
            for f in ('price', 'op', 'cl', 'plazas', 'll', 'city', 'prov', 'res'):
                if k.get(f) in (None, '') and t.get(f) not in (None, ''): k[f] = t[f]
            if k.get('mod') == 'Sin indicar' and t.get('mod') != 'Sin indicar': k['mod'] = t['mod']
            k.setdefault('also', []).append(t['url'])
            break
    if not dup: kept.append(t)

json.dump(GEO, open(GEO_P, 'w'), ensure_ascii=False)
json.dump(kept, open(SCR + 'tournaments.json', 'w'), ensure_ascii=False)
import collections
print('total', len(T), 'tras duplicados', len(kept), '- no fusionados por ser distintos:', dict(SEPARADOS))
print(collections.Counter(t['src'] for t in kept))
print(collections.Counter(t['ccaa'] for t in kept).most_common())
print('sin coordenadas', sum(1 for t in kept if not t.get('ll')), 'sin provincia', sum(1 for t in kept if not t.get('prov')))
print('con precio', sum(1 for t in kept if t.get('price') is not None), 'con plazo', sum(1 for t in kept if t.get('cl')))
