OUT='banderin-reel-7-pregúntale-al-caddie.mp4'.replace('ú','u'); DUR=16.0; G='gold'
VOICE=[('89312d6c-723e-48c4-98f3-af5c1e50b5ae',.2),('a3bd4e61-a74e-4939-93bd-4787b5ef00a3',5.1),('39c8127d-0f9d-4680-8c3b-d2827d3b1c43',11.5)]
ROW=[dict(m='DOM',dd='22',n='Scramble por parejas',sub='Ejemplo · formato por equipos',tag='Para ti',cls='ok')]
def SCENES(ph,DUR): return [
 dict(type='text',t0=0,t1=3.4,y=710,size=118,stag=.15,eyebrow='Le preguntas al caddie',words=[['Hándicap',G],['24'],'/',['y'],['puntería'],'/',['dudosa.',G]],flash=True),
 dict(type='text',t0=3.4,t1=5.0,y=890,size=190,align='center',stag=.1,flash=True,words=[['Tranquilo.',G]]),
 dict(type='cards',t0=5.0,t1=6.8,y=640,eyebrow='Tu torneo',title='Este es <span class="gold">para ti.</span>',rows=ROW,gap=.2),
 dict(type='text',t0=6.8,t1=8.6,y=830,size=140,align='center',stag=.14,words=[['Scramble'],'/',['por'],['parejas.',G]],flash=True),
 dict(type='text',t0=8.6,t1=11.4,y=770,size=124,stag=.14,words=[['Si'],['fallas,'],'/',['falla',G],['tu'],'/',['compañero.',G]]),
 dict(type='end',t0=11.4,t1=DUR+1,html='Todos los <span class="gold">torneos de golf.</span>')]
