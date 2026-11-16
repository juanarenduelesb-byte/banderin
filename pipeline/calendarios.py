#!/usr/bin/env python3
"""Banderín - calendarios suscribibles (.ics).

Genera, a partir de site/data.js, un calendario por provincia, por comunidad y
por club con los torneos próximos:

  site/cal/prov/<provincia>.ics
  site/cal/ccaa/<comunidad>.ics
  site/cal/club/<club>.ics

Quien se suscribe (Apple, Google, Outlook) ve los torneos en su calendario y se
actualizan solos. Se ejecuta cada día después de pipeline/seo.py:

  python3 pipeline/calendarios.py
"""
import datetime as dt
import hashlib
import shutil
from pathlib import Path

import seo  # reutiliza la carga de datos, los nombres y los slugs de las páginas

SITE = seo.SITE
HOST = seo.BASE.split('://', 1)[1]
STAMP = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')


def esc(s):
    return str(s).replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,').replace('\n', '\\n')


def fold(line):
    """Corta las líneas a 75 octetos, como pide el estándar iCalendar."""
    b = line.encode('utf-8')
    if len(b) <= 75:
        return line
    out, cur = [], b''
    for ch in line:
        c = ch.encode('utf-8')
        if len(cur) + len(c) > (75 if not out else 74):
            out.append(cur.decode('utf-8'))
            cur = b''
        cur += c
    out.append(cur.decode('utf-8'))
    return '\r\n '.join(out)


def day(s):
    return s.replace('-', '')


def event(t):
    end = (dt.date.fromisoformat(t.get('e') or t['s']) + dt.timedelta(days=1)).isoformat()
    url = seo.safe_url(t.get('url'))
    desc = [' - '.join(x for x in [t.get('cat'), t.get('mod'), t.get('form')] if x and x != 'Sin indicar')]
    if t.get('op') or t.get('cl'):
        desc.append('Inscripción: ' + ', '.join(x for x in [
            ('abre el ' + seo.flong(t['op'])) if t.get('op') else '',
            ('cierra el ' + seo.flong(t['cl'])) if t.get('cl') else ''] if x) + '.')
    if t.get('price') is not None:
        desc.append('Precio: ' + seo.eur(t['price']) + '.')
    if url:
        desc.append('Ficha oficial: ' + url)
    desc.append('Confirma fechas y condiciones en la web del organizador. Vía Banderín.')
    lines = ['BEGIN:VEVENT',
             'UID:' + hashlib.sha1((url or t['n'] + t['s']).encode()).hexdigest()[:20] + '@' + HOST,
             'DTSTAMP:' + STAMP,
             'DTSTART;VALUE=DATE:' + day(t['s']),
             'DTEND;VALUE=DATE:' + day(end),
             'SUMMARY:' + esc(t['n']),
             'LOCATION:' + esc(', '.join(x for x in [t.get('club'), t.get('city'), t.get('prov')] if x and x != 'Por confirmar')),
             'DESCRIPTION:' + esc('\n'.join(x for x in desc if x)),
             'TRANSP:TRANSPARENT',
             'STATUS:' + ('CANCELLED' if t.get('aviso') and 'cancel' in t['aviso'].lower() else 'CONFIRMED')]
    if url:
        lines.append('URL:' + url)
    lines.append('END:VEVENT')
    return lines


def write(kind, name, ts, title):
    lines = ['BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Banderin//Torneos de golf//ES', 'CALSCALE:GREGORIAN',
             'METHOD:PUBLISH', 'X-WR-CALNAME:' + esc('Banderín - ' + title),
             'X-WR-CALDESC:' + esc('Torneos de golf: %s. Se actualiza cada mañana. %s' % (title, seo.BASE)),
             'X-WR-TIMEZONE:Europe/Madrid', 'REFRESH-INTERVAL;VALUE=DURATION:PT12H', 'X-PUBLISHED-TTL:PT12H']
    for t in ts:
        lines += event(t)
    lines.append('END:VCALENDAR')
    out = SITE / 'cal' / kind / (seo.slug(name) + '.ics')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(('\r\n'.join(fold(x) for x in lines) + '\r\n').encode('utf-8'))


def main():
    src = (SITE / 'data.js').read_text(encoding='utf-8')
    T = [t for t in seo.load('TORNEOS', src) if (t.get('e') or t['s']) >= seo.ISO and t.get('n') and t.get('s')]
    T.sort(key=lambda t: (t['s'], t['n']))
    if (SITE / 'cal').exists():
        shutil.rmtree(SITE / 'cal')
    groups = {'prov': {}, 'ccaa': {}, 'club': {}}
    for t in T:
        if t.get('prov') and t['prov'] != 'Por confirmar':
            groups['prov'].setdefault(t['prov'], []).append(t)
        if t.get('ccaa'):
            groups['ccaa'].setdefault(t['ccaa'], []).append(t)
        if t.get('club'):
            groups['club'].setdefault(t['club'], []).append(t)
    n = 0
    for kind, g in groups.items():
        for name, ts in g.items():
            write(kind, name, ts, name)
            n += 1
    print('calendarios: %d archivos (%d provincias, %d comunidades, %d clubes)' % (
        n, len(groups['prov']), len(groups['ccaa']), len(groups['club'])))


if __name__ == '__main__':
    main()
