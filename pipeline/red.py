"""Banderín · acceso educado a webs ajenas.

Al importarlo, todas las descargas con urllib del programa diario:
  - se identifican como BanderinBot, con una página pública que explica quiénes somos (https://banderin.es/robot);
  - respetan el robots.txt de cada web (si una ruta está prohibida para nosotros, no se descarga);
  - van despacio: como mucho una petición por segundo a cada web.
Las API propias o de servicios contratados (Cloudflare, Brevo, geocodificación) no pasan por estos filtros.

Uso como programa (sustituye a curl en update.sh):  python3 -I red.py get URL SALIDA
"""
import sys, time, threading, urllib.request, urllib.parse, urllib.robotparser, urllib.error

UA = 'Mozilla/5.0 (compatible; BanderinBot/1.0; +https://banderin.es/robot)'
TOKEN = 'BanderinBot'
PAUSA = 1.0  # segundos mínimos entre dos peticiones a la misma web
EXENTOS = ('api.cloudflare.com', 'api.brevo.com', 'geocoding-api.open-meteo.com', 'banderin.es', 'www.banderin.es')

_orig_urlopen = urllib.request.urlopen
_orig_open = urllib.request.OpenerDirector.open
_robots, _ultimo, _lock = {}, {}, threading.Lock()
BLOQUEADAS = []


class ProhibidoPorRobots(urllib.error.URLError):
    pass


def _host(url):
    return urllib.parse.urlsplit(url).netloc.lower()


def _reglas(url):
    p = urllib.parse.urlsplit(url)
    base = '%s://%s' % (p.scheme, p.netloc)
    if base in _robots:
        return _robots[base]
    rp = urllib.robotparser.RobotFileParser()
    try:
        req = urllib.request.Request(base + '/robots.txt', headers={'User-Agent': UA})
        with _orig_urlopen(req, timeout=20) as r:
            rp.parse(r.read().decode('utf-8', 'replace').splitlines())
    except urllib.error.HTTPError as e:
        # 401/403: la web no deja leer su robots.txt -> por prudencia, no entramos. 404 y demás: sin reglas.
        rp.parse(['User-agent: *', 'Disallow: /'] if e.code in (401, 403) else [])
    except Exception:
        rp.parse([])  # sin respuesta: se trata como si no hubiera reglas
    _robots[base] = rp
    return rp


def _esperar(host):
    with _lock:
        t = time.monotonic()
        espera = _ultimo.get(host, 0) + PAUSA - t
        if espera > 0:
            time.sleep(espera)
        _ultimo[host] = time.monotonic()


def _preparar(req):
    if isinstance(req, str):
        req = urllib.request.Request(req)
    url = req.full_url
    host = _host(url)
    if host in EXENTOS or not url.startswith('http'):
        return req
    req.add_header('User-Agent', UA)  # sustituye la que traiga el programa
    if urllib.parse.urlsplit(url).path == '/robots.txt':
        return req
    if not _reglas(url).can_fetch(TOKEN, url):
        if url not in BLOQUEADAS:
            BLOQUEADAS.append(url)
            print('robots.txt no permite descargar', url, file=sys.stderr)
        raise ProhibidoPorRobots('robots.txt: ' + url)
    _esperar(host)
    return req


def _open(self, req, *a, **k):
    return _orig_open(self, _preparar(req), *a, **k)


# urlopen y los openers propios (con cookies) acaban todos en OpenerDirector.open
urllib.request.OpenerDirector.open = _open
urlopen = urllib.request.urlopen


if __name__ == '__main__' and len(sys.argv) == 4 and sys.argv[1] == 'get':
    try:
        with urlopen(sys.argv[2], timeout=60) as r:
            open(sys.argv[3], 'wb').write(r.read())
    except Exception as e:
        print('no se pudo descargar', sys.argv[2], e, file=sys.stderr)
        sys.exit(1)
