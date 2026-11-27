OUT='banderin-reel-2-la-carta-del-torneo.mp4'; DUR=15.0; G='gold'
VOICE=[('1932bc56-042e-40bf-a0e1-4068243968c0',.2),('f2bcf3de-10b6-4ea6-afdb-9c1b601df2af',2.9),('69eb37fb-9998-49cb-ae1d-41ec9023fa65',11.4)]
ROWS=[dict(m='SÁB',dd='14',n='Torneo Mid-Amateur Femenino',sub='Barberán y Collar · Madrid',tag='Ejemplo',cls='ok'),
 dict(m='DOM',dd='15',n='Copa RFGM Costa del Sol',sub='Olivar de la Hinojosa · Madrid',tag='Ejemplo',cls='ok'),
 dict(m='SÁB',dd='14',n='Absoluto de Pitch & Putt',sub='Montepríncipe · Boadilla del Monte',tag='Ejemplo',cls='ok'),
 dict(m='DOM',dd='15',n='Parejas Greensome Chapman',sub='Club de Golf Aranjuez',tag='Ejemplo',cls='ok')]
def SCENES(ph,DUR): return [
 dict(type='text',t0=0,t1=2.8,y=830,size=132,stag=.12,words=[['Hay'],['un'],['campo',G],'/',['esperándote.',G]],flash=True),
 dict(type='counter',t0=2.8,t1=6.6,to=1049,dur=1.3,eyebrow='Toda España',label='torneos. <span class="gold">Uno es tuyo.</span>',y=330,map=dict(x=40,y=840,s=.95,o=.8,wave=.9),flash=True),
 dict(type='cards',t0=6.6,t1=10.2,y=480,eyebrow='La carta de hoy',title='Elige el <span class="gold">tuyo.</span>',rows=ROWS,gap=.3),
 dict(type='text',t0=10.2,t1=11.4,y=890,size=150,align='center',stag=.12,words=[['Gratis.',G]]),
 dict(type='end',t0=11.4,t1=DUR+1,html='Encuentra tu <span class="gold">próximo torneo.</span>')]
