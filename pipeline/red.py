"""Banderín · acceso educado a webs ajenas.

Al importarlo, todas las descargas con urllib del programa diario:
  - se identifican como BanderinBot, con una página pública que explica quiénes somos (https://banderin.es/robot);
  - respetan el robots.txt de cada web (si una ruta está prohibida para nosotros, no se descarga);
  - van despacio: como mucho una petición por segundo a cada web.
Las API propias o de servicios contratados (Cloudflare, Brevo, geocodificación) no pasan por estos filtros.

Uso como programa (sustituye a curl en update.sh):  python3 -I red.py get URL SALIDA
"""
import sys, os, re, time, threading, urllib.request, urllib.parse, urllib.error

UA = 'Mozilla/5.0 (compatible; BanderinBot/1.0; +https://banderin.es/robot)'
TOKEN = 'BanderinBot'
PAUSA = float(os.environ.get('BANDERIN_PAUSA', '0.5'))  # segundos mínimos entre dos peticiones a la misma web
# Calendarios publicados para suscribirse (.ics de Google Calendar): los lee igual que una app de calendario,
# no es rastreo, así que no se aplica el robots.txt de calendar.google.com.
SUSCRIPCION = re.compile(r'^https://calendar\.google\.com/calendar/ical/[^/]+/public/basic\.ics$')
EXENTOS = ('api.cloudflare.com', 'api.brevo.com', 'geocoding-api.open-meteo.com', 'banderin.es', 'www.banderin.es')

_orig_urlopen = urllib.request.urlopen
_orig_open = urllib.request.OpenerDirector.open
_robots, _ultimo, _locks, _lock = {}, {}, {}, threading.Lock()
BLOQUEADAS = []


class ProhibidoPorRobots(urllib.error.URLError):
    pass


def _host(url):
    return urllib.parse.urlsplit(url).netloc.lower()


class Reglas:
    """robots.txt según la norma RFC 9309: gana la regla más larga que encaja; a igualdad, Allow."""
    def __init__(self, lines=()):
        grupos, actual, ua_abierto = {}, None, False
        for raw in lines:
            line = raw.split('#', 1)[0].strip()
            if ':' not in line:
                continue
            k, v = [x.strip() for x in line.split(':', 1)]
            k = k.lower()
            if k == 'user-agent':
                if not ua_abierto:
                    actual = []
                ua_abierto = True
                grupos.setdefault(v.lower(), actual)
                # varios user-agent seguidos comparten las mismas reglas
                for ua, g in list(grupos.items()):
                    if g is not actual and ua == v.lower():
                        grupos[ua] = actual
            elif k in ('allow', 'disallow') and actual is not None:
                ua_abierto = False
                actual.append((k == 'allow', v))
        self.reglas = grupos.get(TOKEN.lower(), grupos.get('*', []))

    @staticmethod
    def _patron(p):
        r = re.escape(p).replace(r'\*', '.*')
        if r.endswith(r'\$'):
            r = r[:-2] + '$'
        return re.compile(r)

    def permite(self, url):
        p = urllib.parse.urlsplit(url)
        ruta = (p.path or '/') + ('?' + p.query if p.query else '')
        mejor = None
        for allow, patron in self.reglas:
            if not patron:
                continue  # «Disallow:» vacío no prohíbe nada
            if self._patron(patron).match(ruta):
                clave = (len(patron), allow)
                if mejor is None or clave > mejor[0]:
                    mejor = (clave, allow)
        return True if mejor is None else mejor[1]


def _reglas(url):
    p = urllib.parse.urlsplit(url)
    base = '%s://%s' % (p.scheme, p.netloc)
    if base in _robots:
        return _robots[base]
    try:
        req = urllib.request.Request(base + '/robots.txt', headers={'User-Agent': UA})
        with _orig_urlopen(req, timeout=20) as r:
            rp = Reglas(r.read().decode('utf-8', 'replace').splitlines())
    except urllib.error.HTTPError as e:
        # 401/403: la web no deja leer su robots.txt -> por prudencia, no entramos. 404 y demás: sin reglas.
        rp = Reglas(['User-agent: *', 'Disallow: /'] if e.code in (401, 403) else [])
    except Exception:
        rp = Reglas([])  # sin respuesta: se trata como si no hubiera reglas
    _robots[base] = rp
    return rp


def _esperar(host):
    with _lock:
        lk = _locks.setdefault(host, threading.Lock())
    with lk:  # cada web tiene su propia cola: las demás no esperan
        espera = _ultimo.get(host, 0) + PAUSA - time.monotonic()
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
    if not SUSCRIPCION.match(url) and not _reglas(url).permite(url):
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
