import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import red  # BanderinBot: robots.txt, pausa e identificación
import json,urllib.request,urllib.parse,datetime as dt,time,os,concurrent.futures as cf
B='https://www.golfdirecto.com/api/v2/public/tournament/last'
def get(url):
    for k in range(3):
        try: return json.loads(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (Banderin)'}),timeout=40).read())
        except Exception as e: time.sleep(2+k)
    return None
def window(a,b,profile):
    q=urllib.parse.urlencode({'filter[profile]':profile,'limit':500,'filter[startDate]':a+'T00:00:00.000Z','filter[endDate]':b+'T23:59:59.000Z'})
    d=get(B+'?'+q)
    return (a,b,profile,d['data'] if d and d.get('code')==0 else None)
# Acordado con Golf Directo (20/11/2026): solo la lista pública de torneos, sin fichas, jugadores, resultados ni precios.
# Si su robots.txt no deja pasar a BanderinBot, no se descarga nada y se usan los torneos congelados.
if not red._reglas(B).permite(B):
    json.dump({},open('/home/claude/raw/gd/official.json','w'));print('Golf Directo: robots.txt no permite a BanderinBot; no se descarga nada');raise SystemExit(0)
start=dt.date.today()-dt.timedelta(days=45);end=dt.date.today()+dt.timedelta(days=240)
W=[];d=start
while d<=end:
    e=min(d+dt.timedelta(days=2),end);W.append((d.isoformat(),e.isoformat()));d=e+dt.timedelta(days=1)
docs={};capped=[]
with cf.ThreadPoolExecutor(4) as ex:
    for a,b,p,data in ex.map(lambda w:window(w[0],w[1],'official'),W):
        if data is None: capped.append((a,b,'ERR'));continue
        if data['totalDocs']>=500: capped.append((a,b,data['totalDocs']))
        for x in data['docs']: docs[x['_id']]=x
json.dump(docs,open('/home/claude/raw/gd/official.json','w'))
print('ventanas',len(W),'torneos',len(docs),'saturadas/errores',capped)
