#!/usr/bin/env python3
"""Comprobaciones de salud de Banderín (agente de operaciones).
Uso: python3 agentes/tools/comprobar.py [--rapido] [--json]
--rapido: solo comprobaciones locales (datos del repositorio); úsalo antes de cada merge.
Sale con 0 si todo está en verde, 1 si hay avisos y 2 si hay fallos."""
import json, os, re, subprocess, sys, datetime, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REPO = 'juanarenduelesb-byte/banderin'
RAPIDO = '--rapido' in sys.argv
res = []
def r(estado, que, detalle=''): res.append(dict(estado=estado, que=que, detalle=detalle))
def sh(*c, **k):
    try: return subprocess.run(c, cwd=ROOT, capture_output=True, text=True, timeout=k.get('t', 120))
    except Exception as e: return None
def torneos(texto):
    p = sh('node', '-e', 'global.window={};eval(require("fs").readFileSync(0,"utf8"));process.stdout.write(JSON.stringify(window.TORNEOS))', t=60) if False else None
    q = subprocess.run(['node', '-e', 'global.window={};eval(require("fs").readFileSync(0,"utf8"));process.stdout.write(JSON.stringify(window.TORNEOS))'], input=texto, capture_output=True, text=True, timeout=60)
    return json.loads(q.stdout)
hoy = datetime.datetime.now(datetime.timezone.utc)
# 1. Datos de la web
try:
    T = torneos(open(os.path.join(ROOT, 'site', 'data.js')).read())
    n = len(T); r('ok' if n >= 500 else 'fallo', 'Torneos en la web', f'{n}')
    sinp = sum(1 for t in T if not t.get('prov')); pct = 100 * sinp / max(n, 1)
    r('ok' if pct < 3 else ('aviso' if pct < 10 else 'fallo'), 'Torneos sin provincia', f'{sinp} ({pct:.1f} %)')
    sinll = sum(1 for t in T if not t.get('ll')); pll = 100 * sinll / max(n, 1)
    r('ok' if pll < 15 else 'aviso', 'Torneos sin coordenadas (mapa)', f'{sinll} ({pll:.1f} %)')
    gd = [t for t in T if 'golfdirecto' in (t.get('url') or '')]
    cg = sum(1 for t in gd if t.get('cg'))
    r('ok' if gd and not cg else ('aviso' if gd else 'fallo'), 'Golf Directo', f'{len(gd)} torneos, {cg} congelados')
    malos = [t for t in gd if t.get('price') is not None or t.get('priceNote') or t.get('res')]
    r('ok' if not malos else 'fallo', 'Acuerdo Golf Directo (sin precios ni resultados)', f'{len(malos)} torneos con precio o resultado')
    # Comparación con la copia de hace ~24 h
    lg = sh('git', 'log', '--format=%H %cI', '--since=36 hours ago', '--', 'site/data.js')
    lines = [l.split() for l in (lg.stdout.strip().splitlines() if lg and lg.returncode == 0 else [])]
    old = None
    for h, d in lines:
        if hoy - datetime.datetime.fromisoformat(d) >= datetime.timedelta(hours=20): old = h; break
    if old:
        prev = torneos(sh('git', 'show', f'{old}:site/data.js').stdout)
        var = 100 * (n - len(prev)) / max(len(prev), 1)
        r('ok' if var > -15 else ('aviso' if var > -40 else 'fallo'), 'Variación de torneos frente a hace ~1 día', f'{len(prev)} → {n} ({var:+.1f} %)')
    else:
        r('aviso', 'Variación de torneos frente a hace ~1 día', 'sin copia de hace 20–36 h para comparar (¿no se actualiza?)')
except Exception as e:
    r('fallo', 'Leer site/data.js', repr(e)[:200])
# 2. Permiso escrito de Golf Directo
try:
    m = re.search(r"PERMISOS\s*=\s*\{[^}]*'(\d{4}-\d{2}-\d{2})'", open(os.path.join(ROOT, 'pipeline', 'red.py')).read())
    if m:
        dias = (datetime.date.fromisoformat(m.group(1)) - hoy.date()).days
        r('ok' if dias > 5 else ('aviso' if dias >= 0 else 'aviso'), 'Permiso escrito de Golf Directo en red.py',
          f'caduca {m.group(1)} ({dias} días)' + ('; desde entonces manda su robots.txt: compruébalo' if dias <= 5 else ''))
except Exception as e: r('aviso', 'Permiso de Golf Directo', repr(e)[:120])
if not RAPIDO:
    # 3. Última actualización publicada
    lg = sh('git', 'log', '-1', '--format=%cI %s', '--grep=Torneos actualizados')
    if lg and lg.stdout.strip():
        d, s = lg.stdout.strip().split(' ', 1); h = (hoy - datetime.datetime.fromisoformat(d)).total_seconds() / 3600
        r('ok' if h < 10 else ('aviso' if h < 26 else 'fallo'), 'Última actualización publicada', f'hace {h:.1f} h ({s})')
    # 4. Ejecuciones de GitHub Actions y avisos por correo
    j = sh('gh', 'api', f'repos/{REPO}/actions/workflows/actualizar.yml/runs?per_page=8')
    if j and j.returncode == 0:
        runs = json.loads(j.stdout)['workflow_runs']
        fall = [x for x in runs if x['conclusion'] == 'failure' and hoy - datetime.datetime.fromisoformat(x['created_at'].replace('Z', '+00:00')) < datetime.timedelta(hours=24)]
        r('ok' if not fall else 'fallo', 'Actualizaciones fallidas en 24 h', ', '.join(str(x['id']) for x in fall) or '0')
        # Avisos: como mucho un correo al día por persona, así que basta con que alguna ejecución de hoy (Madrid) haya enviado.
        madrid = lambda d: (datetime.datetime.fromisoformat(d.replace('Z', '+00:00')) + datetime.timedelta(hours=1)).date()
        hoym = (hoy + datetime.timedelta(hours=1)).date(); vistos = []
        for x in [x for x in runs if x['conclusion'] == 'success' and madrid(x['created_at']) == hoym][:4]:
            lg = sh('gh', 'run', 'view', str(x['id']), '--repo', REPO, '--log', t=180)
            m = re.search(r'avisos: (\d+) novedades, (\d+) suscriptores activos, (\d+) correos enviados, (\d+) errores', lg.stdout if lg else '')
            if m: vistos.append((x['created_at'], *map(int, m.groups())))
        if vistos:
            env = sum(v[3] for v in vistos); err = sum(v[4] for v in vistos); nov = max(v[1] for v in vistos); sus = max(v[2] for v in vistos)
            est = 'fallo' if (nov > 0 and sus > 0 and env == 0) or err > 0 else 'ok'
            r(est, 'Avisos por correo hoy', f'{len(vistos)} ejecuciones: {env} enviados, {err} errores (novedades {nov}, activos {sus})')
        else:
            r('aviso', 'Avisos por correo hoy', 'ninguna ejecución de hoy con avisos todavía')
    else:
        r('aviso', 'GitHub Actions', 'no se pudo consultar con gh api (¿sin credenciales?)')
    # 5. Web en producción
    try:
        q = urllib.request.Request('https://banderin.es/', headers={'User-Agent': 'BanderinBot-salud (+https://banderin.es)'})
        h = urllib.request.urlopen(q, timeout=20); body = h.read().decode('utf8', 'ignore')
        r('ok' if h.status == 200 and 'banderin' in body.lower() else 'fallo', 'Web en producción', f'HTTP {h.status}')
    except Exception as e:
        r('aviso', 'Web en producción', f'no comprobable desde aquí ({type(e).__name__}); compruébala con WebFetch')
# Salida
ic = {'ok': '🟢', 'aviso': '🟡', 'fallo': '🔴'}
if '--json' in sys.argv: print(json.dumps(res, ensure_ascii=False, indent=1))
else:
    for x in res: print(f"{ic[x['estado']]} {x['que']}: {x['detalle']}")
peor = 2 if any(x['estado'] == 'fallo' for x in res) else (1 if any(x['estado'] == 'aviso' for x in res) else 0)
sys.exit(peor)
