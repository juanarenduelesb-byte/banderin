#!/usr/bin/env python3
"""Láminas de Banderín (carrusel, publicación o story) a partir de un JSON. Sin IA: HTML + Playwright.

Uso:  python3 marketing/carrusel/hacer.py pieza.json salida/
      → salida/01.png, 02.png… (1080×1350; story 1080×1920) y salida/portada.jpg

pieza.json:
{
  "formato": "carrusel" | "post" | "story",
  "laminas": [
    {"tipo": "portada", "antetitulo": "Para guardar", "titulo": "Todos los torneos", "cursiva": "en un sitio", "texto": "…", "imagen": "fondo.jpg"},
    {"tipo": "normal",  "antetitulo": "01", "titulo": "…", "texto": "…", "cita": "…"},
    {"tipo": "cifra",   "cifra": "184", "titulo": "torneos este finde", "texto": "Datos a 28/11/2026"},
    {"tipo": "lista",   "titulo": "…", "items": ["…", "…"]},
    {"tipo": "cta",     "titulo": "Tu próximo torneo", "texto": "…"}
  ]
}
"imagen" (opcional, en cualquier lámina): ruta a una foto; va de fondo con un velo para que el texto se lea.
Texto plano: se escapa todo. Nunca precios, jugadores ni resultados (acuerdo con Golf Directo).
"""
import html, json, sys, base64, mimetypes
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
FONTS = RAIZ / 'site' / 'fonts'
ICON = RAIZ / 'site' / 'icons' / 'icon-192.png'


def uri(p):
    p = Path(p)
    mt = mimetypes.guess_type(p.name)[0] or 'application/octet-stream'
    return f'data:{mt};base64,' + base64.b64encode(p.read_bytes()).decode()


def font(fam, fich, w=400, it=False):
    return (f"@font-face{{font-family:{fam};font-weight:{w};font-style:{'italic' if it else 'normal'};"
            f"src:url({uri(FONTS / fich)})}}")


CSS = ''.join([
    font('PS', 'public-sans-latin-500-normal.woff2', 500), font('PS', 'public-sans-latin-700-normal.woff2', 700),
    font('Cas', 'libre-caslon-display-latin-400-normal.woff2'), font('ISit', 'instrument-serif-latin-400-italic.woff2', 400, True),
    font('Logo', 'instrument-sans-latin-700-normal.woff2', 700)]) + '''
*{margin:0;padding:0;box-sizing:border-box}body{margin:0;font-family:PS;background:#000}
.s{width:1080px;height:var(--h);position:relative;overflow:hidden;background:#F4EFE3;color:#14201A;padding:110px 96px}
.s.osc{background:radial-gradient(110% 80% at 50% 30%,#1F5139 0%,#123323 60%,#071710 100%);color:#F4F1E8}
.s.oro{background:#E9C77E;color:#123323}
.bg{position:absolute;inset:0;background-size:cover;background-position:center}
.bg::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(7,23,16,.35) 0%,rgba(7,23,16,.55) 45%,rgba(7,23,16,.92) 100%)}
.s.foto{color:#F4F1E8}.in{position:relative;z-index:1;height:100%}
.k{font-weight:700;font-size:30px;letter-spacing:.22em;text-transform:uppercase;color:#8A6A2E}.osc .k,.foto .k{color:#E9C77E}
h1{font-family:Logo;font-weight:700;font-size:132px;line-height:.94;letter-spacing:-.045em;margin-top:170px}
h1 em,h2 em{font-family:ISit;font-weight:400;font-style:italic;letter-spacing:-.01em;color:#E9C77E}.oro h1 em{color:#123323}
h2{font-family:Cas;font-weight:400;font-size:96px;line-height:1.02;letter-spacing:-.02em;margin-top:60px}
.t{font-size:44px;line-height:1.35;margin-top:44px;max-width:880px;opacity:.86}
.cf{font-family:Cas;font-size:330px;line-height:.9;letter-spacing:-.04em;color:#E9C77E;margin-top:120px}
.q{position:absolute;left:0;right:0;bottom:120px;background:#123323;color:#F4F1E8;border-radius:36px;padding:40px 48px;font-family:ISit;font-style:italic;font-size:58px;line-height:1.1}
.osc .q,.foto .q{background:#E9C77E;color:#123323}
ul{list-style:none;margin-top:56px}li{font-size:48px;line-height:1.25;padding:26px 0 26px 70px;position:relative;border-top:2px solid rgba(20,32,26,.12)}
.osc li,.foto li{border-color:rgba(244,241,232,.18)}li::before{content:"";position:absolute;left:0;top:40px;width:34px;height:34px;border-radius:50%;background:#1F6B45}
.osc li::before,.foto li::before{background:#E9C77E}
.url{display:inline-block;margin-top:56px;background:#123323;color:#F4F1E8;border-radius:999px;padding:28px 64px;font-family:Logo;font-weight:700;font-size:84px;letter-spacing:-.03em}
.sw{position:absolute;right:0;bottom:120px;background:#F4F1E8;color:#123323;border-radius:999px;padding:22px 44px;font-weight:700;font-size:36px}
.ft{position:absolute;left:96px;right:96px;bottom:60px;display:flex;justify-content:space-between;align-items:center;font-size:30px;font-weight:600;opacity:.78;z-index:2}
.lg{display:flex;align-items:center;gap:14px;font-family:Logo;font-weight:700;font-size:36px;letter-spacing:-.03em}.lg img{width:48px;height:48px;border-radius:12px}
'''


def e(x):
    return html.escape(str(x or ''))


def lamina(L, i, n, h, base):
    tipo = L.get('tipo', 'normal')
    img = L.get('imagen')
    cls = {'portada': 'osc', 'cifra': 'osc', 'cta': 'oro'}.get(tipo, '')
    if img:
        p = Path(img) if Path(img).is_absolute() else base / img
        cls = 'foto'
        bg = f'<div class="bg" style="background-image:url({uri(p)})"></div>'
    else:
        bg = ''
    tit = e(L.get('titulo')) + (f' <em>{e(L["cursiva"])}</em>' if L.get('cursiva') else '')
    k = f'<p class="k">{e(L["antetitulo"])}</p>' if L.get('antetitulo') else ''
    t = f'<p class="t">{e(L["texto"])}</p>' if L.get('texto') else ''
    if tipo == 'portada':
        body = f'{k}<h1>{tit}</h1>{t}' + ('<div class="sw">Desliza →</div>' if n > 1 else '')
    elif tipo == 'cifra':
        body = f'{k}<div class="cf">{e(L.get("cifra"))}</div><h2>{tit}</h2>{t}'
    elif tipo == 'lista':
        body = f'{k}<h2>{tit}</h2><ul>' + ''.join(f'<li>{e(x)}</li>' for x in L.get('items', [])) + f'</ul>{t}'
    elif tipo == 'cta':
        body = f'{k}<h1 style="margin-top:120px">{tit}</h1>{t}<div class="url">banderin.es</div>'
    else:
        body = f'{k}<h2>{tit}</h2>{t}' + (f'<div class="q">{e(L["cita"])}</div>' if L.get('cita') else '')
    num = f'<span>{i}/{n}</span>' if n > 1 else '<span>banderin.es</span>'
    return (f'<section class="s {cls}" style="--h:{h}px">{bg}<div class="in">{body}</div>'
            f'<div class="ft"><span class="lg"><img src="{uri(ICON)}">banderín</span>{num}</div></section>')


def main():
    spec_p, out = Path(sys.argv[1]), Path(sys.argv[2])
    spec = json.loads(spec_p.read_text(encoding='utf-8'))
    out.mkdir(parents=True, exist_ok=True)
    h = 1920 if spec.get('formato') == 'story' else 1350
    L = spec['laminas']
    page = f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>' + \
        ''.join(lamina(x, i + 1, len(L), h, spec_p.parent) for i, x in enumerate(L)) + '</body></html>'
    (out / 'laminas.html').write_text(page, encoding='utf-8')
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1080, 'height': h})
        pg.set_content(page, wait_until='load')
        pg.evaluate('document.fonts.ready')
        pg.wait_for_timeout(300)
        for i, s in enumerate(pg.query_selector_all('section.s')):
            s.screenshot(path=str(out / f'{i + 1:02d}.png'))
        b.close()
    from PIL import Image
    Image.open(out / '01.png').convert('RGB').save(out / 'portada.jpg', quality=88)
    print(f'{len(L)} láminas en {out}')


if __name__ == '__main__':
    main()
