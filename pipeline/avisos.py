#!/usr/bin/env python3
"""Banderín · envío diario de avisos por correo.

Compara los torneos de hoy con los de la publicación anterior, busca qué le
interesa a cada suscriptor (torneos, clubes y provincias que sigue) y le envía
UN correo como máximo al día con todas sus novedades.

  python3 pipeline/avisos.py <data.js nuevo> <data.js anterior>

Variables de entorno (en GitHub: secretos del repositorio):
  AVISOS=on            sin esto no hace nada
  BREVO_API_KEY        clave de la API de Brevo
  AVISOS_FROM          remitente, p. ej. avisos@banderin.es
  LINK_SECRET          el mismo secreto que usa la API de la web (lib/avisos.js)
  SITE_URL             dirección pública de la web
  Base de datos: CF_API_TOKEN + CF_ACCOUNT_ID + D1_DATABASE_ID (Cloudflare D1),
                 o D1_SQLITE=<ruta> para pruebas en local.
"""
import base64
import datetime as dt
import hashlib
import hmac
import html
import json
import os
import sqlite3
import sys
import urllib.request
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import correo  # noqa: E402  plantilla de los correos

TZ = ZoneInfo('Europe/Madrid')
TODAY = dt.date.fromisoformat(os.environ['AVISOS_HOY']) if os.environ.get('AVISOS_HOY') else dt.datetime.now(TZ).date()  # AVISOS_HOY: solo para pruebas
ISO, TOMORROW = TODAY.isoformat(), (TODAY + dt.timedelta(days=1)).isoformat()
MAX_ITEMS = 30
# Qué avisos recibe quien sigue un club o una provincia (quien sigue un torneo concreto los recibe todos).
FOR_PLACES = {'nuevo', 'abre', 'cierra', 'cancelado', 'fecha', 'plazo'}


def load(path, name):
    if not path or not os.path.exists(path):
        return None
    src = open(path, encoding='utf-8').read()
    i = src.find('window.%s=' % name)
    if i < 0:
        return None
    return json.JSONDecoder().raw_decode(src, i + len('window.%s=' % name))[0]


def events(new_path, prev_path):
    T = [t for t in load(new_path, 'TORNEOS') or [] if (t.get('e') or t['s']) >= ISO]
    prev = load(prev_path, 'TORNEOS')
    prev_urls = {t['url'] for t in prev} if prev else None
    by_url = {t['url']: t for t in T}
    ev = []
    for t in T:
        if t.get('op') in (ISO, TOMORROW):
            ev.append({'t': t, 'tipo': 'abre', 'cuando': 'hoy' if t['op'] == ISO else 'mañana'})
        if t.get('cl') in (ISO, TOMORROW) and (not t.get('op') or t['op'] <= ISO):
            ev.append({'t': t, 'tipo': 'cierra', 'cuando': 'hoy' if t['cl'] == ISO else 'mañana'})
        if prev_urls is not None and t['url'] not in prev_urls and t['s'] > ISO:  # avisar de uno que ya empezó no sirve
            ev.append({'t': t, 'tipo': 'nuevo'})
    for c in load(new_path, 'CAMBIOS') or []:
        if c.get('d') != ISO or c.get('k') not in ('fecha', 'cancelado', 'plazo'):
            continue
        t = by_url.get(c.get('url')) or {'url': c.get('url'), 'n': c.get('n'), 'club': c.get('club'), 's': c.get('s')}
        if t.get('url'):
            ev.append({'t': t, 'tipo': c['k'], 'nuevo_valor': c.get('b')})
    for x in ev:
        x['clave'] = x['t']['url'] + '|' + x['tipo'] + ('|' + x['nuevo_valor'] if x.get('nuevo_valor') else '')
    return ev, T, prev_urls



WD = TODAY.weekday()
SAT = TODAY + dt.timedelta(days=(5 - WD) if WD <= 5 else 0)
SUN = SAT + dt.timedelta(days=1) if WD <= 5 else TODAY
WEEK = '%d-%02d' % TODAY.isocalendar()[:2]
JUEVES = WD == 3


def zone_of(follows, T):
    """Comunidades de lo que sigue la persona."""
    prov_cc, club_cc, url_cc = {}, {}, {}
    for t in T:
        if t.get('ccaa'):
            prov_cc.setdefault(t.get('prov'), t['ccaa'])
            club_cc.setdefault(t.get('club'), t['ccaa'])
            url_cc[t['url']] = t['ccaa']
    z = set()
    for tipo, k in follows:
        c = {'prov': prov_cc, 'club': club_cc, 'torneo': url_cc}[tipo].get(k)
        if c:
            z.add(c)
    return z


def encaja(t, p):
    """Misma lógica que «No encaja» en la web (app.js, fit): solo excluye lo que no cumple con claridad."""
    if not p:
        return True
    c = t.get('cond') or {}
    if p.get('sexo') == 'F' and t.get('sex') == 'Masculino':
        return False
    if p.get('sexo') == 'M' and t.get('sex') == 'Femenino':
        return False
    if p.get('nac'):
        age = int((t.get('s') or ISO)[:4]) - int(p['nac'])
        if c.get('edadMax') is not None:
            if age > c['edadMax']:
                return False
        elif t.get('cat') == 'Juvenil' and age > 21:
            return False
        if c.get('edadMin') is not None:
            if age < c['edadMin']:
                return False
        elif t.get('cat') == 'Senior' and age < 50:
            return False
    if c.get('hcp') is not None and p.get('hcp') is not None and p['hcp'] > c['hcp']:
        return False
    if c.get('priv') and t.get('club') not in (p.get('clubs') or []):
        return False
    if c.get('fed') and p.get('fed') and p['fed'] != c['fed']:
        return False
    return True


def extras(sid, follows, T, prev_urls, taken, sent, lang, perfil=None):
    """Bloques secundarios: fin de semana, cierres próximos y nuevos en su comunidad."""
    zone = zone_of(follows, T)
    if not zone:
        return [], zone
    fprov = {k for tipo, k in follows if tipo == 'prov'}
    fclub = {k for tipo, k in follows if tipo == 'club'}
    pool = [t for t in T if t.get('ccaa') in zone and t['url'] not in taken and encaja(t, perfil)]
    is_open = lambda t: (not t.get('op') or t['op'] <= ISO) and (not t.get('cl') or t['cl'] >= ISO)
    used, out = set(), []
    def pick(cands, n, key):
        res = []
        for t in cands:
            k = t['url'] + '|' + key + '|' + WEEK
            if t['url'] in used or (sid, k) in sent:
                continue
            res.append((t, k))
            used.add(t['url'])
            if len(res) >= n:
                break
        return res
    pref = lambda t: (t.get('prov') not in fprov and t.get('club') not in fclub, not is_open(t), t['s'])
    finde = sorted([t for t in pool if t['s'] <= SUN.isoformat() and (t.get('e') or t['s']) >= SAT.isoformat()], key=pref)
    pronto = sorted([t for t in pool if t.get('cl') and (TODAY + dt.timedelta(days=2)).isoformat() <= t['cl'] <= (TODAY + dt.timedelta(days=7)).isoformat()
                     and is_open(t)], key=lambda t: (t['cl'], pref(t)))
    nuevos = sorted([t for t in pool if prev_urls is not None and t['url'] not in prev_urls and t['s'] > ISO], key=pref)
    en = lang == 'en'
    for tipo, cands, n, lab in (
            ('finde', finde, 5, lambda t: 'This weekend' if en else 'Este fin de semana'),
            ('pronto', pronto, 3, lambda t: ('Entries close ' if en else 'Cierra la inscripción el ') + fdate(t['cl'], lang)),
            ('nuevo', nuevos, 3, lambda t: 'New tournament' if en else 'Torneo nuevo')):
        for t, k in pick(cands, n, tipo):
            out.append({'t': t, 'tipo': tipo, 'label': lab(t), 'clave': k})
    return out, zone


# ------------------------------------------------------------------ base de datos

class D1:
    def __init__(self):
        if os.environ.get('D1_SQLITE'):
            self.db = sqlite3.connect(os.environ['D1_SQLITE'])
            self.db.row_factory = sqlite3.Row
        else:
            self.db = None
            self.url = 'https://api.cloudflare.com/client/v4/accounts/%s/d1/database/%s/query' % (
                os.environ['CF_ACCOUNT_ID'], os.environ['D1_DATABASE_ID'])

    def q(self, sql, params=()):
        if self.db:
            cur = self.db.execute(sql, params)
            rows = [dict(r) for r in cur.fetchall()]
            self.db.commit()
            return rows
        req = urllib.request.Request(self.url, method='POST', data=json.dumps({'sql': sql, 'params': list(params)}).encode(),
                                     headers={'Authorization': 'Bearer ' + os.environ['CF_API_TOKEN'], 'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.load(r)
        if not data.get('success'):
            raise RuntimeError('D1: %s' % data.get('errors'))
        return data['result'][0].get('results') or []


# ------------------------------------------------------------------ correo

def manage_token(sid):
    sig = hmac.new(os.environ['LINK_SECRET'].encode(), ('gestion|' + sid).encode(), hashlib.sha256).digest()
    return sid + '.' + base64.urlsafe_b64encode(sig).decode().rstrip('=')[:32]


MES = {'es': ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic'],
       'en': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']}


def fdate(s, lang):
    d = dt.date.fromisoformat(s)
    return ('%d %s' % (d.day, MES[lang][d.month - 1])) if lang == 'es' else ('%s %d' % (MES[lang][d.month - 1], d.day))


def label(x, lang):
    t, w = x['tipo'], x.get('cuando')
    if lang == 'en':
        w = {'hoy': 'today', 'mañana': 'tomorrow'}.get(w, w)
        return {'abre': 'Entries open ' + str(w), 'cierra': 'Entries close ' + str(w), 'nuevo': 'New tournament',
                'cancelado': 'Cancelled', 'fecha': 'New date: ' + fdate(x.get('nuevo_valor') or x['t']['s'], lang),
                'plazo': 'New entry deadline: ' + fdate(x.get('nuevo_valor') or ISO, lang)}[t]
    return {'abre': 'Abre la inscripción ' + str(w), 'cierra': 'Cierra la inscripción ' + str(w), 'nuevo': 'Torneo nuevo',
            'cancelado': 'Cancelado', 'fecha': 'Cambia de fecha: ahora el ' + fdate(x.get('nuevo_valor') or x['t']['s'], lang),
            'plazo': 'Nuevo plazo de inscripción: hasta el ' + fdate(x.get('nuevo_valor') or ISO, lang)}[t]


def compose(sub, items, site, extra=(), zone=()):
    lang = sub['idioma'] if sub['idioma'] in ('es', 'en') else 'es'
    tok = manage_token(sub['id'])
    manage = site + ('/en/' if lang == 'en' else '/') + '#perfil?avisos=' + tok
    unsub = site + '/api/avisos/baja?t=' + tok
    n = len(items)
    if n == 0:
        zname = next(iter(zone)) if len(zone) == 1 else ('your area' if lang == 'en' else 'tu zona')
        subject = ('Your golf weekend in %s' if lang == 'en' else 'Tu fin de semana de golf en %s') % zname
        title = 'Your golf weekend' if lang == 'en' else 'Tu fin de semana de golf'
    elif n == 1:
        subject = label(items[0], lang) + ' · ' + items[0]['t']['n']
        title = label(items[0], lang)
    else:
        subject = ('%d updates on what you follow' if lang == 'en' else '%d novedades de lo que sigues') % n
        title = 'News on what you follow' if lang == 'en' else 'Novedades de lo que sigues'
    zl = ', '.join(sorted(zone))
    if n == 0:
        lede = ('What is on in %s this weekend, and what is worth not missing.' if lang == 'en'
                else 'Lo que se juega en %s este fin de semana y lo que no conviene perderse.') % zl
    elif lang == 'en':
        lede = 'Today there %s %d %s on the tournaments, clubs and provinces you follow.' % (
            'is' if n == 1 else 'are', n, 'update' if n == 1 else 'updates')
    else:
        lede = 'Hoy hay %d %s en los torneos, clubes y provincias que sigues.' % (n, 'novedad' if n == 1 else 'novedades')
    cards, text = [], []
    # Agrupados por urgencia: primero lo que cierra, luego lo que abre, lo nuevo y los cambios.
    GRUPOS = [('cierra', ('Closing soon', "Don't miss it") if lang == 'en' else ('Cierra la inscripción', 'Que no se te escape')),
              ('abre', ('Entries opening', 'Get ready to enter') if lang == 'en' else ('Abre la inscripción', 'Prepárate para apuntarte')),
              ('nuevo', ('Just published', 'New tournaments') if lang == 'en' else ('Recién publicados', 'Torneos nuevos')),
              ('cambio', ('Changes', 'Dates, deadlines and cancellations') if lang == 'en' else ('Cambios', 'Fechas, plazos y cancelaciones'))]
    grupo = lambda x: x['tipo'] if x['tipo'] in ('cierra', 'abre', 'nuevo') else 'cambio'
    shown = sorted(items[:MAX_ITEMS], key=lambda x: [g for g, _ in GRUPOS].index(grupo(x)))
    tipos = [g for g, _ in GRUPOS if any(grupo(x) == g for x in shown)]
    if n > 1:
        nombres = {'cierra': ('closing', 'cierran'), 'abre': ('opening', 'abren'), 'nuevo': ('new', 'nuevos'), 'cambio': ('changes', 'cambios')}
        cards.append(correo.chips([(sum(1 for x in items if grupo(x) == g), nombres[g][0 if lang == 'en' else 1],
                                    {'cambio': 'fecha'}.get(g, g)) for g in tipos]))
    for g, (eyebrow, stitle) in GRUPOS:
        grp = [x for x in shown if grupo(x) == g]
        if not grp:
            continue
        if len(tipos) > 1:
            cards.append(correo.section(eyebrow, stitle))
        for x in grp:
            t = x['t']
            enter = x['tipo'] in ('abre', 'cierra')
            btn = ('Enter' if enter else 'View page') if lang == 'en' else ('Inscribirme' if enter else 'Ver ficha')
            cards.append(correo.item(lang, x['tipo'], label(x, lang), t, t['url'], btn))
            where = ' · '.join(v for v in [t.get('club'), t.get('city')] if v)
            text.append('- %s: %s (%s%s)\n  %s' % (label(x, lang), t['n'], fdate(t['s'], lang), (' · ' + where) if where else '', t['url']))
    more = n - MAX_ITEMS
    if more > 0:
        cards.append(correo.para('<a href="%s" style="color:%s">%s</a>' % (
            correo.e(manage), correo.GREEN, ('And %d more' if lang == 'en' else 'Y %d más') % more), 14.5, margin='14px 0 0'))
    if extra:
        zname = (next(iter(zone)) if len(zone) == 1 else ('your regions' if lang == 'en' else 'tus comunidades'))
        if n:  # en el resumen del jueves todo es «tu zona»: sin cabecera extra
            cards.append(correo.section('Also near you' if lang == 'en' else 'También en tu zona',
                                        ('More golf in %s' if lang == 'en' else 'Más golf en %s') % zname))
        for x in extra:
            t = x['t']
            cards.append(correo.item(lang, x['tipo'], x['label'], t, t['url'], 'View page' if lang == 'en' else 'Ver ficha'))
            text.append('- %s: %s (%s) %s' % (x['label'], t['n'], fdate(t['s'], lang), t['url']))
    cards.append(correo.cta(site + ('/en/' if lang == 'en' else '/') + '#lista',
                            'See every tournament' if lang == 'en' else 'Ver todos los torneos'))
    why = ('You get this email because you turned on Banderín alerts. At most one a day.' if lang == 'en'
           else 'Recibes este correo porque activaste los avisos de Banderín. Como mucho, uno al día.')
    preheader = ' · '.join(x['t']['n'] for x in (list(items) + list(extra))[:3])
    body = correo.shell(lang, subject, preheader, 'Alerts' if lang == 'en' else 'Avisos',
                        correo.h1(title) + correo.para(correo.e(lede), margin='0 0 10px') + ''.join(cards),
                        correo.footer(lang, manage, unsub, why), site)
    txt = title + '\n\n' + lede + '\n\n' + '\n'.join(text) + '\n\n' + why + '\n' + manage + '\n' + unsub
    return subject, body, txt, unsub


def send(sub, subject, body, txt, unsub):
    payload = {'sender': {'name': 'Banderín', 'email': os.environ['AVISOS_FROM']}, 'to': [{'email': sub['email']}],
               'subject': subject, 'htmlContent': body, 'textContent': txt,
               'headers': {'List-Unsubscribe': '<%s>' % unsub, 'List-Unsubscribe-Post': 'List-Unsubscribe=One-Click'}}
    req = urllib.request.Request(os.environ.get('BREVO_API_URL', 'https://api.brevo.com') + '/v3/smtp/email', method='POST',
                                 data=json.dumps(payload).encode(),
                                 headers={'api-key': os.environ['BREVO_API_KEY'], 'Content-Type': 'application/json', 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as r:
        if r.status >= 300:
            raise RuntimeError('Brevo %s' % r.status)


# ------------------------------------------------------------------ principal

def main():
    if os.environ.get('AVISOS') != 'on':
        print('avisos: apagados (AVISOS no es "on")')
        return
    if sys.argv[1:2] == ['--desde']:
        # Desde cuándo hay que comparar: el último correo más antiguo entre quienes aún no lo han recibido hoy
        # (como mucho 7 días). Así, lo que cambió en una pasada posterior al correo de ese día no se pierde;
        # lo ya enviado no se repite porque cada aviso queda registrado en «enviados».
        hoy0 = dt.datetime.combine(TODAY, dt.time(), TZ).astimezone(dt.timezone.utc)
        r = D1().q("SELECT MIN(ultimo_aviso) AS d FROM suscriptores WHERE estado = 'activo' AND ultimo_aviso IS NOT NULL AND ultimo_aviso < ?",
                   (hoy0.isoformat(),))
        d = r[0]['d'] if r else None
        if d:
            d = max(dt.datetime.fromisoformat(d.replace('Z', '+00:00')), hoy0 - dt.timedelta(days=7))
            print(d.strftime('%Y-%m-%dT%H:%M:%SZ'))
        return
    if len(sys.argv) < 3:
        sys.exit('uso: avisos.py <data.js nuevo> <data.js anterior>')
    site = (os.environ.get('SITE_URL') or 'https://banderin.es').rstrip('/')
    if 'pages.dev' in site:  # la dirección antigua redirige, y una redirección rompe la baja en un clic
        site = 'https://banderin.es'
    ev, T, prev_urls = events(sys.argv[1], sys.argv[2])
    db = D1()
    now = dt.datetime.now(dt.timezone.utc)
    # Limpieza: altas sin confirmar (7 días), cuentas inactivas (24 meses) y registro de enviados (120 días).
    db.q("DELETE FROM seguimientos WHERE suscriptor IN (SELECT id FROM suscriptores WHERE estado = 'pendiente' AND creado < ?)",
         ((now - dt.timedelta(days=7)).isoformat(),))
    db.q("DELETE FROM suscriptores WHERE estado = 'pendiente' AND creado < ?", ((now - dt.timedelta(days=7)).isoformat(),))
    old = (now - dt.timedelta(days=730)).isoformat()
    db.q("DELETE FROM seguimientos WHERE suscriptor IN (SELECT id FROM suscriptores WHERE ultima_actividad < ?)", (old,))
    db.q("DELETE FROM enviados WHERE suscriptor IN (SELECT id FROM suscriptores WHERE ultima_actividad < ?)", (old,))
    db.q("DELETE FROM suscriptores WHERE ultima_actividad < ?", (old,))
    db.q("DELETE FROM enviados WHERE fecha < ?", ((TODAY - dt.timedelta(days=120)).isoformat(),))
    if not ev and not JUEVES:
        print('avisos: ninguna novedad hoy')
        return
    subs = db.q("SELECT id, email, idioma, ultimo_aviso, perfil FROM suscriptores WHERE estado = 'activo'")
    sigo = {}
    for r in db.q('SELECT suscriptor, tipo, clave FROM seguimientos'):
        sigo.setdefault(r['suscriptor'], set()).add((r['tipo'], r['clave']))
    sent = {(r['suscriptor'], r['clave']) for r in db.q('SELECT suscriptor, clave FROM enviados')}
    enviados = errores = 0
    for s in subs:
        last = s.get('ultimo_aviso')
        if last and dt.datetime.fromisoformat(last.replace('Z', '+00:00')).astimezone(TZ).date() == TODAY:
            continue  # como mucho un correo al día
        f = sigo.get(s['id'], set())
        if not f:
            continue
        try:
            perfil = json.loads(s.get('perfil') or 'null')
        except ValueError:
            perfil = None
        items, seen = [], set()
        for x in ev:
            t = x['t']
            own = ('torneo', t['url']) in f  # un torneo que sigue a mano: todos los avisos, encaje o no
            place = x['tipo'] in FOR_PLACES and (('club', t.get('club')) in f or ('prov', t.get('prov')) in f)
            match = own or (place and encaja(t, perfil))
            if match and (s['id'], x['clave']) not in sent and x['clave'] not in seen:
                items.append(x)
                seen.add(x['clave'])
        items.sort(key=lambda x: (x['tipo'] != 'cancelado', x['t'].get('s', '')))
        lang = s['idioma'] if s['idioma'] in ('es', 'en') else 'es'
        weekly_key = 'semanal|' + WEEK
        weekly = JUEVES and (s['id'], weekly_key) not in sent
        if not items and not weekly:
            continue
        extra, zone = extras(s['id'], f, T, prev_urls, {x['t']['url'] for x in items}, sent, lang, perfil)
        if not items and not extra:
            continue
        try:
            send(s, *compose(s, items, site, extra, zone))
        except Exception as ex:  # un fallo con una persona no para el resto
            errores += 1
            print('avisos: error enviando a un suscriptor:', ex)
            continue
        stamp = now.isoformat().replace('+00:00', 'Z')
        db.q('UPDATE suscriptores SET ultimo_aviso = ? WHERE id = ?', (stamp, s['id']))
        for x in list(items) + list(extra):
            db.q('INSERT OR IGNORE INTO enviados (suscriptor, clave, fecha) VALUES (?, ?, ?)', (s['id'], x['clave'], ISO))
        if weekly:
            db.q('INSERT OR IGNORE INTO enviados (suscriptor, clave, fecha) VALUES (?, ?, ?)', (s['id'], weekly_key, ISO))
        enviados += 1
    print('avisos: %d novedades, %d suscriptores activos, %d correos enviados, %d errores' % (len(ev), len(subs), enviados, errores))
    if errores and not enviados:
        sys.exit(1)


if __name__ == '__main__':
    main()
