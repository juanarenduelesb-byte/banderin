#!/usr/bin/env python3
"""Deja imágenes y vídeos en una carpeta pública de la web para que Metricool los pueda leer.

Metricool solo programa con enlaces públicos, y los archivos de la oficina son privados. Esto copia las
piezas a site/publicar/<id>/ (se publica con la web en Cloudflare Pages, sin indexar: robots.txt) y
espera a que estén en línea.

  python3 agentes/tools/publicar_media.py <id-encargo> archivo1.png archivo2.png …   → imprime las URL públicas (JSON)
  python3 agentes/tools/publicar_media.py --esperar <url>                              → espera a que responda 200 (máx. 6 min)
  python3 agentes/tools/publicar_media.py --limpiar                                    → borra carpetas de más de 30 días

Después de copiar hay que hacer commit y push (la web se despliega sola desde main).
"""
import json, re, shutil, sys, time, urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DIR = RAIZ / 'site' / 'publicar'
BASE = 'https://banderin.es/publicar'
TIPOS = {'.png', '.jpg', '.jpeg', '.mp4', '.mov'}



def copiar(tid, ficheros):
    if not re.fullmatch(r'[A-Za-z0-9_-]{4,40}', tid):
        sys.exit('id de encargo no válido')
    dest = DIR / tid
    dest.mkdir(parents=True, exist_ok=True)
    urls = []
    for i, f in enumerate(ficheros, 1):
        p = Path(f)
        ext = p.suffix.lower()
        if ext not in TIPOS:
            sys.exit(f'tipo no admitido: {p.name}')
        if p.stat().st_size > 24 * 1024 * 1024:
            sys.exit(f'{p.name} pesa más de 24 MB: recodifícalo (Cloudflare Pages no admite más de 25 MiB)')
        nombre = f'{i:02d}{ext}'
        shutil.copyfile(p, dest / nombre)
        urls.append(f'{BASE}/{tid}/{nombre}')
    (dest / 'fecha.txt').write_text(time.strftime('%Y-%m-%d'), encoding='utf-8')
    print(json.dumps(urls, ensure_ascii=False))


def esperar(url):
    for _ in range(36):
        try:
            req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'banderin-productor'})
            with urllib.request.urlopen(req, timeout=15) as r:
                if r.status == 200:
                    print('en línea:', url)
                    return
        except Exception:
            pass
        time.sleep(10)
    sys.exit('no responde todavía: ' + url)


def limpiar():
    if not DIR.exists():
        return
    hoy = time.time()
    for d in DIR.iterdir():
        f = d / 'fecha.txt'
        if d.is_dir() and f.exists():
            t = time.mktime(time.strptime(f.read_text().strip(), '%Y-%m-%d'))
            if hoy - t > 30 * 86400:
                shutil.rmtree(d)
                print('borrada', d.name)


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == '--limpiar':
        limpiar()
    elif a[0] == '--esperar':
        esperar(a[1])
    else:
        copiar(a[0], a[1:])
