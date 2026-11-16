#!/usr/bin/env python3
"""Banderín - comunicado puntual a toda la gente con cuenta o con avisos activos.

Destinatarios: suscriptores activos de los avisos (D1) + los correos de COMUNICADO_EXTRA (cuentas de
Supabase), sin repetir. Nunca a altas sin confirmar. Lo lanza el workflow «Comunicado» a mano.
  COMUNICADO_PRUEBA=correo → solo envía a esa dirección (para revisar antes).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import correo as c  # noqa: E402
import json  # noqa: E402
import urllib.request  # noqa: E402
from avisos import D1  # noqa: E402


def send(to, subject, body, txt):
    payload = {'sender': {'name': 'Banderín', 'email': os.environ['AVISOS_FROM']}, 'to': [{'email': to}],
               'subject': subject, 'htmlContent': body, 'textContent': txt}
    req = urllib.request.Request('https://api.brevo.com/v3/smtp/email', method='POST', data=json.dumps(payload).encode(),
                                 headers={'api-key': os.environ['BREVO_API_KEY'], 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as r:
        if r.status >= 300:
            raise RuntimeError('Brevo %s' % r.status)

SITE = 'https://banderin.es'
SUBJECT = 'Banderín ya tiene correo oficial: avisos@banderin.es'
PRE = 'A partir de ahora, todo lo de Banderín te llega desde esta dirección.'
BODY = (c.h1('Bienvenido a Banderín')
        + c.para('Desde hoy, todos los correos de Banderín (tus avisos, las confirmaciones y los de tu cuenta) te llegan '
                 'desde <b style="color:#13201A">avisos@banderin.es</b>, nuestro correo oficial. Añádelo a tus contactos '
                 'para que no acabe en la carpeta de spam.')
        + c.para('Gracias por estar desde el principio. Banderín reúne todos los torneos de golf de España en un solo '
                 'sitio, gratis, para que encontrar dónde jugar sea mucho más fácil.')
        + c.bullets(['Todos los torneos, revisados cada mañana', 'Avisos cuando abre y cierra la inscripción de lo que sigues',
                     'Filtros para ver solo los que encajan contigo'])
        + c.button(SITE, 'Abrir Banderín')
        + c.para('¿Aún no tienes los avisos? Actívalos desde tu perfil en banderin.es.', 13.5, '#6B776F', '26px 0 0'))
FOOT = ('Recibes este correo porque tienes una cuenta o los avisos activos en Banderín. Es un aviso puntual del servicio.<br>'
        'Banderín - Confirma siempre fechas y condiciones con el organizador.')
TXT = ('Bienvenido a Banderín\n\nDesde hoy, todos los correos de Banderín te llegan desde avisos@banderin.es, nuestro correo '
       'oficial. Añádelo a tus contactos para que no acabe en spam.\n\nGracias por estar desde el principio. Banderín reúne '
       'todos los torneos de golf de España en un solo sitio, gratis.\n\n' + SITE)

html = c.shell('es', SUBJECT, PRE, 'Novedades', BODY, FOOT)
prueba = os.environ.get('COMUNICADO_PRUEBA', '').strip()
if prueba:
    dest = [prueba]
else:
    dest = [r['email'] for r in D1().q("SELECT email FROM suscriptores WHERE estado = 'activo'")]
    dest += [x.strip().lower() for x in os.environ.get('COMUNICADO_EXTRA', '').replace(';', ',').split(',') if '@' in x]
    dest = sorted(set(dest))
ok = err = 0
for d in dest:
    try:
        send(d, SUBJECT, html, TXT)
        ok += 1
    except Exception as e:  # noqa: BLE001
        err += 1
        print('error:', type(e).__name__)
print('comunicado: %d enviados, %d errores' % (ok, err))
