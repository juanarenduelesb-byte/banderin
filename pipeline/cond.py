"""Banderín · condiciones de participación de cada torneo.

Lee el texto que publica la fuente (ficha de NextCaddy, información del torneo
en Golf Directo) y extrae solo las condiciones de inscripción que se pueden
afirmar sin dudas:

  hcp     hándicap máximo para inscribirse
  edadMin edad mínima (torneos senior y mid-amateur)
  edadMax edad máxima (torneos juveniles)
  priv    reservado a socios o a un grupo privado
  fed     solo federados de una comunidad

Criterio: ante la duda, no se extrae. Un límite de hándicap de una categoría de
premios ("1.ª categoría hasta 20,4") o un tope de hándicap de juego ("hándicap
limitado a 36,4") NO impide inscribirse y no se toma como condición.
"""
import html
import re

NUM = r'(\d{1,2}(?:[.,]\d)?)'


def plain(htm):
    t = re.sub(r'<(script|style)\b.*?</\1>', ' ', htm or '', flags=re.S | re.I)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    return re.sub(r'\s+', ' ', t).strip()


def _num(s):
    return float(s.replace(',', '.'))


def _near_category(text, start):
    return re.search(r'categor[ií]a|premio', text[max(0, start - 70):start], re.I) is not None


HCP_PATTERNS = [
    re.compile(r'l[ií]mite de (?:h[áa]ndicap|hcp) (?:de|para la|para) inscripci[oó]n\D{0,15}' + NUM, re.I),
    re.compile(r'h[áa]ndicap (?:exacto )?m[áa]ximo (?:de |para la |para )?inscripci[oó]n\D{0,15}' + NUM, re.I),
    re.compile(r'(?:podr[áa]n (?:participar|inscribirse|tomar parte)|abiert[oa] a|dirigid[oa] a)[^.;]{0,160}?'
               r'h[áa]ndicap (?:exacto )?(?:igual o inferior a|inferior o igual a|m[áa]ximo de|hasta)\s*' + NUM, re.I),
]
AGE_MIN = re.compile(r'(?:cumplan|tengan|con)\s+(?:al menos|como m[ií]nimo|un m[ií]nimo de)?\s*(\d{2})\s*a[ñn]os'
                     r'|mayores de\s*(\d{2})\s*a[ñn]os', re.I)
AGE_MAX = re.compile(r'menores de\s*(\d{1,2})\s*a[ñn]os|hasta (?:los )?(\d{1,2})\s*a[ñn]os', re.I)
PRIV_NAME = re.compile(r'privad[oa]|solo socios|s[óo]lo socios', re.I)
PRIV_TEXT = re.compile(r'(?:reservad[oa]|exclusiv[oa]|[úu]nicamente|solo|s[óo]lo)\s+(?:a|para)\s+(?:los\s+)?socios'
                       r'|torneo privado|grupo privado', re.I)
FED = {
    'Madrid': 'Comunidad de Madrid', 'Andaluza': 'Andalucía', 'Andalucía': 'Andalucía', 'Canaria': 'Canarias',
    'Castilla y León': 'Castilla y León', 'Comunitat Valenciana': 'Comunitat Valenciana', 'Catalana': 'Cataluña',
    'Vasca': 'País Vasco', 'Navarra': 'Comunidad Foral de Navarra', 'Riojana': 'La Rioja', 'Cántabra': 'Cantabria',
    'Castilla-La Mancha': 'Castilla-La Mancha', 'Asturias': 'Principado de Asturias', 'Gallega': 'Galicia',
    'Aragonesa': 'Aragón', 'Balear': 'Illes Balears', 'Extremeña': 'Extremadura', 'Región de Murcia': 'Región de Murcia',
}
FED_RE = re.compile(r'federad[oa]s\s+(?:por|en)\s+(?:la\s+)?(?:Real\s+)?Federaci[oó]n\s+(?:de\s+Golf\s+)?(?:de\s+la\s+|del\s+|de\s+)?(' +
                    '|'.join(re.escape(k) for k in FED) + ')', re.I)


def conditions(text, name='', cat=''):
    """Devuelve un dict solo con las condiciones encontradas (vacío si ninguna)."""
    t = text or ''
    out = {}
    hs = []
    for p in HCP_PATTERNS:
        for m in p.finditer(t):
            v = _num(m.group(1))
            if 0 < v <= 54 and not _near_category(t, m.start()):
                hs.append(v)
    if hs:
        out['hcp'] = max(hs)  # el más permisivo: nunca excluir de más
    if cat in ('Senior', 'Mid-Amateur'):
        ages = [int(a or b) for a, b in AGE_MIN.findall(t) if 18 <= int(a or b) <= 80]
        if ages:
            out['edadMin'] = min(ages)
    if cat == 'Juvenil':
        mx = []
        for m in AGE_MAX.finditer(t):
            if _near_category(t, m.start()):
                continue
            v = int(m.group(1)) - 1 if m.group(1) else int(m.group(2))
            if 6 <= v <= 25:
                mx.append(v)
        if mx:
            out['edadMax'] = max(mx)
    if PRIV_NAME.search(name or '') or PRIV_TEXT.search(t):
        out['priv'] = True
    m = FED_RE.search(t)
    if m:
        key = next(k for k in FED if k.lower() == m.group(1).lower())
        out['fed'] = FED[key]
    return out


def nextcaddy_text(path):
    """Texto de la ficha de NextCaddy guardada por nc_tours.py."""
    try:
        return plain(open(path, encoding='utf-8', errors='ignore').read())
    except OSError:
        return ''
