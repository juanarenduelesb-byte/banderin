import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import red  # BanderinBot: robots.txt, pausa e identificación
import json,re,os,html,time,urllib.request,concurrent.futures as cf
L=json.load(open('/home/claude/scr/nc_lists.json'))
rows={}
for code,v in L.items():
    for r in v:
        if r['date'] and r['date']>=(__import__('datetime').date.today()-__import__('datetime').timedelta(days=45)).isoformat():
            rows.setdefault(r['id'],r)
def get(id_):
    p=f'/home/claude/raw/nct/{id_}.html'
    if os.path.exists(p): return open(p).read()
    for k in range(3):
        try:
            h=urllib.request.urlopen(urllib.request.Request(f'https://www.nextcaddy.com/tour/{id_}',headers={'User-Agent':'Mozilla/5.0 (Banderin)'}),timeout=20).read().decode('utf8','ignore')
            open(p,'w').write(h);return h
        except Exception: time.sleep(1+k)
    return ''
def text(h):
    h=re.sub(r'<svg.*?</svg>|<style.*?</style>|<script.*?</script>','',h,flags=re.S)
    t=re.sub(r'<[^>]+>',' | ',h);t=html.unescape(t).replace('\xa0',' ')
    t=re.sub(r'(\s*\|\s*)+',' | ',t);return re.sub(r'[ \t\r\n]+',' ',t)
def parse(id_):
    h=get(id_);t=text(h)
    cut=t.find('Esta competicion se encuentra');core=t[:cut if cut>0 else 4000]
    o={'id':id_}
    o['tarifas']=[(a.strip(' |:'),float(b.replace('.','').replace(',','.')) if ',' in b else float(b)) for a,b in re.findall(r'\|\s*([^|]{2,60}?):\s*\|?\s*([\d.,]+)\s*€',core)]
    pz=re.search(r'Plazo[^|]*\|\s*(\d\d)/(\d\d)/(\d\d)\s*\|?\s*[\d:]*\s*\|?\s*(\d\d)/(\d\d)/(\d\d)',core)
    if pz: o['op']='20%s-%s-%s'%(pz.group(3),pz.group(2),pz.group(1));o['cl']='20%s-%s-%s'%(pz.group(6),pz.group(5),pz.group(4))
    pl=re.search(r'Plazas disponibles:?\s*\|?\s*(\d+)',core);o['plazas']=int(pl.group(1)) if pl else None
    mod=re.search(r'\|\s*((?:Medal Play|Stableford|Match Play|Scramble|Fourball|Four[- ]?ball|Foursome|Greensome|Copa Canadá|Bogey|Texas Scramble|Chapman)[^|]{0,40})\|',core,re.I)
    o['mod_raw']=mod.group(1).strip() if mod else None
    o['ins_email']='Inscripción por email' in core or 'por email' in core
    o['cerrada']=bool(re.search(r'Inscripci[oó]n cerrada|Plazo finalizado|Fuera de plazo',core,re.I))
    o['core']=core[:700]
    # Resultados publicados por el organizador (premios o clasificación); no se copian nombres
    o['results']=('clasificaciones-container' in h or bool(re.search(r'\|\s*Premios\s*\|\s*Ganador',t))) and 'publican automáticamente' not in t
    return o
with cf.ThreadPoolExecutor(6) as ex:
    out=list(ex.map(parse,sorted(rows)))
D={o['id']:{**rows[o['id']],**o} for o in out}
json.dump(D,open('/home/claude/scr/nc_tours.json','w'),ensure_ascii=False)
print(len(D),'con precio',sum(1 for o in out if o['tarifas']),'con plazo',sum(1 for o in out if o.get('op')),'con modalidad',sum(1 for o in out if o['mod_raw']))
for o in out[:4]: print(o['id'],o['tarifas'],o.get('op'),o.get('cl'),o['mod_raw'],o['plazas'],'|',o['core'][:300])
