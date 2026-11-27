OUT='banderin-reel-5-golf-a-lo-mapa.mp4'; DUR=12.0; G='gold'
VOICE=[('efc8727b-b12b-498a-9dbb-ad715df5a8b3',.1),('959dd03a-1f30-4956-b760-0561951fff06',3.1),('135e7bdd-6af0-44fa-99d3-bb7f9725d46c',5.7)]
def SCENES(ph,DUR): return [
 dict(type='counter',t0=0,t1=3.0,to=1049,dur=1.2,eyebrow='Golf a lo mapa',label='<span class="gold">torneos.</span>',y=300,map=dict(x=40,y=780,s=1.0,o=.9,wave=.9),flash=True),
 dict(type='counter',t0=3.0,t1=5.6,to=17,dur=1.0,eyebrow='Cada punto, un torneo',label='<span class="gold">comunidades.</span>',y=300,map=dict(x=40,y=780,s=1.0,o=.9,wave=0)),
 dict(type='text',t0=5.6,t1=8.4,y=810,size=150,align='center',stag=.15,flash=True,words=[['Un'],['solo'],'/',['sitio.',G]],map=dict(x=40,y=1000,s=.85,o=.4,wave=0)),
 dict(type='end',t0=8.4,t1=DUR+1,html='Todos los torneos, <span class="gold">en un mapa.</span>')]
