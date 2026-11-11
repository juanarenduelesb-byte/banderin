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

TZ = ZoneInfo('Europe/Madrid')
TODAY = dt.datetime.now(TZ).date()
ISO, TOMORROW = TODAY.isoformat(), (TODAY + dt.timedelta(days=1)).isoformat()
MAX_ITEMS = 30
# Qué avisos recibe quien sigue un club o una provincia (quien sigue un torneo concreto los recibe todos).
FOR_PLACES = {'nuevo', 'abre', 'cancelado', 'fecha'}


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
        if prev_urls is not None and t['url'] not in prev_urls:
            ev.append({'t': t, 'tipo': 'nuevo'})
    for c in load(new_path, 'CAMBIOS') or []:
        if c.get('d') != ISO or c.get('k') not in ('fecha', 'cancelado', 'plazo'):
            continue
        t = by_url.get(c.get('url')) or {'url': c.get('url'), 'n': c.get('n'), 'club': c.get('club'), 's': c.get('s')}
        if t.get('url'):
            ev.append({'t': t, 'tipo': c['k'], 'nuevo_valor': c.get('b')})
    for x in ev:
        x['clave'] = x['t']['url'] + '|' + x['tipo'] + ('|' + x['nuevo_valor'] if x.get('nuevo_valor') else '')
    return ev


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


def compose(sub, items, site):
    lang = sub['idioma'] if sub['idioma'] in ('es', 'en') else 'es'
    e = html.escape
    tok = manage_token(sub['id'])
    manage = site + ('/en/' if lang == 'en' else '/') + '#perfil?avisos=' + tok
    unsub = site + '/api/avisos/baja?t=' + tok
    n = len(items)
    if n == 1:
        subject = label(items[0], lang) + ' · ' + items[0]['t']['n']
    else:
        subject = ('%d updates on what you follow' if lang == 'en' else '%d novedades de lo que sigues') % n
    rows, text = [], []
    for x in items[:MAX_ITEMS]:
        t = x['t']
        where = ' · '.join(v for v in [t.get('club'), t.get('city')] if v)
        cancelled = x['tipo'] == 'cancelado'
        rows.append(
            '<tr><td style="padding:14px 0;border-top:1px solid #E4DDCB">'
            '<p style="margin:0 0 4px;font-size:12px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:%s">%s</p>'
            '<p style="margin:0 0 3px;font-size:16px;font-weight:600;color:#13201A">%s</p>'
            '<p style="margin:0 0 10px;font-size:14px;color:#55645B">%s%s</p>'
            '<a href="%s" style="font-size:14px;font-weight:600;color:#1C4734">%s</a></td></tr>' % (
                '#B83232' if cancelled else '#1E6B43', e(label(x, lang)), e(t['n']), e(fdate(t['s'], lang)),
                (' · ' + e(where)) if where else '', e(t['url']), 'Open the official page' if lang == 'en' else 'Ver la ficha oficial'))
        text.append('- %s: %s (%s%s)\n  %s' % (label(x, lang), t['n'], fdate(t['s'], lang), (' · ' + where) if where else '', t['url']))
    more = n - MAX_ITEMS
    title = 'News on what you follow' if lang == 'en' else 'Novedades de lo que sigues'
    foot = ('You get this because you follow these tournaments, clubs or provinces on Banderín. At most one email a day.'
            if lang == 'en' else 'Recibes esto porque sigues estos torneos, clubes o provincias en Banderín. Como mucho, un correo al día.')
    links = ('<a href="%s" style="color:#1C4734">%s</a> · <a href="%s" style="color:#1C4734">%s</a>' % (
        e(manage), 'Manage alerts' if lang == 'en' else 'Gestionar avisos', e(unsub), 'Unsubscribe' if lang == 'en' else 'Darme de baja'))
    body = ('<!DOCTYPE html><html><body style="margin:0;background:#0E2A1E;padding:24px 12px;font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif">'
            '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0"><tr><td align="center">'
            '<table role="presentation" width="100%%" style="max-width:560px;background:#FAF7EE;border-radius:20px" cellpadding="0" cellspacing="0"><tr><td style="padding:28px">'
            '<p style="margin:0 0 18px;font-weight:700;font-size:18px;color:#13201A">⛳ banderín</p>'
            '<h1 style="margin:0 0 6px;font-family:Georgia,serif;font-weight:400;font-size:28px;color:#13201A">%s</h1>'
            '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0">%s</table>%s'
            '<p style="margin:18px 0 0;font-size:13px;line-height:1.5;color:#6B776F">%s<br>%s</p>'
            '<p style="margin:10px 0 0;font-size:12px;color:#6B776F">%s</p>'
            '</td></tr></table></td></tr></table></body></html>') % (
        e(title), ''.join(rows),
        ('<p style="margin:12px 0 0;font-size:14px"><a href="%s" style="color:#1C4734">%s</a></p>' % (
            e(manage), ('And %d more' if lang == 'en' else 'Y %d más') % more)) if more > 0 else '',
        e(foot), links,
        'Confirm dates and conditions on the organiser\'s page.' if lang == 'en' else 'Confirma fechas y condiciones en la web del organizador.')
    txt = title + '\n\n' + '\n'.join(text) + '\n\n' + foot + '\n' + manage + '\n' + unsub
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
    if len(sys.argv) < 3:
        sys.exit('uso: avisos.py <data.js nuevo> <data.js anterior>')
    site = os.environ.get('SITE_URL', 'https://banderin.pages.dev').rstrip('/')
    ev = events(sys.argv[1], sys.argv[2])
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
    if not ev:
        print('avisos: ninguna novedad hoy')
        return
    subs = db.q("SELECT id, email, idioma, ultimo_aviso FROM suscriptores WHERE estado = 'activo'")
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
        items, seen = [], set()
        for x in ev:
            t = x['t']
            match = ('torneo', t['url']) in f or (x['tipo'] in FOR_PLACES and (('club', t.get('club')) in f or ('prov', t.get('prov')) in f))
            if match and (s['id'], x['clave']) not in sent and x['clave'] not in seen:
                items.append(x)
                seen.add(x['clave'])
        if not items:
            continue
        items.sort(key=lambda x: (x['tipo'] != 'cancelado', x['t'].get('s', '')))
        try:
            send(s, *compose(s, items, site))
        except Exception as ex:  # un fallo con una persona no para el resto
            errores += 1
            print('avisos: error enviando a un suscriptor:', ex)
            continue
        stamp = now.isoformat().replace('+00:00', 'Z')
        db.q('UPDATE suscriptores SET ultimo_aviso = ? WHERE id = ?', (stamp, s['id']))
        for x in items:
            db.q('INSERT OR IGNORE INTO enviados (suscriptor, clave, fecha) VALUES (?, ?, ?)', (s['id'], x['clave'], ISO))
        enviados += 1
    print('avisos: %d novedades, %d suscriptores activos, %d correos enviados, %d errores' % (len(ev), len(subs), enviados, errores))
    if errores and not enviados:
        sys.exit(1)


if __name__ == '__main__':
    main()
