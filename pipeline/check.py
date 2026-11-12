import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import red  # BanderinBot: robots.txt, pausa e identificación
import json,urllib.request,concurrent.futures as cf,os,time,collections
T=json.load(open('/home/claude/scr/tournaments.json'))
UA={'User-Agent':'Mozilla/5.0 (Banderin link check)'}
def http(u,api=False):
    for k in range(3):
        try:
            r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=25)
            b=r.read(200000)
            return r.status,b
        except urllib.error.HTTPError as e: return e.code,b''
        except Exception as e: time.sleep(1+k)
    return 0,b''
def check(t):
    if t.get('gid'):
        st,b=http(f"https://www.golfdirecto.com/api/v2/public/game/{t['gid']}/active")
        ok=False;status=None
        if st==200:
            try:
                d=json.loads(b);ok=d.get('code')==0;dd=d.get('data') or {};status=dd.get('status')
                if status=='finished' and (dd.get('privacy') or {}).get('publicResults') and (dd.get('__playersCount') or 0)>0: status='finished_public'
                bk=dd.get('booking') or {}
                info=((dd.get('microsite') or {}).get('information') or '')[:6000]
                extra={'en':bool(bk.get('isEnabled')),'pay':bool(bk.get('isPaymentEnabled')),'pg':bk.get('priceForGeneral'),
                       'op':bk.get('startDate'),'cl':bk.get('endDate'),'info':info}
                return t['url'],ok,st,status,extra
            except Exception: pass
        return t['url'],ok,st,status
    if 'nextcaddy.com/tour/' in t['url']:
        p='/home/claude/raw/nct/'+t['url'].rsplit('/',1)[1]+'.html'
        if os.path.exists(p) and os.path.getsize(p)>20000 and 'NextCaddy' in open(p).read(3000): return t['url'],True,200,None
    st,b=http(t['url'])
    txt=b.decode('utf8','ignore').lower()
    ok=st==200 and not ('page not found' in txt or 'no encontrad' in txt[:5000] or 'error 404' in txt)
    return t['url'],ok,st,None
with cf.ThreadPoolExecutor(8) as ex: R=list(ex.map(check,T))
json.dump(R,open('/home/claude/scr/linkcheck.json','w'))
c=collections.Counter((r[1],r[2],r[3]) for r in R)
print(c.most_common(12))
for r in R:
    if not r[1]: print('FALLO',r[2],r[0])
