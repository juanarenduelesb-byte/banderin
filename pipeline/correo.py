"""Banderín · plantilla de los correos (mismo diseño que la web).

El resumen diario de avisos se construye aquí. Los correos de la web
(confirmación y «ya estabas suscrito») usan la misma plantilla, copiada en
lib/avisos.js: si cambias el diseño, cámbialo en los dos sitios.

Pensado para clientes de correo: tablas, estilos en línea, sin JavaScript ni
fuentes externas (Georgia hace de Libre Caslon), y legible con las imágenes
bloqueadas.
"""
import datetime as dt
import html

SITE = 'https://banderin.es'
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
SERIF = "'Libre Caslon Display',Georgia,'Times New Roman',serif"
GREEN, GREEN_DK, CREAM, CREAM2, INK, MUTED, HAIR, GOLD, GOLD_DK = (
    '#1C4734', '#0E2A1E', '#FAF7EE', '#F2EDDF', '#13201A', '#55645B', '#E4DDCB', '#C9A86A', '#8A6A2E')
PAGE = '#ECE8DA'  # fondo claro: aguanta el modo oscuro de Gmail sin que se pierdan textos
# Color de la etiqueta de cada tipo de aviso: (texto, fondo)
TAG = {'finde': (GREEN, '#E1ECE5'), 'pronto': ('#8A5A00', '#F7EBCF'), 'abre': ('#1E6B43', '#E3F0E7'), 'cierra': ('#8A5A00', '#F7EBCF'), 'nuevo': (GOLD_DK, '#F3E9D2'),
       'fecha': ('#3B4A41', '#ECE6D6'), 'plazo': ('#3B4A41', '#ECE6D6'), 'cancelado': ('#B83232', '#F6E1DE')}
MES = {'es': ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC'],
       'en': ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']}
e = html.escape


def shell(lang, title, preheader, eyebrow, inner, footer, site=SITE):
    return (
        '<!DOCTYPE html><html lang="%s"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="color-scheme" content="light"><meta name="supported-color-schemes" content="light">'
        '<title>%s</title><style>@media (max-width:600px){.px{padding-left:22px!important;padding-right:22px!important}'
        '.h1{font-size:28px!important}}</style></head>'
        '<body style="margin:0;padding:0;background:%s">'
        '<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:transparent;mso-hide:all">%s%s</div>'
        '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" style="background:%s">'
        '<tr><td align="center" style="padding:28px 12px 34px">'
        '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" style="max-width:560px">'
        # Cabecera: marca y antetítulo
        '<tr><td style="padding:0 8px 18px"><table role="presentation" width="100%%" cellpadding="0" cellspacing="0"><tr>'
        '<td width="34" valign="middle"><img src="%s/icons/icon-192.png" width="30" height="30" alt="" '
        'style="display:block;border:0;border-radius:8px"></td>'
        '<td valign="middle" style="padding-left:10px;font:700 20px/1 %s;letter-spacing:-.02em;color:#1C4734">banderín</td>'
        '<td align="right" valign="middle" style="font:600 11px/1 %s;letter-spacing:.14em;text-transform:uppercase;color:%s">%s</td>'
        '</tr></table></td></tr>'
        # Tarjeta crema
        '<tr><td class="px" style="background:%s;border-radius:24px;padding:34px 34px 30px">%s</td></tr>'
        # Pie
        '<tr><td style="padding:22px 18px 0;text-align:center;font:12.5px/1.65 %s;color:#55645B">%s</td></tr>'
        '</table></td></tr></table></body></html>') % (
        lang, e(title), PAGE, e(preheader), '&nbsp;&zwnj;' * 40, PAGE, site, SANS, SANS, GOLD_DK, e(eyebrow),
        CREAM, inner, SANS, footer)


def h1(text):
    return ('<h1 class="h1" style="margin:0 0 12px;font-family:%s;font-weight:400;font-size:32px;line-height:1.05;'
            'letter-spacing:-.01em;color:%s">%s</h1>') % (SERIF, INK, e(text))


def para(text, size=15.5, color=MUTED, margin='0 0 22px'):
    return '<p style="margin:%s;font:%spx/1.6 %s;color:%s">%s</p>' % (margin, size, SANS, color, text)


def button(url, label, big=True, solid=True):
    pad, size = ('15px 26px', 15.5) if big else ('10px 16px', 14)
    style = ('background:#DDEBE1;color:#17643F;border:1.5px solid #17643F' ) if solid else \
        ('background:transparent;color:%s;border:1px solid %s' % (GREEN, GREEN))
    return ('<a href="%s" style="display:inline-block;%s;font:600 %spx/1 %s;text-decoration:none;'
            'padding:%s;border-radius:999px">%s</a>') % (e(url), style, size, SANS, pad, e(label))


def bullets(items):
    rows = ''.join(
        '<tr><td width="18" valign="top" style="padding:6px 0"><div style="width:7px;height:7px;border-radius:50%%;'
        'background:%s;margin-top:7px"></div></td><td style="padding:4px 0;font:15px/1.5 %s;color:%s">%s</td></tr>' % (
            GOLD, SANS, INK, e(x)) for x in items)
    return '<table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 26px">%s</table>' % rows


def footer(lang, manage=None, unsub=None, why=None):
    links = []
    if manage:
        links.append('<a href="%s" style="color:%s;text-decoration:underline">%s</a>' % (
            e(manage), GREEN, 'Manage alerts' if lang == 'en' else 'Gestionar avisos'))
    if unsub:
        links.append('<a href="%s" style="color:%s;text-decoration:underline">%s</a>' % (
            e(unsub), GREEN, 'Unsubscribe' if lang == 'en' else 'Darme de baja'))
    parts = []
    if why:
        parts.append(e(why))
    if links:
        parts.append(' &nbsp;·&nbsp; '.join(links))
    parts.append(('Banderín · a project by Esclusa · Always confirm dates and conditions with the organiser.' if lang == 'en'
                  else 'Banderín · un proyecto de Esclusa · Confirma siempre fechas y condiciones con el organizador.'))
    return '<br>'.join(parts)


def item(lang, tipo, tag_label, t, url, btn_label):
    col, bg = TAG.get(tipo, TAG['fecha'])
    d = dt.date.fromisoformat(t['s'])
    where = ' · '.join(v for v in [t.get('club'), t.get('city'), t.get('prov')] if v and v != 'Por confirmar')
    solid = tipo in ('abre', 'cierra')
    return (
        '<table role="presentation" width="100%%" cellpadding="0" cellspacing="0" style="border-top:1px solid %s"><tr>'
        '<td width="72" valign="top" style="padding:18px 14px 18px 0">'
        '<table role="presentation" width="58" cellpadding="0" cellspacing="0" style="background:%s;border-radius:14px">'
        '<tr><td align="center" style="padding:9px 0 3px;font:700 10.5px/1 %s;letter-spacing:.12em;color:%s">%s</td></tr>'
        '<tr><td align="center" style="padding:0 0 10px;font:400 27px/1 %s;color:%s">%d</td></tr></table></td>'
        '<td valign="top" style="padding:18px 0">'
        '<span style="display:inline-block;background:%s;color:%s;font:700 11px/1 %s;letter-spacing:.06em;'
        'text-transform:uppercase;padding:6px 10px;border-radius:999px">%s</span>'
        '<p style="margin:9px 0 3px;font:600 16.5px/1.3 %s;color:%s">%s</p>'
        '<p style="margin:0 0 13px;font:14px/1.45 %s;color:%s">%s</p>%s</td></tr></table>') % (
        HAIR, CREAM2, SANS, GOLD_DK, MES[lang][d.month - 1], SERIF, INK, d.day,
        bg, col, SANS, e(tag_label), SANS, INK, e(t['n']), SANS, MUTED, e(where),
        button(url, btn_label + ' →', big=False, solid=solid))


def section(eyebrow, title):
    """Cabecera de un bloque secundario del correo (p. ej. «También en tu comunidad»)."""
    return ('<div style="margin:30px 0 4px;padding-top:22px;border-top:2px solid %s">'
            '<p style="margin:0 0 6px;font:600 11px/1 %s;letter-spacing:.14em;text-transform:uppercase;color:%s">%s</p>'
            '<h2 style="margin:0 0 4px;font-family:%s;font-weight:400;font-size:24px;line-height:1.1;color:%s">%s</h2></div>') % (
        HAIR, SANS, GOLD_DK, e(eyebrow), SERIF, INK, e(title))
