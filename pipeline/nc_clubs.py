import re,json,urllib.request
h=urllib.request.urlopen(urllib.request.Request('https://www.nextcaddy.com/provincias/28',headers={'User-Agent':'Mozilla/5.0 (Banderin)'}),timeout=40).read().decode('utf8','ignore')
h=re.sub(r'<svg.*?</svg>','',h,flags=re.S)
parts=re.split(r'(<h\d[^>]*>.*?</h\d>)',h,flags=re.S);cur=None;clubs=[]
for p in parts:
    if re.match(r'<h\d',p): cur=re.sub(r'<[^>]+>|\s+',' ',p).strip();continue
    for code,txt in re.findall(r'href="/club/([A-Z0-9]+)"[^>]*>(.*?)</a>',p,re.S):
        x=[s.strip() for s in re.sub(r'<[^>]+>',' | ',txt).split('|') if s.strip()]
        clubs.append({'code':code,'name':x[0] if x else '','city':x[1] if len(x)>1 else '','hdr':cur})
assert len(clubs)>100, 'Lista de clubes NextCaddy sospechosamente corta'
json.dump(clubs,open('/home/claude/scr/nc_clubs.json','w'),ensure_ascii=False);print('clubes NextCaddy',len(clubs))
