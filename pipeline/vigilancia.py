#!/usr/bin/env python3
"""Banderín - vigilancia diaria de seguridad.

1. Resume la actividad sospechosa de las últimas 24 horas (tabla «seguridad» de D1).
2. Comprueba en producción que las protecciones siguen puestas (HTTPS, cabeceras, archivos privados, CSRF).
3. Borra registros viejos (eventos de más de 30 días y límites caducados).
Si algo no cuadra, termina con error: GitHub te avisa por correo de que el workflow ha fallado.
  python3 pipeline/vigilancia.py
"""
import json
import os
import sys
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from avisos import D1  # noqa: E402

WEB = 'https://banderin.es'
UMBRAL_TOTAL = 300   # eventos sospechosos en 24 h
UMBRAL_IP = 60       # eventos de una misma huella de IP en 24 h
problemas = []


def pedir(url, metodo='GET', cabeceras=None, datos=None):
    req = urllib.request.Request(url, method=metodo, data=datos, headers={'User-Agent': 'BanderinVigilancia/1.0', **(cabeceras or {})})

    class SinRedireccion(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k):
            return None
    op = urllib.request.build_opener(SinRedireccion)
    try:
        with op.open(req, timeout=20) as r:
            return r.status, {k.lower(): v for k, v in r.headers.items()}
    except urllib.error.HTTPError as e:
        return e.code, {k.lower(): v for k, v in e.headers.items()}


# 1. Actividad sospechosa
try:
    db = D1()
    filas = db.q("SELECT tipo, ip, SUM(n) AS n FROM seguridad WHERE ventana > strftime('%Y-%m-%dT%H:%M:%S', 'now', '-1 day') GROUP BY tipo, ip")
    total = sum(f['n'] for f in filas)
    por_tipo, por_ip = {}, {}
    for f in filas:
        por_tipo[f['tipo']] = por_tipo.get(f['tipo'], 0) + f['n']
        por_ip[f['ip']] = por_ip.get(f['ip'], 0) + f['n']
    print('Actividad sospechosa en 24 h: %d eventos %s' % (total, json.dumps(por_tipo, ensure_ascii=False)))
    if total > UMBRAL_TOTAL:
        problemas.append('%d eventos sospechosos en 24 h (umbral %d)' % (total, UMBRAL_TOTAL))
    peor = max(por_ip.items(), key=lambda x: x[1], default=None)
    if peor and peor[1] > UMBRAL_IP:
        problemas.append('una misma IP ha generado %d eventos en 24 h' % peor[1])
    pend = db.q("SELECT COUNT(*) AS n FROM suscriptores WHERE estado = 'pendiente' AND creado > strftime('%Y-%m-%dT%H:%M:%S', 'now', '-1 day')")
    print('Altas sin confirmar en 24 h: %d' % pend[0]['n'])
    if pend[0]['n'] > 300:
        problemas.append('%d altas sin confirmar en 24 h: posible abuso del formulario' % pend[0]['n'])
    db.q("DELETE FROM seguridad WHERE ventana < strftime('%Y-%m-%dT%H:%M:%S', 'now', '-30 days')")
    db.q("DELETE FROM limites WHERE hasta < strftime('%Y-%m-%dT%H:%M:%S', 'now', '-1 day')")
except Exception as e:  # tabla sin crear o sin credenciales
    print('Aviso: no se pudo leer la tabla de seguridad (%s). ¿Falta db/migracion-2026-11-18-seguridad.sql?' % e)

# 2. Protecciones en producción
st, h = pedir('http://banderin.es/')
if st != 301 or not h.get('location', '').startswith('https://'):
    problemas.append('http:// no redirige a https:// (%s)' % st)
st, h = pedir(WEB + '/')
for c in ['strict-transport-security', 'content-security-policy', 'x-frame-options', 'x-content-type-options', 'referrer-policy', 'permissions-policy']:
    if c not in h:
        problemas.append('falta la cabecera %s' % c)
if 'access-control-allow-origin' in h:
    problemas.append('la web devuelve Access-Control-Allow-Origin')
for ruta in ['/.git/config', '/.env', '/db/schema.sql', '/lib/avisos.js', '/pipeline/avisos.py', '/README.md', '/.github/workflows/copia.yml']:
    st, _ = pedir(WEB + ruta)
    if st != 404:
        problemas.append('%s responde %s (debería ser 404)' % (ruta, st))
st, _ = pedir(WEB + '/api/avisos/alta', 'POST', {'Origin': 'https://ejemplo-malicioso.com', 'Content-Type': 'application/json'}, b'{}')
if st != 403:
    problemas.append('la API acepta escrituras desde otra web (%s)' % st)
st, _ = pedir(WEB + '/api/avisos/yo', cabeceras={'Authorization': 'Bearer falsa'})
if st != 401:
    problemas.append('la API acepta una llave falsa (%s)' % st)

if problemas:
    print('\nPROBLEMAS:\n- ' + '\n- '.join(problemas))
    sys.exit(1)
print('Todo en orden.')
