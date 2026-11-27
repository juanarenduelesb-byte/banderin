OUT='banderin-reel-4-cuenta-atras.mp4'; DUR=13.0; G='gold'
VOICE=[('f3a00fd0-85db-4429-8c03-9c14c7eeb7f4',.2),('f451f834-bceb-4428-ad18-bed4d7c11c4e',2.9),('6b6483ba-7db1-4d7d-b095-461fd776c373',5.8)]
def SCENES(ph,DUR): return [
 dict(type='text',t0=0,t1=2.8,y=750,size=124,stag=.13,eyebrow='Cierre de inscripción',words=[['Se'],['cierra'],['en'],'/',['dos',G],['minutos.',G]],flash=True),
 dict(type='notifs',t0=2.8,t1=4.4,y=830,items=[['ahora','Última hora','Quedan 2 minutos · Torneo de ejemplo']]),
 dict(type='text',t0=4.4,t1=5.8,y=890,size=170,align='center',stag=.14,flash=True,words=[['Un'],['toque.'],'/',['Solo'],['uno.',G]]),
 dict(type='text',t0=5.8,t1=7.0,y=890,size=230,align='center',stag=.1,flash=True,words=[['Dentro.',G]]),
 dict(type='text',t0=7.0,t1=9.0,y=830,size=130,align='center',stag=.14,words=[['Nos'],['vemos'],['en'],'/',['la'],['salida.',G]]),
 dict(type='end',t0=9.0,t1=DUR+1,html='Que no se cierre <span class="gold">sin ti.</span>')]
