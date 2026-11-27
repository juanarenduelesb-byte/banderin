import sys,subprocess,os
from playwright.sync_api import sync_playwright
INIT="localStorage.setItem('banderin.consent',JSON.stringify({v:1,pref:true,ts:Date.now()}));localStorage.setItem('banderin.avpop',JSON.stringify(Date.now()));localStorage.setItem('banderin.sincuenta','1');localStorage.setItem('banderin.tema',JSON.stringify('light'))"
rid=sys.argv[1];mode=sys.argv[2]
with sync_playwright() as p:
    b=p.chromium.launch(); c=b.new_context(viewport={'width':1080,'height':1920},color_scheme='light',geolocation={'latitude':40.4168,'longitude':-3.7038},permissions=['geolocation']); c.add_init_script(INIT)
    pg=c.new_page(); pg.goto(f'http://127.0.0.1:8772/_r/'+os.environ.get('PAGE','engine')+f'.html?r={rid}',timeout=120000); pg.wait_for_timeout(4000); pg.evaluate('prep()'); pg.wait_for_timeout(400)
    if mode=='stills':
        for t in [float(x) for x in sys.argv[3:]]:
            pg.evaluate(f'render({max(0,t-0.6)})')
            for k in range(6): w=pg.evaluate(f'render({max(0,t-0.5+k*0.1)})'); pg.wait_for_timeout(max(40,w or 0))
            pg.screenshot(path=f'/home/claude/reels/st_{rid}_{t:05.2f}.jpg',type='jpeg',quality=80)
    else:
        a,bq,out=float(sys.argv[2]),float(sys.argv[3]),sys.argv[4]; tmp=out.replace('.mp4','.tmp.mp4')
        ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate','30','-c:v','mjpeg','-i','-','-c:v','libx264','-crf','18','-preset','veryfast','-pix_fmt','yuv420p','-r','30',tmp],stdin=subprocess.PIPE)
        for k in range(8):
            w=pg.evaluate(f'render({max(0,a-0.8+k*0.1)})')
            if w: pg.wait_for_timeout(w)
        for n in range(round(a*30),round(bq*30)):
            w=pg.evaluate(f'render({n/30})')
            if w: pg.wait_for_timeout(w)
            ff.stdin.write(pg.screenshot(type='jpeg',quality=92))
        ff.stdin.close()
        if ff.wait()==0: os.rename(tmp,out); print('ok',out)
    b.close()
