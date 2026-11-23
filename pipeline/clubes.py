#!/usr/bin/env python3
"""Banderín - directorio de clubes con campo de toda España, con su localidad, provincia y coordenadas.

Fuentes: el directorio de clubes de la RFEG (pipeline/datos/rfeg_clubes.json, sacado con rfeg_clubs.py)
y los clubes que ya aparecen en los torneos de Banderín. Las coordenadas son las del torneo cuando las hay
y, si no, las de la localidad (Nominatim / OpenStreetMap, una petición por segundo, con caché).
Genera site/clubes.js:  window.CLUBES=[[nombre, localidad, provincia, lat, lng, hoyos], ...]
  python3 pipeline/clubes.py
"""
import json, os, re, sys, time, unicodedata, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, '..', 'site')
CACHE = os.path.join(HERE, 'datos', 'clubes_geo.json')


def norm(s):
    s = unicodedata.normalize('NFD', (s or '').lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()


def key(name):  # para emparejar «Real Club Valderrama» con «Real Club de Golf Valderrama»
    w = [x for x in norm(name).split() if x not in ('club', 'de', 'golf', 'real', 'el', 'la', 'los', 'las', 'del', 'campo', 'c', 'r', 'cg', 'rcg', 'country', 'resort', 'municipal', 'sa', 's', 'a', 'sl', 'l', 'y', 'i', 'd')]
    return ' '.join(w)


def fix_city(c):  # «Caldas, las» -> «Las Caldas»
    m = re.match(r'^(.*), (el|la|los|las|o|a|os|as|es|sa|ses|l\'|els|les)$', c or '', re.I)
    c = (m.group(2) + ' ' + m.group(1)) if m else (c or '')
    return ' '.join(w if w.lower() in ('de', 'del', 'la', 'las', 'los', 'el', 'y', 'i', 'd\'') and i else w[:1].upper() + w[1:] for i, w in enumerate(c.split()))


def load_js(name, var):
    s = open(os.path.join(SITE, name), encoding='utf-8').read()
    return json.loads(s[s.index(var + '=') + len(var) + 1:].rstrip().rstrip(';'))


T = load_js('data.js', 'window.TORNEOS') + load_js('pasados.js', 'window.PASADOS')
PROVS = {norm(t['prov']): t['prov'] for t in T if t.get('prov') and t['prov'] != 'Por confirmar'}
PROVS.update({'illes balears': 'Baleares', 'islas baleares': 'Baleares', 'gerona': 'Girona', 'lerida': 'Lleida', 'orense': 'Ourense', 'la coruna': 'A Coruña', 'coruna a': 'A Coruña',
              'vizcaya': 'Bizkaia', 'guipuzcoa': 'Gipuzkoa', 'alava': 'Álava', 'tenerife': 'Santa Cruz de Tenerife', 'palmas las': 'Las Palmas', 'rioja la': 'La Rioja'})
FAILS = [0]
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
old = json.load(open(os.path.join(HERE, 'geo_cache.json')))


def geocode(city, prov):
    k = city + '|' + prov
    if k in old: return old[k]
    if k in cache: return cache[k]
    if '--sin-red' in sys.argv: return None
    q = urllib.parse.urlencode({'q': ', '.join(x for x in (city, prov, 'España') if x), 'format': 'json', 'limit': 1, 'countrycodes': 'es'})
    try:
        req = urllib.request.Request('https://nominatim.openstreetmap.org/search?' + q, headers={'User-Agent': 'BanderinBot/1.0 (+https://banderin.es)'})
        r = json.loads(urllib.request.urlopen(req, timeout=30).read())
        cache[k] = [round(float(r[0]['lat']), 3), round(float(r[0]['lon']), 3)] if r else None
    except Exception as e:
        print('geo', k, e, flush=True); time.sleep(3); FAILS[0] += 1
        if FAILS[0] > 8: sys.argv.append('--sin-red')
        return None
    time.sleep(1.1)
    json.dump(cache, open(CACHE, 'w'), ensure_ascii=False, indent=0)
    return cache[k]


clubs = {}  # clave -> [nombre, localidad, provincia, lat, lng, hoyos]
for t in T:  # los de Banderín mandan: sus nombres son los que salen en los torneos
    c = t.get('club')
    if not c or t.get('prov') in (None, '', 'Por confirmar'): continue
    k = key(c) or norm(c)
    cur = clubs.get(k)
    ll = t.get('ll') or [None, None]
    if not cur: clubs[k] = [c, (t.get('city') or '').split(' (')[0].title(), t['prov'], ll[0], ll[1], 0]
    elif cur[3] is None and ll[0] is not None: cur[3], cur[4] = ll
for slug, ts in json.load(open(os.path.join(HERE, 'datos', 'rfeg_clubes.json'))).items():
    ts = [x for x in ts if x != 'Ver Club']
    holes = 0
    if ts and re.match(r'^\d+ hoyos$', ts[0]): holes = int(ts[0].split()[0]); ts = ts[1:]
    if not holes or len(ts) < 3: continue  # sin campo propio: no es un sitio donde quedar a jugar
    name, city, prov = ts[0], fix_city(ts[1]), PROVS.get(norm(ts[2]), ts[2])
    k = key(name) or norm(name)
    if k in clubs:
        clubs[k][5] = holes
        if not clubs[k][1]: clubs[k][1] = city
    else: clubs[k] = [name, city, prov, None, None, holes]
n = 0
for c in clubs.values():
    if c[3] is None and (c[1] or c[2]):
        ll = geocode(c[1], c[2]) or (geocode('', c[2]) if c[1] else None)
        if ll: c[3], c[4] = ll
        n += 1
        if n % 25 == 0: print(n, 'localidades', flush=True)
FIX = {'Jaen': 'Jaén', 'Calafell': 'Tarragona', 'Mont-roig del Camp': 'Tarragona'}
for c in clubs.values(): c[2] = FIX.get(c[2], c[2])
out = sorted(clubs.values(), key=lambda c: norm(c[0]))
open(os.path.join(SITE, 'clubes.js'), 'w', encoding='utf-8').write('window.CLUBES=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n')
print('clubes: %d (%d con coordenadas)' % (len(out), sum(1 for c in out if c[3] is not None)))
