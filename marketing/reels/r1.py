OUT='banderin-reel-1-el-que-nunca-se-entera.mp4'; DUR=14.0; G='gold'
VOICE=[('0e277fda-d881-47b3-bad5-5b6fe1728a8b',.2),('d80ddde7-b5d3-4adb-bb6c-09072a07be44',2.9),('9c775de3-21c7-49c1-a170-b32e757e02cc',6.5),('1f3e74ac-1f0d-4590-a162-70a8f29dae9b',8.5)]
def SCENES(ph,DUR): return [
 dict(type='text',t0=0,t1=2.8,y=750,size=108,stag=.12,eyebrow='Sábado, 9:41',words=[['¿Cómo'],['que'],['cerró',G],['ayer'],'/',['la'],['inscripción?',G]],flash=True),
 dict(type='text',t0=2.8,t1=4.0,y=890,size=190,align='center',stag=.1,flash=True,words=[['Te'],['lo'],'/',['dije.',G]]),
 dict(type='text',t0=4.0,t1=6.4,y=790,size=116,stag=.14,words=[['Tienes'],['banderín'],'/',['y'],['no'],['lo',G],['abres.',G]]),
 dict(type='notifs',t0=6.4,t1=8.5,y=750,items=[['ahora','Se abre la inscripción','Torneo de ejemplo · Sábado 21'],['ahora','Plazas limitadas','Avisos de Banderín · gratis']]),
 dict(type='text',t0=8.5,t1=10.6,y=890,size=170,align='center',stag=.14,flash=True,words=[['Avisos'],'/',['gratis.',G]]),
 dict(type='end',t0=10.6,t1=DUR+1,html='Que no se te <span class="gold">escape otro.</span>')]
