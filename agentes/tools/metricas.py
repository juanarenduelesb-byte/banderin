#!/usr/bin/env python3
"""Métricas semanales de Banderín sin IA: D1 (avisos), torneos y ejecuciones.
Escribe agentes/historico/semanas/AAAA-Wnn-datos.md y añade una fila a agentes/historico/metricas.csv.
Necesita CF_ACCOUNT_ID, D1_DATABASE_ID y CF_API_TOKEN (los mismos que la actualización diaria). Nunca lee correos."""
import os, json, csv, datetime, subprocess, urllib.request, collections
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
H = os.path.join(ROOT, 'agentes', 'historico')
def d1(sql):
    u = 'https://api.cloudflare.com/client/v4/accounts/%s/d1/database/%s/query' % (os.environ['CF_ACCOUNT_ID'], os.environ['D1_DATABASE_ID'])
    r = urllib.request.Request(u, method='POST', data=json.dumps({'sql': sql}).encode(), headers={'Authorization': 'Bearer ' + os.environ['CF_API_TOKEN'], 'Content-Type': 'application/json'})
    d = json.load(urllib.request.urlopen(r, timeout=30))
    if not d.get('success'): raise RuntimeError(d.get('errors'))
    return d['result'][0].get('results') or []
hoy = datetime.date.today(); ini = hoy - datetime.timedelta(days=7)
ano, sem, _ = hoy.isocalendar(); tag = f'{ano}-W{sem:02d}'
M = collections.OrderedDict(fecha=hoy.isoformat())
try:
    one = lambda s: list(d1(s)[0].values())[0]
    M['suscriptores_activos'] = one("SELECT COUNT(*) n FROM suscriptores WHERE estado='activo'")
    M['pendientes'] = one("SELECT COUNT(*) n FROM suscriptores WHERE estado='pendiente'")
    M['altas_semana'] = one(f"SELECT COUNT(*) n FROM suscriptores WHERE estado='activo' AND substr(COALESCE(confirmado,creado),1,10) >= '{ini}'")
    M['con_perfil'] = one("SELECT COUNT(*) n FROM suscriptores WHERE estado='activo' AND perfil IS NOT NULL")
    M['avisos_enviados_semana'] = one(f"SELECT COUNT(DISTINCT suscriptor || fecha) n FROM enviados WHERE fecha >= '{ini}'")
    M['activos_ultima_semana'] = one(f"SELECT COUNT(*) n FROM suscriptores WHERE estado='activo' AND substr(COALESCE(ultima_actividad,''),1,10) >= '{ini}'")
    seg = d1("SELECT tipo, COUNT(*) n FROM seguimientos GROUP BY tipo")
    M['seguimientos'] = ' · '.join(f"{x['tipo']} {x['n']}" for x in seg)
except Exception as e:
    M['error_d1'] = repr(e)[:200]
q = subprocess.run(['node', '-e', 'global.window={};eval(require("fs").readFileSync(0,"utf8"));const T=window.TORNEOS;const c={};for(const t of T){c[t.src]=(c[t.src]||0)+1};process.stdout.write(JSON.stringify({n:T.length,sinprov:T.filter(t=>!t.prov).length,src:c}))'],
                   input=open(os.path.join(ROOT, 'site', 'data.js')).read(), capture_output=True, text=True)
t = json.loads(q.stdout); M['torneos'] = t['n']; M['sin_provincia'] = t['sinprov']
M['fuentes'] = ' · '.join(f'{k} {v}' for k, v in sorted(t['src'].items(), key=lambda x: -x[1])[:5])
os.makedirs(os.path.join(H, 'semanas'), exist_ok=True)
cp = os.path.join(H, 'metricas.csv'); prev = None
campos = ['fecha', 'suscriptores_activos', 'pendientes', 'altas_semana', 'con_perfil', 'activos_ultima_semana', 'avisos_enviados_semana', 'torneos', 'sin_provincia']
if os.path.exists(cp):
    filas = list(csv.DictReader(open(cp))); prev = filas[-1] if filas else None
nuevo = not os.path.exists(cp)
with open(cp, 'a', newline='') as f:
    w = csv.DictWriter(f, fieldnames=campos, extrasaction='ignore')
    if nuevo: w.writeheader()
    w.writerow(M)
def var(k):
    try: return f"{int(M[k]) - int(prev[k]):+d}" if prev else '—'
    except Exception: return '—'
L = [f'# Datos de la semana {tag}', '', f'Generado sin IA por `agentes/tools/metricas.py` el {hoy:%d/%m/%Y}. El analista escribe encima la explicación y las decisiones.', '',
     '| Métrica | Valor | Variación | Fuente |', '|---|---|---|---|']
for k, f in [('suscriptores_activos', 'D1'), ('altas_semana', 'D1'), ('pendientes', 'D1'), ('con_perfil', 'D1'), ('activos_ultima_semana', 'D1'), ('avisos_enviados_semana', 'D1'), ('torneos', 'site/data.js'), ('sin_provincia', 'site/data.js')]:
    L.append(f'| {k.replace("_", " ").capitalize()} | {M.get(k, "[POR CONFIRMAR]")} | {var(k)} | {f} |')
L += ['', f"**Seguimientos:** {M.get('seguimientos', '—')}", f"**Fuentes:** {M['fuentes']}"] + ([f"**Error D1:** {M['error_d1']}"] if 'error_d1' in M else []) + ['',
      'Pendientes de medir: visitas (Cloudflare Web Analytics), cuentas (Supabase), Instagram (Metricool).', '']
open(os.path.join(H, 'semanas', f'{tag}-datos.md'), 'w').write('\n'.join(L))
print('\n'.join(L))
