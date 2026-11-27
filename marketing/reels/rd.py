import json, datetime
_s = open('/home/claude/banderin/site/data.js').read()
T = json.loads(_s[_s.index('window.TORNEOS=') + 15:].rstrip().rstrip(';'))
HOY = '2026-11-18'
DIAS = ['LUN', 'MAR', 'MIÉ', 'JUE', 'VIE', 'SÁB', 'DOM']
def row(t, tag=None):
    d = datetime.date.fromisoformat(t['s'])
    sub = t['club'] + (' · ' + t['city'].split(' (')[0].title() if t.get('city') else '')
    if tag is None:
        tag = 'Abierta' if (not t.get('cl') or t['cl'] >= HOY) else 'Cerrada'
    n = t['n'] if len(t['n']) <= 34 else t['n'][:33].rstrip() + '…'
    if len(sub) > 40: sub = sub[:39].rstrip() + '…'
    return dict(m=DIAS[d.weekday()], dd=str(d.day), n=n, sub=sub, tag=tag, cls='ok')
def rng(a, b): return [t for t in T if t['s'] <= b and t['e'] >= a]
