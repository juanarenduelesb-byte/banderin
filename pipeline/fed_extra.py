# Calendarios propios de federaciones que no están (o no del todo) en NextCaddy ni Golf Directo.
# Escribe /home/claude/raw/fed2/extra.json con registros sin normalizar; build.py los localiza y clasifica.
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import red  # BanderinBot: robots.txt, pausa e identificación
import re, html, json, time, datetime as dt, urllib.request, urllib.parse, http.cookiejar, subprocess, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ics

OUT = '/home/claude/raw/fed2/'
os.makedirs(OUT, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (Banderin)'}
TODAY = dt.date.today()
PAST = (TODAY - dt.timedelta(days=45)).isoformat()
HORIZON = (TODAY + dt.timedelta(days=330)).isoformat()
MES = {'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'ago': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dic': 12}
MESL = {'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12}
SKIP = re.compile(r'reuni[oó]n|asamblea|curso|clinic|charla|examen|festivo|concentraci[oó]n|entrenamiento|gala\b', re.I)

def get(url, data=None, headers=None, opener=None, tries=3):
    for k in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers={**UA, **(headers or {})})
            return (opener.open(req, timeout=40) if opener else urllib.request.urlopen(req, timeout=40)).read()
        except Exception:
            time.sleep(2 + 2 * k)
    return None
def text(h):
    t = re.sub(r'<script.*?</script>|<style.*?</style>', '', h, flags=re.S)
    t = re.sub(r'<[^>]+>', ' | ', t); t = html.unescape(t)
    t = re.sub(r'(\s*\|\s*)+', ' | ', t); return re.sub(r'\s+', ' ', t)
def inwin(s, e): return (e or s) >= PAST and s <= HORIZON

R = []; STATUS = {}
def rec(**k):
    k.setdefault('e', k['s'])
    if not k.get('n') or not inwin(k['s'], k['e']) or SKIP.search(k['n']): return
    R.append(k)

def run(name, fn):
    n0 = len(R)
    try:
        fn(); STATUS[name] = {'ok': True, 'n': len(R) - n0}
    except Exception as ex:
        STATUS[name] = {'ok': False, 'n': len(R) - n0, 'error': str(ex)[:200]}
    print(name, STATUS[name])

# ---------------- Cataluña: Federació Catalana de Golf ----------------
def cataluna():
    cj = http.cookiejar.CookieJar(); op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    h = get('https://www.catgolf.com/es/calendario-fcgolf', opener=op).decode()
    tok = re.search(r'name="csrf-token" content="([^"]+)"', h).group(1)
    seen = set(); m = (TODAY - dt.timedelta(days=45)).replace(day=1); fails = 0
    for i in range(13):
        b = (m.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
        data = urllib.parse.urlencode([('ludico', 0), ('competicion', 0), ('start', m.isoformat()), ('end', b.isoformat())]).encode()
        r = get('https://www.catgolf.com/es/calendar/events', data=data, opener=op, headers={'X-CSRF-TOKEN': tok, 'X-Requested-With': 'XMLHttpRequest'})
        m = b
        if not r: fails += 1; continue
        d = json.loads(r)
        F = d.get('tournamentsFGC') or []
        F = list(F.values()) if isinstance(F, dict) else F
        C = []
        cl = d.get('tournamentsClubs') or {}
        if isinstance(cl, dict):
            for lst in cl.values(): C += list(lst.values()) if isinstance(lst, dict) else lst
        for t, org in [(x, 'Federación') for x in F] + [(x, 'Club') for x in C]:
            if t['id'] in seen or not t.get('active', 1): continue
            seen.add(t['id'])
            club = (t.get('club') or {}).get('name')
            o = dict(n=t['title'].strip(), s=t['starting_date'], e=t.get('ending_date') or t['starting_date'], club=club,
                     url='https://www.catgolf.com/es' + t['route'], direct=True, src='Federació Catalana de Golf',
                     via='Federació Catalana de Golf' if org == 'Federación' else (club or 'Club'), org=org, ccaa='Cataluña', only_ccaa=True)
            a, z = t.get('starting_inscription_date'), t.get('ending_inscription_date')
            if a and a[:4] != '0000': o['op'] = a
            if z and z[:4] != '0000': o['cl'] = z
            rec(**o)
    if fails > 6: raise RuntimeError(f'{fails} meses sin respuesta')
    # Enlace de inscripción en Golf Directo de cada prueba próxima (de ahí sale el precio)
    import concurrent.futures as cf
    todo = [r for r in R if r['src'] == 'Federació Catalana de Golf' and r['e'] >= TODAY.isoformat()]
    def gid_of(r):
        h = get(r['url'])
        if not h: return
        m = re.search(r'golfdirecto\.com/(?:next/)?micro/game/([0-9a-f]{24})', h.decode('utf8', 'ignore'))
        if m: r['gid'] = m.group(1)
    with cf.ThreadPoolExecutor(6) as ex: list(ex.map(gid_of, todo))

# ---------------- País Vasco: Federación Vasca y territoriales (Google Calendar) ----------------
def pais_vasco():
    h = get('https://www.fvgolf.com/es/competiciones/calendario/').decode('utf8', 'ignore')
    ids = list(dict.fromkeys(re.findall(r'src=([a-z0-9]+)%40group\.calendar\.google\.com', html.unescape(h))))
    if not ids: raise RuntimeError('sin calendarios')
    for i in ids:
        cal, ev = ics.parse(ics.fetch(f'https://calendar.google.com/calendar/ical/{i}%40group.calendar.google.com/public/basic.ics'))
        for e in ev:
            if e['status'] == 'CANCELLED' or e['rrule']: continue
            loc = re.split(r',', e['loc'])[0].strip() if e['loc'] else None
            link = re.search(r'https?://[^\s"<>]+', e['desc'] or '')
            rec(n=e['n'], s=e['s'], e=e['e'], club=loc, url=link.group(0) if link and 'fvgolf' in link.group(0) else 'https://www.fvgolf.com/es/competiciones/calendario/',
                direct=bool(link and 'fvgolf' in link.group(0)), src='Federación Vasca de Golf', via=cal or 'Federación Vasca de Golf', org='Federación',
                ccaa='País Vasco', only_ccaa=True)

# ---------------- Navarra: Federación Navarra de Golf ----------------
NAV = {'ZUASTI': 'Señorío de Zuasti Club de Golf', 'LIZASO': 'Club de Golf Ulzama', 'ULZAMA': 'Club de Golf Ulzama', 'GORRAIZ': 'Club de Golf Castillo de Gorraiz', 'CASTILLO DE GORRAIZ': 'Club de Golf Castillo de Gorraiz', 'ARAZURI': 'Club de Golf Ulzama', 'SENDAVIVA': 'Golf Sendaviva', 'ESPARZA': 'Club Golf Señorío de Zuasti'}
def navarra():
    h = get('https://fnavarragolf.com/calendario-inscripciones/').decode('utf8', 'ignore')
    blocks = h.split('contact_box')[1:]
    if 'contact_box' not in h: raise RuntimeError('estructura cambiada')
    for b in blocks:
        t = text(b)
        tm = re.search(r'^[^|]*\|\s*([^|]+?)\s*\|\s*Fecha', t)
        ds = re.findall(r'(\d{1,2})/(\d{1,2})/(\d{2,4})\s*\(([^)]+)\)', t)
        if not tm or not ds: continue
        dates = [f'{(2000 + int(y)) if len(y) == 2 else int(y)}-{int(mo):02d}-{int(d):02d}' for d, mo, y, _ in ds]
        place = ds[0][3].strip().upper()
        link = re.search(r'href="(https://fnavarragolf\.com/calendar/[^"]+)"', b)
        rec(n=tm.group(1), s=min(dates), e=max(dates), club=NAV.get(place, place.title()), url=link.group(1) if link else 'https://fnavarragolf.com/calendario-inscripciones/',
            direct=bool(link), src='Federación Navarra de Golf', via='Federación Navarra de Golf', org='Federación', ccaa='Comunidad Foral de Navarra', prov='Navarra',
            insNote='Pago en el club' if 'En el club' in t else None)

# ---------------- Cantabria: Federación Cántabra de Golf ----------------
def cantabria():
    a = (TODAY - dt.timedelta(days=45)).isoformat(); b = HORIZON
    d = json.loads(get(f'https://federacioncantabradegolf.com/wp-admin/admin-ajax.php?action=whb_rounds_feed&start={a}&end={b}'))
    for e in d:
        rec(n=html.unescape(e['title']), s=e['start'][:10], e=(e.get('end') or e['start'])[:10], club=(e.get('extendedProps') or {}).get('course'),
            url=e['url'], direct=True, src='Federación Cántabra de Golf', via='Federación Cántabra de Golf', org='Federación', ccaa='Cantabria', prov='Cantabria')

# ---------------- La Rioja: Federación Riojana de Golf (calendario en PDF) ----------------
RIO = {'EL CAMPO DE LOGROÑO': 'El Campo de Logroño', 'RIOJA ALTA GOLF CLUB': 'Rioja Alta Golf Club', 'CLUB DE CAMPO SOJUELA': 'Club de Campo Sojuela', 'SOJUELA': 'Club de Campo Sojuela'}
def rioja():
    h = get('https://frgolf.es/calendario').decode('utf8', 'ignore')
    pdfs = sorted(set(re.findall(r'https://frgolf\.es/wp-content/uploads/\d{4}/\d{2}/[^"\']*Calendario(\d{4})[^"\']*\.pdf', h)))
    urls = re.findall(r'(https://frgolf\.es/wp-content/uploads/\d{4}/\d{2}/[^"\']*Calendario\d{4}[^"\']*\.pdf)', h)
    if not urls: raise RuntimeError('sin PDF de calendario')
    for url in dict.fromkeys(urls):
        year = int(re.search(r'Calendario(\d{4})', url).group(1))
        if year < TODAY.year - 1 or year > TODAY.year + 1: continue
        p = OUT + f'rioja{year}.pdf'; open(p, 'wb').write(get(url))
        try: txt = subprocess.run(['pdftotext', '-layout', p, '-'], capture_output=True, text=True, timeout=60).stdout
        except Exception: txt = ''
        if not txt.strip():
            import pypdf; txt = '\n'.join(pg.extract_text() or '' for pg in pypdf.PdfReader(p).pages)
        mon = None
        for line in txt.splitlines():
            ml = line.strip().lower()
            if ml in MESL: mon = MESL[ml]; continue
            m = re.match(r'\s*(\d{1,2}(?:/\d{1,2})?(?:\s*y\s*)?(?:[\d\-y ]*?))\s{2,}(.+?)\s{2,}(\S.*)$', line)
            if not m or not mon: continue
            dd, name, place = m.group(1), m.group(2).strip(), m.group(3).strip()
            if 'ESPAÑA' in name.upper() and 'RIOJA' not in place.upper() and place.upper() not in RIO: continue
            nums = [int(x) for x in re.findall(r'\d{1,2}', dd)]
            if '/' in dd: s = f'{year}-{mon - 1:02d}-{nums[0]:02d}'; e = f'{year}-{mon:02d}-{nums[-1]:02d}'
            else: s = f'{year}-{mon:02d}-{nums[0]:02d}'; e = f'{year}-{mon:02d}-{max(nums):02d}'
            club = RIO.get(place.upper(), place.title() if '/' not in place else 'Varios campos')
            rec(n=name.title().replace('Cto ', 'Campeonato ').replace('Frg', 'FRG').replace('P&P', 'Pitch & Putt'), s=s, e=e, club=club, url=url, direct=False,
                src='Federación Riojana de Golf', via='Federación Riojana de Golf', org='Federación', ccaa='La Rioja', prov='La Rioja', only_ccaa=False)

# ---------------- Castilla-La Mancha: calendario oficial de la federación ----------------
def clm():
    h = get('https://fedgolfclm.com/inscripciones-y-resultados-torneos-fed-castilla-la-mancha/').decode('utf8', 'ignore')
    main = h.split('CATEGORÍAS ESPECÍFICAS')[0]
    for blk in re.findall(r'<div[^>]*class="mes-bloque"[^>]*>(.*?)</ul>', main, re.S):
        mt = re.search(r'mes-title">\s*([A-Za-zéá]+)\s+(\d{4})', blk)
        if not mt: continue
        year = int(mt.group(2))
        for li in re.findall(r'<li class="torneo-item">(.*?)</li>', blk, re.S):
            f = re.search(r'class="fecha">([^<]+)<', li); nm = re.search(r'class="nombre-torneo"[^>]*>(.*?)</(?:a|span)>', li, re.S)
            lg = re.search(r'class="lugar">\s*-?\s*([^<]+)<', li); ln = re.search(r'class="nombre-torneo" href="([^"]+)"', li)
            if not f or not nm: continue
            fs = f.group(1).strip().lower()
            mm = re.findall(r'(\d{1,2})\s*([a-z]{3})?', fs)
            ms = [MES.get(x[1]) for x in mm if x[1]]
            if not ms: continue
            d1, d2 = int(mm[0][0]), int(mm[-1][0]); m1 = MES.get(mm[0][1]) or ms[-1]; m2 = ms[-1]
            s = f'{year}-{m1:02d}-{d1:02d}'; e = f'{year}-{m2:02d}-{d2:02d}'
            place = (lg.group(1).strip() if lg else '')
            place = re.split(r'\s+y\s+|,', place)[0].strip() or None
            rec(n=html.unescape(re.sub(r'<[^>]+>', '', nm.group(1))).strip(), s=s, e=e, club=place, url=ln.group(1) if ln else 'https://fedgolfclm.com/inscripciones-y-resultados-torneos-fed-castilla-la-mancha/',
                direct=False, src='Federación de Golf de Castilla-La Mancha', via='Federación de Golf de Castilla-La Mancha', org='Federación', ccaa='Castilla-La Mancha',
                only_ccaa=True, insNote='Inscripción en la app FGCLM Torneos')

# ---------------- Asturias: Federación de Golf del Principado de Asturias ----------------
MESW = {**MESL}
def asturias():
    h = get('https://www.fedegolfasturias.com/competiciones').decode('utf8', 'ignore')
    slug = {}
    for m in re.finditer(r'/competicion/([^"/]+)/(\d+)"', h):
        near = text(h[m.end():m.end() + 900]).lower()
        ds = [f'{int(y)}-{MESW[mo]:02d}-{int(dd):02d}' for dd, mo, y in re.findall(r'(\d{1,2})\s+([a-záéíóú]+)\s+(\d{4})', near)[:2] if mo in MESW]
        if ds and max(ds) < PAST: continue
        slug.setdefault(m.group(2), m.group(1))
    for cid, sl in slug.items():
        url = f'https://www.fedegolfasturias.com/competicion/{sl}/{cid}'
        d = get(url)
        if not d: continue
        tx = text(d.decode('utf8', 'ignore'))
        nm = re.search(r'\|\s*Competición\s*\|\s*([^|]+?)\s*\|\s*Comité', tx)
        fe = re.search(r'Fechas\s*\|\s*([^|]+?)\s*\|\s*Lugar\s*\|\s*([^|]+?)\s*\|', tx)
        if not nm or not fe: continue
        ds = re.findall(r'(\d{1,2})\s+([a-záéíóú]+)\s+(\d{4})', fe.group(1).lower())
        dates = [f'{int(y)}-{MESW[mo]:02d}-{int(dd):02d}' for dd, mo, y in ds if mo in MESW]
        if not dates or max(dates) < PAST: continue
        o = dict(n=nm.group(1), s=min(dates), e=max(dates), club=fe.group(2).title(), url=url,
                 direct=True, src='Federación de Golf del Principado de Asturias', via='Federación de Golf del Principado de Asturias', org='Federación',
                 ccaa='Principado de Asturias', only_ccaa=True)
        pl = re.search(r'Plazo abierto desde el [^,]+,\s*(\d{1,2})\s+([a-záéíóú]+)\s+(\d{4}).*?hasta el [^,]+,\s*(\d{1,2})\s+([a-záéíóú]+)\s+(\d{4})', tx.lower())
        if pl and pl.group(2) in MESW and pl.group(5) in MESW:
            o['op'] = f'{pl.group(3)}-{MESW[pl.group(2)]:02d}-{int(pl.group(1)):02d}'; o['cl'] = f'{pl.group(6)}-{MESW[pl.group(5)]:02d}-{int(pl.group(4)):02d}'
        rec(**o)
        time.sleep(0.2)

# ---------------- Golf Directo: partidas que las federaciones enlazan pero no salen en el listado público ----------------
def have_gd():
    s = set()
    try:
        for t in json.load(open('/home/claude/scr/tournaments.json')):
            for u in [t['url']] + t.get('also', []):
                m = re.search(r'game/([0-9a-f]{24})', u)
                if m: s.add(m.group(1))
            if t.get('gid'): s.add(t['gid'])
    except Exception: pass
    try:
        for x in json.load(open('/home/claude/raw/gd/official.json')).values():
            g = (x.get('nextGame') or {}).get('_id')
            if g: s.add(g)
    except Exception: pass
    return s
def gd_game(gid, via, ccaa):
    r = get(f'https://www.golfdirecto.com/api/v2/public/game/{gid}/active')
    if not r: return
    d = json.loads(r)
    if d.get('code') != 0: return
    g = d['data']
    if (g.get('privacy') or {}).get('privacy') != 'public' or g.get('status') == 'cancelled': return
    st = g.get('scheduleStartDate')
    if not st: return
    s = (dt.datetime.fromisoformat(st.replace('Z', '+00:00')) + dt.timedelta(hours=1)).date().isoformat()
    nm = g['name']
    tn = (g.get('tournament') or {}).get('name')
    if tn and (re.match(r'^(ronda|jornada|d[ií]a|vuelta|round)\s*\d*$', nm.strip(), re.I) or len(nm) < 6): nm = tn
    o = dict(n=nm, s=s, club=(g.get('club') or {}).get('name'), url=f'https://www.golfdirecto.com/micro/game/{gid}/summary', direct=True,
             src='Golf Directo', via=via, org='Federación', ccaa=ccaa, only_ccaa=True, gid=gid)
    if g.get('status') == 'finished' and (g.get('privacy') or {}).get('publicResults') and (g.get('__playersCount') or 0) > 0: o['res'] = True
    rec(**o)
def galicia():
    h = get('https://www.fggolf.com/torneos.aspx').decode('utf8', 'ignore')
    have = have_gd(); n = 0
    for gid in dict.fromkeys(re.findall(r'game/([0-9a-f]{24})', h)):
        n += 1
        if gid not in have: gd_game(gid, 'Federación Gallega de Golf', 'Galicia')
    if not n: raise RuntimeError('sin enlaces a Golf Directo')
    STATUS.setdefault('_galicia_links', n)
def aragon():
    base = 'https://www.aragongolf.com'
    h = get(base + '/torneos/').decode('utf8', 'ignore')
    groups = [g for g in dict.fromkeys(re.findall(r'href="(/torneos/grupo/[^"]+)"', h)) if re.search(r'%d|%d' % (TODAY.year, TODAY.year + 1), g)]
    fichas = set(re.findall(r'torneos-ficha/(\d+)', h)) | set(re.findall(r'torneos-ficha/(\d+)', (get(base + '/') or b'').decode('utf8', 'ignore')))
    for g in groups:
        fichas |= set(re.findall(r'torneos-ficha/(\d+)', (get(base + g) or b'').decode('utf8', 'ignore')))
    have = have_gd()
    for fid in sorted(fichas, key=int):
        d = get(f'{base}/torneos-ficha/{fid}/')
        if not d: continue
        d = d.decode('utf8', 'ignore'); tx = text(d)
        g = re.search(r'golfdirecto\.com/(?:next/)?micro/game/([0-9a-f]{24})', d)
        if g and g.group(1) in have: continue
        dd = re.search(r'al (\d{1,2}) de ([a-z]+) de (\d{4})', tx)
        if dd and dd.group(2) in MESL and f'{dd.group(3)}-{MESL[dd.group(2)]:02d}-{int(dd.group(1)):02d}' < PAST: continue
        if g: gd_game(g.group(1), 'Federación Aragonesa de Golf', 'Aragón'); continue
        m = re.search(r'\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*Del (\d{1,2}) de ([a-z]+) de (\d{4})\s*\|\s*al (\d{1,2}) de ([a-z]+) de (\d{4})', tx)
        if not m or m.group(4) not in MESL: continue
        s = f'{m.group(5)}-{MESL[m.group(4)]:02d}-{int(m.group(3)):02d}'; e = f'{m.group(8)}-{MESL[m.group(7)]:02d}-{int(m.group(6)):02d}'
        rec(n=m.group(1), s=s, e=e, club=m.group(2), url=f'{base}/torneos-ficha/{fid}/', direct=False, src='Federación Aragonesa de Golf',
            via='Federación Aragonesa de Golf', org='Federación', ccaa='Aragón', only_ccaa=True)


# ---------------- Murcia: Federación de Golf de la Región de Murcia (The Events Calendar) ----------------
def murcia():
    page = 1
    while page <= 10:
        r = get(f'https://fgolfmurcia.com/wp-json/tribe/events/v1/events?start_date={PAST}&end_date={HORIZON}&per_page=50&page={page}')
        if not r: raise RuntimeError('sin respuesta')
        d = json.loads(r)
        for e in d.get('events', []):
            title = html.unescape(e['title']).strip()
            ven = e.get('venue') if isinstance(e.get('venue'), dict) else {}
            club = (ven or {}).get('venue')
            parts = re.split(r'\s+[–-]\s+', title)
            if not club and len(parts) > 1: club = parts[-1]
            name = parts[0] if len(parts) > 1 and club and parts[-1].strip().lower() == (club or '').strip().lower() else title
            if club and re.search(r'FGCV|FGRM|FGCLM|RFGA', club): club = None
            rec(n=name, s=e['start_date'][:10], e=e['end_date'][:10], club=html.unescape(club) if club else None, url=e['url'], direct=True,
                src='Federación de Golf de la Región de Murcia', via='Federación de Golf de la Región de Murcia', org='Federación', ccaa='Región de Murcia', prov='Murcia')
        if page >= (d.get('total_pages') or 1): break
        page += 1

for name, fn in [('Cataluña', cataluna), ('País Vasco', pais_vasco), ('Navarra', navarra), ('Cantabria', cantabria), ('La Rioja', rioja),
                 ('Castilla-La Mancha', clm), ('Asturias', asturias), ('Galicia', galicia), ('Aragón', aragon), ('Murcia', murcia)]:
    run(name, fn)
R = [{k: v for k, v in r.items() if v is not None} for r in R]
json.dump({'records': R, 'status': STATUS, 'when': dt.datetime.now().isoformat(timespec='minutes')}, open(OUT + 'extra.json', 'w'), ensure_ascii=False)
print('total', len(R))
