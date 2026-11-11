#!/usr/bin/env python3
"""Banderín · páginas para buscadores.

Lee site/data.js y genera, sin JavaScript, lo que Google necesita para
entender y posicionar la web:

  site/torneos-golf/index.html                 todas las comunidades
  site/torneos-golf/<comunidad>/index.html     una por comunidad
  site/torneos-golf/<comunidad>/<provincia>/   una por provincia
  site/en/index.html                           portada en inglés (copia de index.html)
  site/sitemap.xml
  y rellena en site/index.html los enlaces del pie y la descripción.

Se ejecuta cada día después de actualizar los datos (ver
.github/workflows/actualizar.yml) y antes de cada publicación manual:

  python3 pipeline/seo.py
"""
import datetime as dt
import html
import json
import re
import shutil
import unicodedata
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = 'https://banderin.es'
SITE = Path(__file__).resolve().parent.parent / 'site'
HUB = 'torneos-golf'
TODAY = dt.datetime.now(ZoneInfo('Europe/Madrid')).date()
ISO = TODAY.isoformat()

# Comunidad -> (nombre corto para titulares, provincias). Las comunidades de
# una sola provincia no tienen páginas de provincia: serían la misma página.
CCAA = {
    'Andalucía': ('Andalucía', ['Almería', 'Cádiz', 'Córdoba', 'Granada', 'Huelva', 'Jaén', 'Málaga', 'Sevilla']),
    'Aragón': ('Aragón', ['Huesca', 'Teruel', 'Zaragoza']),
    'Principado de Asturias': ('Asturias', []),
    'Illes Balears': ('Baleares', []),
    'Canarias': ('Canarias', ['Las Palmas', 'Santa Cruz de Tenerife']),
    'Cantabria': ('Cantabria', []),
    'Castilla y León': ('Castilla y León', ['Ávila', 'Burgos', 'León', 'Palencia', 'Salamanca', 'Segovia', 'Soria', 'Valladolid', 'Zamora']),
    'Castilla-La Mancha': ('Castilla-La Mancha', ['Albacete', 'Ciudad Real', 'Cuenca', 'Guadalajara', 'Toledo']),
    'Cataluña': ('Cataluña', ['Barcelona', 'Girona', 'Lleida', 'Tarragona']),
    'Comunitat Valenciana': ('la Comunidad Valenciana', ['Alicante', 'Castellón', 'Valencia']),
    'Extremadura': ('Extremadura', ['Badajoz', 'Cáceres']),
    'Galicia': ('Galicia', ['A Coruña', 'Lugo', 'Ourense', 'Pontevedra']),
    'Comunidad de Madrid': ('Madrid', []),
    'Región de Murcia': ('Murcia', []),
    'Comunidad Foral de Navarra': ('Navarra', []),
    'País Vasco': ('el País Vasco', ['Álava', 'Bizkaia', 'Gipuzkoa']),
    'La Rioja': ('La Rioja', []),
    'Ceuta': ('Ceuta', []),
    'Melilla': ('Melilla', []),
}
SLUG = {'Principado de Asturias': 'asturias', 'Illes Balears': 'baleares', 'Comunitat Valenciana': 'comunidad-valenciana',
        'Comunidad de Madrid': 'madrid', 'Región de Murcia': 'murcia', 'Comunidad Foral de Navarra': 'navarra'}
# Lo que la gente busca además del nombre oficial.
ALIAS = {
    'Illes Balears': 'Mallorca, Menorca e Ibiza',
    'Canarias': 'Tenerife, Gran Canaria, Lanzarote y Fuerteventura',
    'Las Palmas': 'Gran Canaria, Lanzarote y Fuerteventura',
    'Santa Cruz de Tenerife': 'Tenerife, La Palma y La Gomera',
    'Málaga': 'la Costa del Sol',
    'Cádiz': 'Sotogrande y la costa gaditana',
    'Alicante': 'la Costa Blanca',
    'Girona': 'la Costa Brava',
}
MES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
DIA = ['lun', 'mar', 'mié', 'jue', 'vie', 'sáb', 'dom']
e = html.escape


def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def ccaa_slug(c):
    return SLUG.get(c) or slug(c)


def load(name, src):
    i = src.index('window.%s=' % name) + len('window.%s=' % name)
    return json.JSONDecoder().raw_decode(src, i)[0]


def d(s):
    return dt.date.fromisoformat(s)


def fday(s):
    x = d(s)
    return '%s %d %s' % (DIA[x.weekday()], x.day, MES[x.month - 1][:3])


def flong(s):
    x = d(s)
    return '%d de %s' % (x.day, MES[x.month - 1])


def eur(p):
    if p is None:
        return ''
    if p == 0:
        return 'Gratis'
    return ('%.2f' % p).rstrip('0').rstrip('.').replace('.', ',') + ' €'


def is_open(t):
    return bool(t.get('op') and t.get('cl') and t['op'] <= ISO <= t['cl'])


def safe_url(u):
    return u if isinstance(u, str) and re.match(r'^https?://', u) else ''


def plural(n, one, many):
    return '%d %s' % (n, one if n == 1 else many)


# ---------------------------------------------------------------- plantilla

CSS_LINK = '<link rel="stylesheet" href="/seo.css">'


def head(title, desc, path, robots='index,follow,max-image-preview:large', ld=()):
    url = BASE + path
    out = ['<!DOCTYPE html>', '<html lang="es">', '<head>', '<meta charset="utf-8">',
           '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">',
           '<title>%s</title>' % e(title),
           '<meta name="description" content="%s">' % e(desc),
           '<link rel="canonical" href="%s">' % url,
           '<meta name="robots" content="%s">' % robots,
           '<meta property="og:type" content="website">', '<meta property="og:site_name" content="Banderín">',
           '<meta property="og:title" content="%s">' % e(title), '<meta property="og:description" content="%s">' % e(desc),
           '<meta property="og:url" content="%s">' % url, '<meta property="og:image" content="%s/og.png?v=2">' % BASE,
           '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">',
           '<meta property="og:locale" content="es_ES">', '<meta name="twitter:card" content="summary_large_image">',
           '<meta name="theme-color" content="#163D2B">',
           '<link rel="icon" href="/icons/icon.svg" type="image/svg+xml">',
           '<link rel="icon" href="/icons/favicon-32.png" sizes="32x32" type="image/png">',
           '<link rel="apple-touch-icon" href="/icons/apple-touch-icon.png">',
           '<link rel="preload" href="/fonts/instrument-serif-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>',
           CSS_LINK]
    for block in ld:
        out.append('<script type="application/ld+json">%s</script>' % json.dumps(block, ensure_ascii=False).replace('</', '<\\/'))
    out.append('</head>')
    return '\n'.join(out)


def topbar():
    return ('<header class="top"><a class="brand" href="/" aria-label="Banderín, inicio">'
            '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3v17" stroke="#F4F1E8" stroke-width="2" stroke-linecap="round"/>'
            '<path d="M8 3.5l10 3.6L8 10.6z" fill="#C9A86A"/></svg><span>banderín</span></a>'
            '<nav aria-label="Principal"><a href="/#lista">Torneos</a><a href="/#calendario">Calendario</a>'
            '<a href="/%s/">Por comunidad</a><a href="/#resultados">Resultados</a></nav></header>' % HUB)


def crumbs(items):
    """items: [(nombre, ruta)]; el último es la página actual."""
    li = []
    for i, (n, p) in enumerate(items):
        li.append('<li>%s</li>' % (e(n) if i == len(items) - 1 else '<a href="%s">%s</a>' % (p, e(n))))
    ld = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': BASE + p} for i, (n, p) in enumerate(items)]}
    return '<nav class="crumbs" aria-label="Estás en"><ol>%s</ol></nav>' % ''.join(li), ld


def footer(regions_html):
    return ('<footer class="foot"><div class="fin">%s'
            '<p class="disc">Banderín reúne los torneos que publican federaciones, clubes y plataformas de inscripción, '
            'y los revisa cada mañana. No organiza torneos ni gestiona inscripciones: confirma siempre fechas y precio '
            'en la web del organizador.</p>'
            '<p class="legal"><a href="/#aviso-legal">Aviso legal</a><a href="/#privacidad">Privacidad</a>'
            '<a href="/#cookies">Cookies</a><a href="/#terminos">Términos de uso</a>'
            '<a href="https://www.instagram.com/banderin.es/" target="_blank" rel="noopener noreferrer">Instagram</a></p>'
            '<a class="byesc" href="https://esclusa.eu" target="_blank" rel="noopener noreferrer">Un proyecto de <b>esclusa</b></a>'
            '</div></footer>' % regions_html)


def regions_nav(counts, current=None):
    a = []
    for c in sorted(CCAA, key=slug):
        n = counts.get(c, 0)
        if not n:
            continue
        name = CCAA[c][0].replace('la Comunidad', 'Comunidad').replace('el País', 'País')
        cls = ' aria-current="page"' if c == current else ''
        a.append('<a href="/%s/%s/"%s>%s <span>%d</span></a>' % (HUB, ccaa_slug(c), cls, e(name), n))
    return '<section class="regions"><h2>Torneos de golf por comunidad</h2><nav>%s</nav></section>' % ''.join(a)


def event_ld(t):
    loc = {'@type': 'Place', 'name': t.get('club') or t.get('campo') or 'Campo de golf',
           'address': {'@type': 'PostalAddress', 'addressLocality': t.get('city') or '', 'addressRegion': t.get('prov') or '',
                       'addressCountry': 'ES'}}
    if t.get('ll'):
        loc['geo'] = {'@type': 'GeoCoordinates', 'latitude': t['ll'][0], 'longitude': t['ll'][1]}
    ev = {'@type': 'SportsEvent', 'name': t['n'], 'startDate': t['s'], 'endDate': t.get('e') or t['s'],
          'eventStatus': 'https://schema.org/EventScheduled',
          'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode',
          'sport': 'Golf', 'location': loc, 'image': [BASE + '/og.png?v=2'],
          'description': ' · '.join(x for x in [t.get('cat'), t.get('mod'), t.get('form'), t.get('club')] if x)}
    u = safe_url(t.get('url'))
    if u:
        ev['url'] = u
    org = t.get('club') if t.get('org') == 'Club' and t.get('club') else None
    if org:
        ev['organizer'] = {'@type': 'Organization', 'name': org}
    if t.get('price') is not None and u:
        off = {'@type': 'Offer', 'price': t['price'], 'priceCurrency': 'EUR', 'url': u}
        if t.get('op'):
            off['validFrom'] = t['op']
        off['availability'] = 'https://schema.org/InStock' if is_open(t) else 'https://schema.org/PreOrder' if t.get('op', '') > ISO else 'https://schema.org/SoldOut' if t.get('cl') and t['cl'] < ISO else 'https://schema.org/InStock'
        ev['offers'] = off
    return ev


def event_li(t):
    u = safe_url(t.get('url'))
    meta = ' · '.join(x for x in [t.get('club'), t.get('city') if t.get('city') and t.get('city') != t.get('club') else None,
                                   t.get('cat'), t.get('mod')] if x)
    when = fday(t['s']) + (' – ' + fday(t['e']) if t.get('e') and t['e'] != t['s'] else '')
    side = []
    if t.get('price') is not None:
        side.append('<span class="price">%s</span>' % e(eur(t['price'])))
    if is_open(t):
        side.append('<span class="open">Inscripción abierta</span>')
    btn = ('<a class="btn" href="%s" target="_blank" rel="noopener">%s</a>' % (e(u), 'Inscribirse' if is_open(t) else 'Ver ficha')) if u else ''
    return ('<li class="ev"><time datetime="%s">%s</time><div class="what"><h3>%s</h3><p>%s</p></div>'
            '<div class="side">%s%s</div></li>' % (t['s'], e(when), e(t['n']), e(meta), ''.join(side), btn))


def month_groups(ts):
    out, cur = [], None
    for t in ts:
        m = t['s'][:7]
        if m != cur:
            if cur:
                out.append('</ol></section>')
            y, mm = m.split('-')
            out.append('<section class="month"><h2>%s de %s</h2><ol class="evs">' % (MES[int(mm) - 1].capitalize(), y))
            cur = m
        out.append(event_li(t))
    if cur:
        out.append('</ol></section>')
    return ''.join(out)


def faq(place):
    qs = [
        ('¿Cómo me inscribo en un torneo de golf en %s?' % place,
         'Cada torneo enlaza a su ficha oficial en la federación, el club o la plataforma de inscripción '
         '(NextCaddy, Golf Directo y otras). La inscripción y el pago se hacen allí; Banderín solo te lleva a la página correcta.'),
        ('¿Qué necesito para jugar un torneo?',
         'Normalmente, licencia federativa en vigor y hándicap. Algunos torneos sociales están abiertos a socios '
         'o tienen límites de hándicap, edad o categoría: lo indica la ficha de cada torneo.'),
        ('¿Cada cuánto se actualiza esta lista?',
         'Cada mañana se revisan las webs de las federaciones, los clubes y las plataformas de inscripción, y se comprueban '
         'los enlaces. Aun así, fechas, plazas y precios pueden cambiar entre una revisión y la siguiente.'),
    ]
    return '<section class="faq"><h2>Preguntas frecuentes</h2>%s</section>' % ''.join(
        '<details><summary>%s</summary><p>%s</p></details>' % (e(q), e(a)) for q, a in qs)


def stats_text(ts, place):
    n = len(ts)
    if not n:
        return ('Ahora mismo no hay torneos de golf publicados en %s para los próximos meses. '
                'Las federaciones y los clubes suelen publicar su calendario por temporadas: vuelve a mirar pronto '
                'o consulta las comunidades cercanas.' % place)
    clubs = len({t.get('club') for t in ts if t.get('club')})
    opn = sum(1 for t in ts if is_open(t))
    wk_end = TODAY + dt.timedelta(days=(6 - TODAY.weekday()))
    this_week = sum(1 for t in ts if d(t['s']) <= wk_end)
    txt = ('Hay %s de golf en %s entre el %s y el %s, en %s. ' %
           (plural(n, 'torneo', 'torneos'), place, flong(max(ts[0]['s'], ISO)), flong(ts[-1]['s']) + (' de %d' % d(ts[-1]['s']).year),
            plural(clubs, 'club', 'clubes')))
    if opn:
        txt += '%s tienen la inscripción abierta ahora mismo. ' % opn if opn > 1 else 'Uno tiene la inscripción abierta ahora mismo. '
    if this_week:
        txt += 'Esta semana se juegan %s. ' % this_week if this_week > 1 else 'Esta semana se juega uno. '
    return txt + 'Cada torneo enlaza a su ficha oficial para inscribirte.'


def top_clubs(ts, k=12):
    c = {}
    for t in ts:
        if t.get('club'):
            c[t['club']] = c.get(t['club'], 0) + 1
    best = sorted(c.items(), key=lambda x: (-x[1], x[0]))[:k]
    if len(best) < 2:
        return ''
    return ('<section class="clubs"><h2>Clubes con más torneos</h2><ul>%s</ul></section>' %
            ''.join('<li><b>%s</b><span>%s</span></li>' % (e(n), plural(v, 'torneo', 'torneos')) for n, v in best))


def cats(ts):
    c = {}
    for t in ts:
        if t.get('cat'):
            c[t['cat']] = c.get(t['cat'], 0) + 1
    if not c:
        return ''
    return '<ul class="chips" aria-label="Tipos de torneo">%s</ul>' % ''.join(
        '<li>%s <b>%d</b></li>' % (e(k), v) for k, v in sorted(c.items(), key=lambda x: -x[1]))


def page(path, title, desc, h1, eyebrow, place, ts, crumb_items, extra_nav, counts, current_ccaa, alias=None, cal=None):
    cr_html, cr_ld = crumbs(crumb_items)
    ld = [{'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': title, 'description': desc,
           'url': BASE + path, 'inLanguage': 'es', 'isPartOf': {'@type': 'WebSite', 'name': 'Banderín', 'url': BASE + '/'},
           'dateModified': ISO,
           'mainEntity': {'@type': 'ItemList', 'numberOfItems': len(ts), 'itemListElement': [
               {'@type': 'ListItem', 'position': i + 1, 'item': event_ld(t)} for i, t in enumerate(ts[:60])]}},
          cr_ld]
    robots = 'index,follow,max-image-preview:large' if ts else 'noindex,follow'
    intro = stats_text(ts, place)
    if alias:
        intro += ' Incluye %s.' % alias
    body = [head(title, desc, path, robots, ld), '<body>', topbar(), '<main>', cr_html,
            '<section class="hero"><p class="eyebrow">%s</p><h1>%s</h1><p class="lede">%s</p>%s'
            '<p class="cta"><a class="btn primary" href="/#lista">Filtrar en el buscador</a>'
            '<a class="btn ghost" href="/#calendario">Ver el calendario</a>%s</p>'
            '<p class="upd">Actualizado el %s.</p></section>' % (e(eyebrow), e(h1), e(intro), cats(ts), cal_link(cal) if ts and cal else '', flong(ISO) + ' de %d' % TODAY.year),
            extra_nav,
            month_groups(ts) if ts else '',
            top_clubs(ts), faq(place), regions_nav(counts, current_ccaa), '</main>', footer(''), '</body></html>']
    out = SITE / path.strip('/') / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text('\n'.join(body), encoding='utf-8')


def cal_link(cal):
    kind, name = cal
    web = 'webcal://%s/cal/%s/%s.ics' % (BASE.split('://', 1)[1], kind, slug(name))
    return '<a class="btn ghost" href="%s" title="Se actualiza solo en tu calendario">Suscribirme al calendario</a>' % e(web)


def subnav(title, links):
    if not links:
        return ''
    return '<nav class="subnav" aria-label="%s"><h2>%s</h2><div>%s</div></nav>' % (e(title), e(title), ''.join(links))


def main():
    src = (SITE / 'data.js').read_text(encoding='utf-8')
    T = [t for t in load('TORNEOS', src) if (t.get('e') or t['s']) >= ISO and t.get('n') and t.get('s')]
    T.sort(key=lambda t: (t['s'], t['n']))
    by_c, by_p = {}, {}
    for t in T:
        by_c.setdefault(t.get('ccaa'), []).append(t)
        by_p.setdefault((t.get('ccaa'), t.get('prov')), []).append(t)
    counts = {c: len(by_c.get(c, [])) for c in CCAA}

    hub_dir = SITE / HUB
    if hub_dir.exists():
        shutil.rmtree(hub_dir)
    pages = []  # (ruta, indexable)

    # Portada de comunidades
    cards = []
    for c in sorted(CCAA, key=lambda x: -counts[x]):
        if not counts[c]:
            continue
        provs = [p for p in CCAA[c][1] if by_p.get((c, p))]
        cards.append('<li><a href="/%s/%s/"><b>%s</b><span>%s</span></a>%s</li>' % (
            HUB, ccaa_slug(c), e(c), plural(counts[c], 'torneo', 'torneos'),
            ('<p>' + ' · '.join('<a href="/%s/%s/%s/">%s</a>' % (HUB, ccaa_slug(c), slug(p), e(p)) for p in provs) + '</p>') if provs else ''))
    cr_html, cr_ld = crumbs([('Inicio', '/'), ('Torneos de golf por comunidad', '/%s/' % HUB)])
    title = 'Torneos de golf por comunidad y provincia | Banderín'
    desc = ('Elige comunidad o provincia y mira todos sus torneos de golf: %d en España, con fechas, precios e inscripción. '
            'Actualizado cada mañana.' % len(T))
    ld = [{'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': title, 'description': desc,
           'url': '%s/%s/' % (BASE, HUB), 'inLanguage': 'es', 'dateModified': ISO}, cr_ld]
    hub = [head(title, desc, '/%s/' % HUB, ld=ld), '<body>', topbar(), '<main>', cr_html,
           '<section class="hero"><p class="eyebrow">Toda España</p><h1>Torneos de golf por comunidad y provincia</h1>'
           '<p class="lede">%s</p><p class="cta"><a class="btn primary" href="/#lista">Abrir el buscador</a></p>'
           '<p class="upd">Actualizado el %s.</p></section>' % (e(stats_text(T, 'España')), flong(ISO) + ' de %d' % TODAY.year),
           '<ul class="cgrid">%s</ul>' % ''.join(cards), faq('España'), '</main>', footer(''), '</body></html>']
    hub_dir.mkdir(parents=True, exist_ok=True)
    (hub_dir / 'index.html').write_text('\n'.join(hub), encoding='utf-8')
    pages.append(('/%s/' % HUB, True))

    for c, (short, provs) in CCAA.items():
        ts = by_c.get(c, [])
        cs = ccaa_slug(c)
        path = '/%s/%s/' % (HUB, cs)
        plinks = ['<a href="/%s/%s/%s/">%s <span>%d</span></a>' % (HUB, cs, slug(p), e(p), len(by_p.get((c, p), [])))
                  for p in provs if by_p.get((c, p))]
        n = len(ts)
        title = 'Torneos de golf en %s · Calendario | Banderín' % short
        desc = ('Calendario de %s de golf en %s: fechas, clubes, precios e inscripción. Revisado cada mañana en federaciones y clubes.'
                % (plural(n, 'torneo', 'torneos'), short)) if n else ('Torneos de golf en %s: calendario de federaciones y clubes, revisado cada mañana.' % short)
        page(path, title, desc, 'Torneos de golf en %s' % short, c, short, ts,
             [('Inicio', '/'), ('Por comunidad', '/%s/' % HUB), (c, path)],
             subnav('Por provincia', plinks), counts, c, ALIAS.get(c), ('ccaa', c))
        pages.append((path, bool(n)))
        for p in provs:
            pts = by_p.get((c, p), [])
            ppath = '%s%s/' % (path, slug(p))
            sib = ['<a href="/%s/%s/%s/"%s>%s <span>%d</span></a>' % (HUB, cs, slug(q), ' aria-current="page"' if q == p else '', e(q),
                                                                     len(by_p.get((c, q), []))) for q in provs if by_p.get((c, q))]
            pn = len(pts)
            title = 'Torneos de golf en %s · Calendario | Banderín' % p
            desc = ('Calendario de %s de golf en %s (%s): fechas, clubes, precios e inscripción, revisado cada mañana.'
                    % (plural(pn, 'torneo', 'torneos'), p, c)) if pn else ('Torneos de golf en %s (%s): calendario de federaciones y clubes, revisado cada mañana.' % (p, c))
            page(ppath, title, desc, 'Torneos de golf en %s' % p, c, p, pts,
                 [('Inicio', '/'), ('Por comunidad', '/%s/' % HUB), (c, path), (p, ppath)],
                 subnav('Otras provincias de %s' % c, sib), counts, c, ALIAS.get(p), ('prov', p))
            pages.append((ppath, bool(pn)))

    # Portada: enlaces rastreables a cada comunidad y descripción con la cifra del día
    idx = SITE / 'index.html'
    s = idx.read_text(encoding='utf-8')
    links = ''.join('<a href="/%s/%s/">%s</a>' % (HUB, ccaa_slug(c), e(c)) for c in sorted(CCAA, key=slug) if counts[c])
    block = ('<!--seo:links--><div class="fregions"><h4>Torneos por comunidad</h4><nav aria-label="Torneos por comunidad">'
             '<a href="/%s/">Todas las comunidades</a>%s</nav></div><!--/seo:links-->' % (HUB, links))
    s = re.sub(r'<!--seo:links-->.*?<!--/seo:links-->', lambda m: block, s, flags=re.S)
    hund = max(100, len(T) // 100 * 100)
    desc = ('Calendario de los torneos de golf de España: más de %d de federaciones y clubes, con fechas, precios '
            'e inscripción. Actualizado cada mañana.' % hund)
    s = re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*(")',
               lambda m: m.group(1) + desc + m.group(2), s)
    idx.write_text(s, encoding='utf-8')

    # Portada en inglés: misma aplicación, servida en /en/
    en = s.replace('<html lang="es">', '<html lang="en">', 1)
    en_desc = ('Every golf tournament in Spain in one calendar: more than %d from federations and clubs, with dates, prices '
               'and entry links. Updated every morning.' % hund)
    en = re.sub(r'(<meta (?:name="description"|property="og:description"|name="twitter:description") content=")[^"]*(")',
                lambda m: m.group(1) + en_desc + m.group(2), en)
    en = en.replace('<title>Calendario de torneos de golf en España | Banderín</title>',
                    '<title>Golf tournament calendar for Spain | Banderín</title>', 1)
    en = en.replace('<link rel="canonical" href="%s/">' % BASE, '<link rel="canonical" href="%s/en/">' % BASE, 1)
    en = en.replace('<meta property="og:url" content="%s/">' % BASE, '<meta property="og:url" content="%s/en/">' % BASE, 1)
    en = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="Every golf tournament in Spain, in one place">', en, count=1)
    en = re.sub(r'<meta name="twitter:title" content="[^"]*">', '<meta name="twitter:title" content="Every golf tournament in Spain, in one place">', en, count=1)
    en = en.replace('<meta property="og:locale" content="es_ES">\n<meta property="og:locale:alternate" content="en_GB">',
                    '<meta property="og:locale" content="en_GB">\n<meta property="og:locale:alternate" content="es_ES">', 1)
    (SITE / 'en').mkdir(exist_ok=True)
    (SITE / 'en' / 'index.html').write_text(en, encoding='utf-8')

    # Mapa del sitio: solo páginas con torneos
    urls = [('/', '1.0'), ('/en/', '0.6')] + [(p, '0.8' if p.count('/') <= 3 else '0.7') for p, ok in pages if ok]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p, pr in urls:
        sm.append('  <url><loc>%s%s</loc><lastmod>%s</lastmod><changefreq>daily</changefreq><priority>%s</priority></url>' % (BASE, p, ISO, pr))
    sm.append('</urlset>')
    (SITE / 'sitemap.xml').write_text('\n'.join(sm) + '\n', encoding='utf-8')
    print('seo: %d torneos, %d páginas (%d en el mapa del sitio)' % (len(T), len(pages), len(urls)))


if __name__ == '__main__':
    main()
