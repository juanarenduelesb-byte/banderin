import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import red  # BanderinBot: robots.txt, pausa e identificación
import re,html,json,time,urllib.request,concurrent.futures as cf,os
def get(u):
    for k in range(3):
        try: return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 (Banderin)'}),timeout=40).read().decode('utf8','ignore')
        except Exception: time.sleep(2+k)
    return ''
def page(n):
    p=f'/home/claude/raw/rfegc/p{n}.html'
    if os.path.exists(p): return open(p).read()
    h=get(f'https://rfegolf.es/jugar-golf/clubes-golf-espana/?e-page-2f94730={n}&eqf_seed=83070');open(p,'w').write(h);return h
def items(h):
    out=[]
    for blk in re.split(r'data-elementor-type="loop-item"',h)[1:]:
        slug=re.search(r'href="https://rfegolf.es/club/([^"]+)"',blk)
        texts=[html.unescape(re.sub(r'\s+',' ',t)).strip() for t in re.findall(r'<(?:h\d|span)[^>]*class="[^"]*(?:elementor-heading-title|elementor-icon-list-text)[^"]*"[^>]*>(.*?)</(?:h\d|span)>',blk,re.S)]
        texts=[re.sub(r'<[^>]+>','',t).strip() for t in texts if t]
        if slug: out.append({'slug':slug.group(1),'t':texts})
    return out
with cf.ThreadPoolExecutor(4) as ex: pages=list(ex.map(page,range(1,49)))
allc={}
for h in pages:
    for it in items(h): allc[it['slug']]=it
json.dump(allc,open('/home/claude/scr/rfeg_clubs.json','w'),ensure_ascii=False)
print(len(allc));import itertools
for v in itertools.islice(allc.values(),6): print(v)
