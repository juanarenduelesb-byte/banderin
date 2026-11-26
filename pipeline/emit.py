import json,datetime as dt,collections,sys,re,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from cond import conditions,plain,nextcaddy_text
from zoneinfo import ZoneInfo
MAD=ZoneInfo('Europe/Madrid')
NOW=dt.datetime.now(MAD)
TODAY=NOW.date().isoformat()
T=json.load(open('/home/claude/scr/tournaments.json'))
L={}
for row in json.load(open('/home/claude/scr/linkcheck.json')):
    L[row[0]]=row[1:]
KEEP_PAST=('n','s','e','club','prov','ccaa','cat','url','src','res')

def _loc(iso):
    try: return dt.datetime.fromisoformat(iso.replace('Z','+00:00')).astimezone(MAD).date().isoformat()
    except Exception: return None
_CTX=re.compile(r'inscripci|precio|cuota|derechos|tarifa|importe|green.?fee|participaci|coste|pago|entry|fee|cost\b|to enter|\bpris\b|price|prix|tarif|inscription|preis',re.I)
_BAD=re.compile(r'entrenam|pr[aá]ctica|buggy|carrito|moto\b|premio|comida|cena|men[uú]|almuerzo|bolas|alquiler|hotel|habitaci|trofeo|cocktail|cóctel|aperitivo|no-show|prize|fund|\bpot\b|regalo|sorteo|valorad',re.I)
def info_prices(htm):
    txt=re.sub(r'<[^>]+>',' ',htm);txt=re.sub(r'&nbsp;|\s+',' ',txt)
    out=[]
    for sent in re.split(r'(?<=[.;:!?])\s+|\n| - | • ',txt):
        if not _CTX.search(sent) or _BAD.search(sent): continue
        for m in re.finditer(r'(\d{1,3}(?:[.,]\d{1,2})?)\s*(?:€|eur(?:os)?\b)|€\s*(\d{1,3}(?:[.,]\d{1,2})?)',sent,re.I):
            v=float((m.group(1) or m.group(2)).replace(',','.'))
            if 1<=v<=400: out.append(v)
    return out
def gd_price(o,gx):
    if gx.get('en') and gx.get('op') and not o.get('op'): o['op']=_loc(gx['op'])
    if gx.get('en') and gx.get('cl') and not o.get('cl'): o['cl']=_loc(gx['cl'])
    if o.get('op') and o.get('cl') and o['op']>o['cl']: o.pop('op')
    if o.get('price') is not None: return
    if gx.get('en') and gx.get('pay') and (gx.get('pg') or 0)>0:
        o['price']=float(gx['pg']);o['priceNote']=o.get('priceNote') or 'Precio de la inscripción online'
        return
    ps=info_prices(gx.get('info') or '')
    if ps:
        o['price']=min(ps)
        o['priceNote']='Según las condiciones publicadas'+(f'; desde {min(ps):g} € hasta {max(ps):g} €' if len(set(ps))>1 else '')
        return
    if gx.get('en') and not gx.get('pay') and not o.get('insNote'): o['insNote']='Inscripción online, se paga en el club'
out=[]
for t in T:
    ok,st,s=(L.get(t['url'])+[None,None,None])[:3] if t['url'] in L else (None,None,None)
    # Solo se retira un torneo con una señal clara: cancelado, página borrada (404/410) o la web dice que no existe.
    # Si la comprobación no obtiene respuesta (caída o lentitud de la web), el torneo se mantiene.
    if s=='cancelled' or (ok is False and st in (200,404,410)): continue
    past=t['e']<TODAY
    if past:
        o={k:t[k] for k in KEEP_PAST if t.get(k) not in (None,'')}
        if s=='finished_public': o['res']=True
        o['past']=True
    else:
        o={k:v for k,v in t.items() if k not in ('gid','also','res') and v not in (None,'')}
        if t.get('price') is None: o['price']=None
        gx=(L.get(t['url'])+[None]*4)[3] if t['url'] in L else None
        if isinstance(gx,dict): gd_price(o,gx)
        txt=''
        if 'nextcaddy.com/tour/' in t['url']: txt=nextcaddy_text('/home/claude/raw/nct/'+t['url'].rsplit('/',1)[1]+'.html')
        if isinstance(gx,dict): txt+=' '+plain(gx.get('info'))
        co=conditions(txt,t.get('n',''),t.get('cat',''))
        if co: o['cond']=co
        o['ok']=TODAY if ok else None
        if s=='postponed': o['aviso']='Aplazado por el organizador'
    out.append(o)
# Golf Directo prohíbe a Banderín en su robots.txt desde el 26/11/2026. Sus torneos ya conocidos se muestran
# congelados (copia del 25/11) hasta que pase su fecha, con aviso en la ficha. No se vuelve a leer su web.
GD_CONG='2026-11-25'
_cg=os.path.join(os.path.dirname(os.path.abspath(__file__)),'datos','gd_congelado.json')
N_CG=0
if os.path.exists(_cg):
    _urls={o['url'] for o in out}
    for g in json.load(open(_cg,encoding='utf-8')):
        if (g.get('e') or g['s'])<TODAY or g['url'] in _urls: continue
        o=dict(g); o.pop('ok',None); o['cg']=GD_CONG; out.append(o); N_CG+=1
F=[
 {'nombre':'NextCaddy','desc':'Plataforma de las federaciones de Andalucía, Madrid, Castilla y León y Canarias, y de 244 clubes. Fichas con precio, plazas y plazo.','url':'https://www.nextcaddy.com/','volcada':True},
 {'nombre':'Golf Directo','desc':'Plataforma de inscripciones de clubes y federaciones. Desde el 26/11/2026 no permite que Banderín la lea: sus torneos se muestran con los datos del 25/11 y no se actualizan.','url':'https://www.golfdirecto.com/','volcada':False},
 {'nombre':'Federación de Golf de la Comunitat Valenciana','desc':'Calendario oficial con precio, plazas y plazo de inscripción.','url':'https://golfcv.com/torneo_seek/','volcada':True},
 {'nombre':'RFEG','desc':'Campeonatos de España y pruebas nacionales.','url':'https://rfegolf.es/competiciones/calendario-torneos','volcada':True},
 {'nombre':'Federación de Golf del Principado de Asturias','desc':'Calendario completo de la federación, con plazo de inscripción.','url':'https://www.fedegolfasturias.com/competiciones','volcada':True},
 {'nombre':'Federación de Golf de Castilla y León','desc':'Convocatorias propias fuera de NextCaddy.','url':'https://fgolfcyl.org/','volcada':True},
 {'nombre':'Grow Sports','desc':'Circuito propio en Madrid.','url':'https://growsportsam.com/torneos-abiertos/','volcada':True},
 {'nombre':'Corporate Golf','desc':'Circuito comercial nacional.','url':'https://www.corporategolf.es/calendariodetorneos-golf','volcada':True},
 {'nombre':'Federació Catalana de Golf','desc':'Calendario oficial de la federación y de los clubes catalanes, incluido el CatProTour.','url':'https://www.catgolf.com/es/calendario-fcgolf','volcada':True},
 {'nombre':'Federación Vasca de Golf','desc':'Calendarios de la federación vasca y de las territoriales de Álava, Bizkaia y Gipuzkoa.','url':'https://www.fvgolf.com/es/competiciones/calendario/','volcada':True},
 {'nombre':'Federación Navarra de Golf','desc':'Calendario e inscripciones de la federación navarra.','url':'https://fnavarragolf.com/calendario-inscripciones/','volcada':True},
 {'nombre':'Federación Riojana de Golf','desc':'Calendario anual oficial (circular en PDF).','url':'https://frgolf.es/calendario','volcada':True},
 {'nombre':'Federación Cántabra de Golf','desc':'Calendario de competiciones de la federación cántabra.','url':'https://federacioncantabradegolf.com/calendario/','volcada':True},
 {'nombre':'Federación de Golf de la Región de Murcia','desc':'Calendario oficial de la federación murciana.','url':'https://fgolfmurcia.com/torneos/','volcada':True},
 {'nombre':'Federación de Golf de Castilla-La Mancha','desc':'Calendario oficial, la inscripción se hace en su app.','url':'https://fedgolfclm.com/inscripciones-y-resultados-torneos-fed-castilla-la-mancha/','volcada':True},
 {'nombre':'Clubes con otras plataformas','desc':'Golfmanager, iMaster o TeeOne, y clubes que solo publican en su web.','url':'https://rfegolf.es/jugar-golf/clubes-golf-espana','volcada':False},
 {'nombre':'Circuitos privados','desc':'Circuitos de asociaciones con inscripción solo para socios, como AESGOLF.','url':'https://www.aesgolf.com/','volcada':False}]
# ---------- Torneos por fuente (incluye los que también publica otra fuente) ----------
DOM={'nextcaddy.com':'NextCaddy','golfdirecto.com':'Golf Directo','golfcv.com':'Federación de Golf de la Comunitat Valenciana','rfegolf.es':'RFEG',
 'fedegolfasturias.com':'Federación de Golf del Principado de Asturias','catgolf.com':'Federació Catalana de Golf','fvgolf.com':'Federación Vasca de Golf',
 'fnavarragolf.com':'Federación Navarra de Golf','frgolf.es':'Federación Riojana de Golf','federacioncantabradegolf.com':'Federación Cántabra de Golf',
 'fedgolfclm.com':'Federación de Golf de Castilla-La Mancha','fgolfmurcia.com':'Federación de Golf de la Región de Murcia','fgolfcyl.org':'Federación de Golf de Castilla y León'}
PER=collections.Counter()
for t in T:
    if t['e']<TODAY: continue
    if t['url'] not in {o['url'] for o in out if not o.get('past')} and not any(o['url']==t['url'] for o in out): continue
    ss={t['src']}
    for u in t.get('also',[]):
        for d,nm in DOM.items():
            if d in u: ss.add(nm)
    for x in ss: PER[x]+=1
for f in F: f['n']=PER.get(f['nombre'],0)+(N_CG if f['nombre']=='Golf Directo' else 0)
# ---------- Cambios frente a la revisión anterior ----------
def load_prev(path):
    if not path or not os.path.exists(path): return [],[]
    src=open(path,encoding='utf-8').read()
    def grab(name):
        m=re.search(r'window\.'+name+r'=(.*?);\n(?=window\.|$)',src,re.S)
        if not m: return []
        try: return json.loads(m.group(1))
        except Exception: return []
    return grab('TORNEOS'),grab('CAMBIOS')
prevT,prevC=load_prev(sys.argv[2] if len(sys.argv)>2 else None)
cur={o['url']:o for o in out}
nuevos=[]
if prevT:
    for o in prevT:
        if o.get('past') or o['s']<TODAY: continue
        n=cur.get(o['url'])
        base={'d':TODAY,'n':o['n'],'club':o.get('club'),'url':o['url'],'s':o['s']}
        if n is None:
            dead=L.get(o['url'])
            k='cancelado' if (dead and dead[2]=='cancelled') or re.search(r'cancelad|suspendid|anulad',o['n'],re.I) else 'retirado'
            nuevos.append({**base,'k':k})
        else:
            if n['s']!=o['s']: nuevos.append({**base,'k':'fecha','a':o['s'],'b':n['s']})
            if re.search(r'cancelad|suspendid|anulad',n['n'],re.I) and not re.search(r'cancelad|suspendid|anulad',o['n'],re.I): nuevos.append({**base,'k':'cancelado'})
            if n.get('op') and n['op']<=TODAY and o.get('op') and o['op']>TODAY: nuevos.append({**base,'k':'abre'})
            if o.get('cl') and n.get('cl') and n['cl']!=o['cl']: nuevos.append({**base,'k':'plazo','a':o['cl'],'b':n['cl']})
    prev_urls={o['url'] for o in prevT}
    alta=sum(1 for o in out if not o.get('past') and o['url'] not in prev_urls)
    if alta: nuevos.append({'d':TODAY,'k':'nuevos','c':alta})
limite=(NOW.date()-dt.timedelta(days=14)).isoformat()
CAMBIOS=[c for c in prevC if c.get('d','')>=limite and c.get('d')!=TODAY]+nuevos
CAMBIOS.sort(key=lambda c:c['d'],reverse=True)

# ---------- Cobertura por comunidad ----------
FED={
 'Andalucía':('completo','Real Federación Andaluza de Golf, en NextCaddy'),
 'Comunidad de Madrid':('completo','Federación de Golf de Madrid, en NextCaddy'),
 'Castilla y León':('completo','Federación de Castilla y León, en NextCaddy y su web'),
 'Canarias':('completo','Federación Canaria, en NextCaddy'),
 'Comunitat Valenciana':('completo','Federación de la Comunitat Valenciana, calendario oficial'),
 'Cataluña':('completo','Federació Catalana: su calendario oficial, con las pruebas de clubes'),
 'País Vasco':('completo','Federación Vasca y territoriales: sus calendarios oficiales'),
 'Comunidad Foral de Navarra':('completo','Federación Navarra: su calendario de inscripciones'),
 'La Rioja':('completo','Federación Riojana: su calendario anual oficial'),
 'Cantabria':('completo','Federación Cántabra: su calendario oficial'),
 'Castilla-La Mancha':('completo','Federación de Castilla-La Mancha: su calendario oficial'),
 'Principado de Asturias':('completo','Federación de Asturias: su calendario de competiciones'),
 'Galicia':('parcial','Federación Gallega: su listado de torneos. Las fichas de Golf Directo, congeladas a 25/11'),
 'Aragón':('parcial','Federación Aragonesa: sus fichas de torneo. Las de Golf Directo, congeladas a 25/11'),
 'Illes Balears':('parcial','Federación Balear: publica en Golf Directo, que no permite a Banderín leerlo. Datos congelados a 25/11'),
 'Extremadura':('parcial','Federación Extremeña: publica en Golf Directo, que no permite a Banderín leerlo. Datos congelados a 25/11'),
 'Región de Murcia':('completo','Federación de la Región de Murcia: su calendario oficial'),
 'Melilla':('parcial','Clubes en Golf Directo (datos congelados a 25/11); la web de la federación no permite la lectura automática'),
}
cnt=collections.Counter(o['ccaa'] for o in out if not o.get('past'))
srcs=collections.defaultdict(collections.Counter)
for o in out:
    if not o.get('past'): srcs[o['ccaa']][o['src']]+=1
COB=[]
for cc,(estado,nota) in FED.items():
    COB.append({'ccaa':cc,'n':cnt.get(cc,0),'estado':estado,'nota':nota,'fuentes':[k for k,_ in srcs[cc].most_common()]})
COB.sort(key=lambda x:-x['n'])

p=sys.argv[1] if len(sys.argv)>1 else '/home/claude/torneos/data.js'
with open(p,'w') as f:
    f.write('window.ACTUALIZADO="%s";\nwindow.REVISION="%s";\nwindow.FUENTES=%s;\nwindow.COBERTURA=%s;\nwindow.CAMBIOS=%s;\nwindow.TORNEOS=[\n%s\n];\n'%(
        TODAY,NOW.strftime('%Y-%m-%dT%H:%M'),json.dumps(F,ensure_ascii=False,indent=1),json.dumps(COB,ensure_ascii=False),json.dumps(CAMBIOS,ensure_ascii=False),
        ',\n'.join(json.dumps(o,ensure_ascii=False) for o in out if not o.get('past'))))
pp=os.path.join(os.path.dirname(p),'pasados.js')
with open(pp,'w') as f:
    PA=sorted((o for o in out if o.get('past')),key=lambda o:o['s'],reverse=True)
    for o in PA: o.pop('past',None)
    f.write('window.PASADOS=[\n%s\n];\n'%',\n'.join(json.dumps(o,ensure_ascii=False,separators=(',',':')) for o in PA))
print('escritos',len(out),'próximos',sum(1 for o in out if not o.get('url') in {x['url'] for x in PA}),'pasados',len(PA),'con resultados',sum(1 for o in out if o.get('res')),'cambios hoy',len(nuevos),'bytes',os.path.getsize(p),'pasados.js',os.path.getsize(pp))
