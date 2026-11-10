import json,re,sys,time,html,concurrent.futures as cf,urllib.request
OUT='/home/claude/raw/nc/'
clubs=json.load(open('/home/claude/scr/nc_clubs.json'))
codes=[('AM00','Real Federación Andaluza de Golf','Andalucia','fed'),('CM00','Real Federación de Golf de Madrid','Comunidad de Madrid','fed'),('7700','Federación de Golf de Castilla y León','Castilla y León','fed'),('CP00','Federación Canaria de Golf','Canarias','fed')]+[(c['code'],c['name'],c['hdr'],'club') for c in clubs]
MES={'ene':1,'feb':2,'mar':3,'abr':4,'may':5,'jun':6,'jul':7,'ago':8,'sep':9,'oct':10,'nov':11,'dic':12}
MESL={'enero':1,'febrero':2,'marzo':3,'abril':4,'mayo':5,'junio':6,'julio':7,'agosto':8,'septiembre':9,'octubre':10,'noviembre':11,'diciembre':12}
def get(url):
    for k in range(3):
        try:
            r=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (Banderin; contacto juan)'}),timeout=20)
            return r.read().decode('utf8','ignore')
        except Exception as e:
            time.sleep(1+k)
    return ''
def parse(code,name,region,kind):
    import os
    p=OUT+'list_'+code+'.html'
    h=open(p).read() if os.path.exists(p) else get('https://www.nextcaddy.com/competiciones-club/'+code)
    open(p,'w').write(h)
    rows=[]
    year=None
    # recorrer tokens en orden: cambioYear, cambioMes, filas
    for m in re.finditer(r'<tr class="active cambio(Mes|Year)">\s*<td[^>]*>\s*([^<]+?)\s*</td>|<tr>(.*?)</tr>',h,re.S):
        if m.group(1)=='Year':
            y=re.search(r'\d{4}',m.group(2)); year=int(y.group()) if y else year; continue
        if m.group(1)=='Mes': continue
        row=m.group(3) or ''
        a=re.search(r'href="/tour/(\d+)"[^>]*>\s*(.*?)\s*</a>',row,re.S)
        if not a: continue
        sub=re.search(r'class="sub header">\s*(.*?)\s*</div>',row,re.S)
        d=re.search(r'(\d{1,2})\s+(ene|feb|mar|abr|may|jun|jul|ago|sep|oct|nov|dic)\s+(\d{4})',row)
        vu=re.search(r'(\d+)\s+vueltas',row)
        rows.append({'id':int(a.group(1)),'n':html.unescape(re.sub(r'<[^>]+>','',a.group(2))).strip(),'club':html.unescape(re.sub(r'<[^>]+>','',sub.group(1))).strip() if sub else '',
                     'date':'%s-%02d-%02d'%(d.group(3),MES[d.group(2)],int(d.group(1))) if d else None,'vueltas':int(vu.group(1)) if vu else None,'list':code,'listname':name,'region':region,'kind':kind,'sace':'aSACE' in row,'wagr':'aWAGR' in row})
    return code,rows
res={}
with cf.ThreadPoolExecutor(6) as ex:
    for code,rows in ex.map(lambda c:parse(*c),codes):
        res[code]=rows
json.dump(res,open('/home/claude/scr/nc_lists.json','w'),ensure_ascii=False)
n=sum(len(v) for v in res.values()); ids=set(r['id'] for v in res.values() for r in v)
print('filas',n,'ids',len(ids),'listas con datos',sum(1 for v in res.values() if v))
print('sin fecha',sum(1 for v in res.values() for r in v if not r['date']));fut=set(r['id'] for v in res.values() for r in v if r['date'] and r['date']>=__import__('datetime').date.today().isoformat());print('futuros',len(fut))
