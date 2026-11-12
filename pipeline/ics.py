# Lector mínimo de calendarios iCalendar públicos (Google Calendar)
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import red  # BanderinBot: robots.txt, pausa e identificación
import re,urllib.request,time,datetime as dt
def fetch(url):
    for k in range(3):
        try: return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (Banderin)'}),timeout=40).read().decode('utf8','ignore')
        except Exception: time.sleep(2+k)
    return ''
def unfold(s): return re.sub(r'\r?\n[ \t]','',s)
def val(v): return v.replace('\\,',',').replace('\\;',';').replace('\\n','\n').replace('\\N','\n').strip()
def parse(txt):
    txt=unfold(txt);out=[]
    cal=(re.search(r'X-WR-CALNAME:(.*)',txt) or [None,''])[1].strip()
    for b in re.findall(r'BEGIN:VEVENT(.*?)END:VEVENT',txt,re.S):
        e={}
        for line in b.strip().splitlines():
            if ':' not in line: continue
            k,v=line.split(':',1);name=k.split(';')[0]
            e[name]=v
            if name in('DTSTART','DTEND'): e[name+'_date']='VALUE=DATE' in k or len(v)==8
        def d(x):
            v=e.get(x)
            if not v: return None
            return f'{v[:4]}-{v[4:6]}-{v[6:8]}'
        s=d('DTSTART');en=d('DTEND')
        if not s: continue
        if en and e.get('DTEND_date'):
            en=(dt.date.fromisoformat(en)-dt.timedelta(days=1)).isoformat()
        en=max(en or s,s)
        out.append({'cal':cal,'uid':e.get('UID'),'n':val(e.get('SUMMARY','')),'s':s,'e':en,'loc':val(e.get('LOCATION','')),'desc':val(e.get('DESCRIPTION','')),'status':e.get('STATUS',''),'rrule':e.get('RRULE')})
    return cal,out
