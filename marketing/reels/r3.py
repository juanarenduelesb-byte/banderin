OUT='banderin-reel-3-por-que-ellos-si-juegan.mp4'; DUR=19.5; G='gold'
VOICE=[('da0c6eae-3af2-4052-8f42-07d0e0c3f5f4',.2),('60ba7dfd-ae8c-4db4-9820-6031aa3e2d2e',4.7),('6be2b48b-8de3-4096-ab13-6efd994f95de',8.4),('91e4ed04-bc2a-40db-8c7e-19d11f3cc04b',11.7),('5e729884-2633-435d-bbfe-b99f735d110d',15.2)]
E='Perfil de ejemplo'
def SCENES(ph,DUR): return [
 dict(type='text',t0=0,t1=4.6,y=730,size=112,stag=.15,eyebrow=E+' · Jugador veterano',words=[['«Llevo'],['40',G],['años',G],['jugando.'],'/',['Los'],['torneos'],['son'],['mi'],['domingo.»',G]]),
 dict(type='text',t0=4.6,t1=8.3,y=730,size=118,stag=.14,eyebrow=E+' · Jugador joven',words=[['«Tengo'],['19',G],['años'],['y'],'/',['quiero'],['competir',G],['ya.»',G]]),
 dict(type='text',t0=8.3,t1=11.6,y=730,size=118,stag=.14,eyebrow=E+' · Padre e hijo',words=[['«Mi'],['hijo'],['y'],['yo'],'/',['jugamos'],['uno',G],['cada'],['mes.»',G]]),
 dict(type='text',t0=11.6,t1=15.1,y=690,size=108,stag=.13,eyebrow=E+' · Recién llegado',words=[['«Llegué'],['de'],['fuera'],['y'],'/',['encontré'],['mi'],['club',G],['en'],['un'],['torneo.»',G]]),
 dict(type='end',t0=15.1,t1=DUR+1,html='Todos los <span class="gold">torneos de España.</span>')]
