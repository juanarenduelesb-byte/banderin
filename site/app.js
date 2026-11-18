'use strict';
const PASV=(document.currentScript&&document.currentScript.dataset.pasados)||'';
const T=(window.TORNEOS||[]).map(t=>Object.assign({},t)),SRC=window.FUENTES||[];
const LANG=window.LANG||'es',LOC=LANG==='en'?'en-GB':'es-ES';
const L=(s,o)=>{let r=LANG==='en'&&window.EN&&window.EN[s]!=null?window.EN[s]:s;if(o)for(const k in o)r=r.split('{'+k+'}').join(o[k]);return r};
const V=v=>LANG!=="en"?v:window.VOC&&window.VOC[v]!=null?window.VOC[v]:window.EN&&window.EN[v]!=null?window.EN[v]:v;
const $=id=>document.getElementById(id);
const pad=n=>String(n).padStart(2,'0');
const iso=d=>d.getFullYear()+'-'+pad(d.getMonth()+1)+'-'+pad(d.getDate());
const now=new Date();const TODAY=iso(now);
const D=s=>{const[a,b,c]=s.split('-').map(Number);return new Date(a,b-1,c)};
const add=(s,n)=>{const d=D(s);d.setDate(d.getDate()+n);return iso(d)};
const fDay=s=>D(s).toLocaleDateString(LOC,{weekday:'long',day:'numeric',month:'long',year:D(s).getFullYear()!==now.getFullYear()?'numeric':undefined});
const fShort=s=>D(s).toLocaleDateString(LOC,{day:'numeric',month:'short'}).replace('.','');
const fWk=s=>D(s).toLocaleDateString(LOC,{weekday:'short',day:'numeric',month:'short'}).replace(/\./g,'');
const eur=p=>{if(p===0)return L('Gratis');if(p==null)return L('En la web');const n=p.toLocaleString(LOC,{minimumFractionDigits:p%1?2:0,maximumFractionDigits:2});return LANG==='en'?'€'+n:n+' €'};
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
// Solo enlaces web: cualquier otro esquema (javascript:, data:…) se descarta
const safeUrl=u=>{try{const x=new URL(String(u||''));return x.protocol==='https:'||x.protocol==='http:'?x.href:'#'}catch(e){return '#'}};
const PREF_KEYS=['tema','city','radius','saved','played'],MEM={};
const raw={get(k){try{const v=localStorage.getItem('banderin.'+k);return v==null?null:JSON.parse(v)}catch(e){return null}},set(k,v){try{localStorage.setItem('banderin.'+k,JSON.stringify(v))}catch(e){}},del(k){try{localStorage.removeItem('banderin.'+k)}catch(e){}}};
const consent={get(){const c=raw.get('consent');if(!c||!c.ts||Date.now()-c.ts>365*864e5)return null;return c},pref(){const c=consent.get();return!!(c&&c.pref)}};
const store={get(k,d){if(k in MEM)return MEM[k];if(!consent.pref())return d;const v=raw.get(k);return v==null?d:v},set(k,v){MEM[k]=v;if(consent.pref())raw.set(k,v)}};

const I={share:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12M7.5 7.5 12 3l4.5 4.5"/><path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7"/></svg>',
 flag:c=>'<svg class="fl '+c+'" viewBox="0 0 16 16" aria-hidden="true"><path d="M4 1.5v13" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" fill="none"/><path d="M5 2l8 3-8 3z" fill="currentColor"/></svg>',
 star:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2L12 17.3 6.4 20.2l1.1-6.2L3 9.6l6.2-.9z"/></svg>',
 starS:'<svg class="sv" viewBox="0 0 24 24" fill="currentColor" role="img" aria-label="Guardado"><path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1.1 6.2L12 17.3 6.4 20.2l1.1-6.2L3 9.6l6.2-.9z"/></svg>',
 cal:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15" rx="3"/><path d="M8 3v4M16 3v4M3.5 10h17M12 13v5M9.5 15.5h5"/></svg>',
 out:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 16 16 8M9 8h7v7"/></svg>',
 x:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>',
 clock:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="8"/><path d="M12 8v4l3 2"/></svg>'
};

// Coordenadas aproximadas por municipio y capitales de provincia
const PROV=[['A Coruña','A Coruña',43.362,-8.411],['Albacete','Albacete',38.994,-1.858],['Alicante','Alicante',38.345,-0.481],['Almería','Almería',36.834,-2.464],['Ávila','Ávila',40.656,-4.700],['Badajoz','Badajoz',38.879,-6.970],['Barcelona','Barcelona',41.385,2.173],['Bilbao','Bizkaia',43.263,-2.935],['Burgos','Burgos',42.344,-3.697],['Cáceres','Cáceres',39.475,-6.372],['Cádiz','Cádiz',36.527,-6.288],['Castellón de la Plana','Castellón',39.986,-0.051],['Ceuta','Ceuta',35.889,-5.321],['Ciudad Real','Ciudad Real',38.985,-3.927],['Córdoba','Córdoba',37.888,-4.779],['Cuenca','Cuenca',40.070,-2.137],['Girona','Girona',41.979,2.821],['Granada','Granada',37.177,-3.599],['Guadalajara','Guadalajara',40.633,-3.167],['Huelva','Huelva',37.261,-6.945],['Huesca','Huesca',42.136,-0.408],['Jaén','Jaén',37.779,-3.784],['Las Palmas de Gran Canaria','Las Palmas',28.124,-15.430],['León','León',42.599,-5.567],['Lleida','Lleida',41.617,0.620],['Logroño','La Rioja',42.465,-2.445],['Lugo','Lugo',43.012,-7.556],['Madrid','Madrid',40.417,-3.704],['Málaga','Málaga',36.721,-4.421],['Melilla','Melilla',35.292,-2.938],['Murcia','Murcia',37.992,-1.131],['Ourense','Ourense',42.336,-7.864],['Oviedo','Asturias',43.362,-5.849],['Palencia','Palencia',42.010,-4.533],['Palma','Illes Balears',39.570,2.650],['Pamplona','Navarra',42.812,-1.646],['Pontevedra','Pontevedra',42.431,-8.645],['Salamanca','Salamanca',40.970,-5.664],['San Sebastián','Gipuzkoa',43.318,-1.981],['Santa Cruz de Tenerife','Santa Cruz de Tenerife',28.464,-16.251],['Santander','Cantabria',43.462,-3.810],['Segovia','Segovia',40.948,-4.118],['Sevilla','Sevilla',37.389,-5.984],['Soria','Soria',41.764,-2.465],['Tarragona','Tarragona',41.119,1.245],['Teruel','Teruel',40.344,-1.106],['Toledo','Toledo',39.863,-4.027],['Valencia','Valencia',39.470,-0.376],['Valladolid','Valladolid',41.652,-4.724],['Vigo','Pontevedra',42.240,-8.720],['Vitoria-Gasteiz','Álava',42.847,-2.672],['Zamora','Zamora',41.503,-5.745],['Zaragoza','Zaragoza',41.649,-0.889]];
const PC={};PROV.forEach(p=>{if(!PC[p[1]])PC[p[1]]=[p[2],p[3]]});
const CITY={'Alalpardo':[40.640,-3.520],'Alcalá de Henares':[40.482,-3.364],'Alcobendas':[40.547,-3.642],'Alcázar de San Juan':[39.390,-3.208],'Alhaurín de la Torre':[36.661,-4.561],'Alhaurín el Grande':[36.642,-4.687],'Aljaraque':[37.270,-7.023],'Almería':[36.834,-2.464],'Aranjuez':[40.033,-3.604],'Benalmádena':[36.599,-4.517],'Boadilla del Monte':[40.405,-3.877],'Borriol':[40.043,-0.070],'Buenavista del Norte':[28.374,-16.861],'Bétera':[39.591,-0.462],'Carcaixent':[39.122,-0.448],'Cartagena':[37.606,-0.986],'Chiclana de la Frontera':[36.419,-6.149],'Chiva':[39.468,-0.718],'Illescas':[40.122,-3.848],'Islantilla':[37.208,-7.226],'Jerez de la Frontera':[36.686,-6.137],'Las Gabias':[37.135,-3.670],'Llucmajor':[39.490,2.891],'Madrid':[40.417,-3.704],'Manises':[39.493,-0.463],'Marbella':[36.510,-4.883],'Mijas':[36.596,-4.637],'Málaga':[36.721,-4.421],'Oliva':[38.920,-0.120],'Picassent':[39.363,-0.459],'Puerto Real':[36.528,-6.190],'San Lorenzo de El Escorial':[40.591,-4.147],'San Miguel de Abona':[28.098,-16.617],'San Pedro de Rozados':[40.791,-5.738],'San Roque':[36.211,-5.385],'Sevilla':[37.389,-5.984],'Siero':[43.390,-5.660],'Teguise':[29.061,-13.560],'Torrejón de Ardoz':[40.456,-3.479],'Torremolinos':[36.622,-4.500],'Valencia':[39.470,-0.376],'Vera':[37.243,-1.859],'Villalbilla':[40.430,-3.299],'Villanueva de la Cañada':[40.446,-4.004]};
function hav(a,b){const R=6371,r=x=>x*Math.PI/180;const dl=r(b[0]-a[0]),dn=r(b[1]-a[1]);const h=Math.sin(dl/2)**2+Math.cos(r(a[0]))*Math.cos(r(b[0]))*Math.sin(dn/2)**2;return 2*R*Math.asin(Math.sqrt(h))}

function rng(seed){return()=>{seed=(seed*16807)%2147483647;return(seed-1)/2147483646}}
function blob(cx,cy,r,ph,amp,k){let d='';const N=64;for(let i=0;i<=N;i++){const a=i/N*Math.PI*2;const rr=r*(1+amp*Math.sin(3*a+ph)+amp*.6*Math.sin(5*a+ph*1.7)+amp*.3*Math.cos(2*a+ph*.5));d+=(i?'L':'M')+(cx+Math.cos(a)*rr*k).toFixed(1)+' '+(cy+Math.sin(a)*rr).toFixed(1)}return d+'Z'}
function topo(cx,cy,rings,step,seed,k){const r=rng(seed);const ph=r()*6;let s='';for(let i=1;i<=rings;i++)s+='<path class="ring'+(i%4===0?' hi':'')+'" d="'+blob(cx,cy,i*step,ph+i*.12,.07+r()*.03,k)+'"/>';return s}
$('bgTopo').innerHTML=topo(1250,180,22,34,7,1.25)+topo(180,860,18,30,19,1.1);
function hash(s){let h=7;for(const c of s)h=(h*31+c.charCodeAt(0))%2147483647;return h||1}
function greenSvg(seed){const r=rng(seed);const cx=230+r()*140,cy=60+r()*20;return '<svg viewBox="0 0 400 118" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><path class="green" d="'+blob(cx,cy,48,r()*6,.06,1.4)+'"/><path class="bunker" d="'+blob(cx-90,cy+38,14,r()*6,.12,1.6)+'"/>'+topo(cx,cy,12,8,seed,1.4)+'<ellipse class="hole" cx="'+(cx+12)+'" cy="'+(cy+4)+'" rx="4" ry="2"/><path class="pole" d="M'+(cx+12)+' '+(cy+4)+'V'+(cy-34)+'"/><path class="cloth" d="M'+(cx+13)+' '+(cy-33)+'l17 6-17 6z"/></svg>'}

function status(t){
  if(t.e<TODAY)return['done',L('Finalizado'),L('Finalizado')];
  if(t.st==='C'||(t.cl&&TODAY>t.cl))return['closed',L('Inscripción cerrada'),L('Cerrada')];
  if(t.op&&t.op>=t.s)return['ask',L('Consultar inscripción'),L('Consultar')];
  if(t.op&&TODAY<t.op)return['soon',L('Abre el {d}',{d:fShort(t.op)}),L('Abre {d}',{d:fShort(t.op)})];
  if(t.cl)return['open',L('Abierta hasta el {d}',{d:fShort(t.cl)}),L('Hasta {d}',{d:fShort(t.cl)})];
  if(t.op||t.st==='A')return['open',L('Inscripción abierta'),L('Abierta')];
  return['ask',L('Consultar inscripción'),L('Consultar')];
}
T.forEach((t,i)=>{t.i=i;t.e=t.e||t.s;t.city=t.city||'';t.prov=t.prov||'Por confirmar';const s=status(t);t.sk=s[0];t.sl=s[1];t.ss=s[2];t.ll=Array.isArray(t.ll)?t.ll:(CITY[t.city]||PC[t.prov]||null)});

const dow=now.getDay();const sat=dow===0?add(TODAY,-1):add(TODAY,6-dow);
const WE=[sat,add(sat,1)],NWE=[add(sat,7),add(sat,8)];
const inRange=(t,a,b)=>t.s<=b&&t.e>=a;
let qOn=new Set(),saved=new Set(store.get('saved',[])),sel=null,calM=null,dayFilter=null;

/* ===== Perfil del golfista y lo que sigue (fase 1: se guarda solo en este navegador) =====
   Mismo formato que tendrán las cuentas: al entrar, estos datos se subirán tal cual.
   Se guardan al pulsar «Guardar» o «Seguir»: es una función que pide el usuario. */
let PERF=raw.get('perfil'),SIGO=raw.get('sigo')||{v:1,clubs:[],prov:[]};
const hasPerf=()=>!!(PERF&&(PERF.hcp!=null||PERF.nac||PERF.sexo||PERF.fed||(PERF.clubs||[]).length));
const fmtH=h=>(h<0?'+':'')+Math.abs(h).toLocaleString(LOC,{minimumFractionDigits:1,maximumFractionDigits:1});
const slugify=x=>String(x).normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^\x00-\x7f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,'');
const follows=t=>SIGO.clubs.includes(t.club)||SIGO.prov.includes(t.prov);
function fit(t){
  if(!hasPerf())return null;
  const c=t.cond||{},why=[];
  if(PERF.sexo==='F'&&t.sex==='Masculino')why.push(L('torneo masculino'));
  if(PERF.sexo==='M'&&t.sex==='Femenino')why.push(L('torneo femenino'));
  const age=PERF.nac?(+t.s.slice(0,4))-PERF.nac:null;
  if(age!=null){
    if(c.edadMax!=null){if(age>c.edadMax)why.push(L('hasta {n} años',{n:c.edadMax}))}
    else if(t.cat==='Juvenil'&&age>21)why.push(L('torneo juvenil'));
    if(c.edadMin!=null){if(age<c.edadMin)why.push(L('desde {n} años',{n:c.edadMin}))}
    else if(t.cat==='Senior'&&age<50)why.push(L('torneo senior'));
  }
  if(c.hcp!=null&&PERF.hcp!=null&&PERF.hcp>c.hcp)why.push(L('hándicap máximo {h}',{h:fmtH(c.hcp)}));
  if(c.priv&&!(PERF.clubs||[]).includes(t.club))why.push(L('solo socios o grupo privado'));
  if(c.fed&&PERF.fed&&PERF.fed!==c.fed)why.push(L('solo federados de {f}',{f:V(c.fed)}));
  return {ok:!why.length,why};
}
const nofit=t=>{const f=fit(t);return !!(f&&!f.ok)};
function saveSigo(){SIGO.ts=Date.now();raw.set('sigo',SIGO);markMe();if(typeof syncAvisos==='function')syncAvisos()}
function toggleFollow(kind,name){const a=SIGO[kind],i=a.indexOf(name);if(i<0)a.push(name);else a.splice(i,1);saveSigo()}
function markMe(){const m=$('me');if(m)m.classList.toggle('has',hasPerf()||SIGO.clubs.length+SIGO.prov.length>0)}
const QUICK=[
 ['we','Este finde',t=>inRange(t,WE[0]<TODAY?TODAY:WE[0],WE[1])],
 ['nwe','Próximo finde',t=>inRange(t,NWE[0],NWE[1])],
 ['open','Inscripción abierta',t=>t.sk==='open'],
 ['closing','Cierra en 3 días',t=>t.sk==='open'&&!!t.cl&&t.cl<=add(TODAY,3)],
 ['free','Gratis',t=>t.price===0],
 ['saved','Guardados',t=>saved.has(t.url)],
 ['fit','Encajan conmigo',t=>!nofit(t)],
 ['sigo','Lo que sigo',t=>follows(t)]
];

const F={ccaa:['fccaa','Comunidad'],prov:['fprov','Provincia'],cat:['fcat','Categoría'],sex:['fsex','Género'],mod:['fmod','Modalidad'],form:['fform','Formato'],campo:['fcampo','Tipo de campo'],org:['forg','Organizador'],src:['fsrc','Fuente']};
function fill(el,vals,all){const cur=el.value;el.innerHTML='<option value="">'+L(all)+'</option>'+vals.map(v=>'<option value="'+esc(v)+'">'+esc(V(v))+'</option>').join('');if(vals.includes(cur))el.value=cur}
const uniq=(k,arr)=>[...new Set((arr||T).map(t=>t[k]))].filter(v=>v&&v!=='Por confirmar').sort((a,b)=>V(a).localeCompare(V(b),LANG));
fill($('fccaa'),uniq('ccaa'),'Todas');fill($('fcat'),uniq('cat'),'Todas');
['sex','mod','form','campo','org','src'].forEach(k=>fill($(F[k][0]),uniq(k),'Cualquiera'));
$('fst').innerHTML=[['','Cualquiera'],['open','Abierta'],['soon','Abre pronto'],['ask','Consultar'],['closed','Cerrada']].map(o=>'<option value="'+o[0]+'">'+L(o[1])+'</option>').join('');
function provs(){const c=$('fccaa').value;fill($('fprov'),uniq('prov',c?T.filter(t=>t.ccaa===c):T),'Todas')}
provs();
$('city').innerHTML='<option value="">'+L('¿Desde dónde sales?')+'</option>'+(navigator.geolocation?'<option value="gps">'+L('Usar mi ubicación actual')+'</option>':'')+PROV.map((p,i)=>'<option value="'+i+'">'+esc(p[0])+'</option>').join('');
$('city').value=store.get('city','');$('radius').value=store.get('radius','');
// Ubicación exacta: solo con el permiso del navegador; se usa en este dispositivo para calcular distancias
// y no se guarda ni se envía a ningún sitio (solo se recuerda que elegiste «Usar mi ubicación»).
let GEO=null,geoPrev='';
const LOCI='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 11 21 3l-8 18-2-8z"/></svg>';
const here=()=>{const v=$('city').value;if(v==='gps')return GEO?[GEO[0],GEO[1]]:null;return v===''||!PROV[v]?null:[PROV[v][2],PROV[v][3]]};
const cityName=()=>{const v=$('city').value;return v==='gps'?L('tu ubicación'):(PROV[v]?PROV[v][0]:'')};
// Identificador corto y estable de un torneo (FNV-1a de su enlace). El mismo cálculo está en functions/t/[id].js.
function tid(t){let h=2166136261;const u=t.url||'';for(let i=0;i<u.length;i++){h^=u.charCodeAt(i);h=Math.imul(h,16777619)>>>0}return h.toString(36)}
async function shareT(t){const url=location.origin+'/t/'+tid(t);const text=t.n+' - '+fShort(t.s)+(t.club?' - '+t.club:'');
  try{if(navigator.share){await navigator.share({title:t.n,text,url});return}}catch(e){if(e&&e.name==='AbortError')return}
  try{await navigator.clipboard.writeText(url);geoMsg(L('Enlace copiado. Pégalo donde quieras.'))}catch(e){prompt(L('Copia el enlace:'),url)}}
function openShared(){const m=/^#t=([a-z0-9]+)$/.exec(location.hash);if(!m)return;const t=T.find(x=>tid(x)===m[1]);
  history.replaceState(null,'',location.pathname+'#inicio');route();if(t)openModal(t.i);else geoMsg(L('Ese torneo ya no está en Banderín, pero aquí tienes todos los demás.'))}
function geoMsg(t){let m=$('geomsg');if(!m){m=document.createElement('div');m.id='geomsg';m.className='geomsg';m.setAttribute('role','status');document.body.appendChild(m)}
  m.textContent=t;m.classList.add('on');clearTimeout(geoMsg.t);geoMsg.t=setTimeout(()=>m.classList.remove('on'),6000)}
function setCity(v){$('city').value=v;store.set('city',v);['hcity','pcity'].forEach(id=>{if($(id))$(id).value=v})}
function locate(quiet){
  if(!navigator.geolocation){if(!quiet)geoMsg(L('Tu navegador no permite compartir la ubicación.'));setCity(geoPrev);return}
  geoLabel(true);['city','hcity','pcity'].forEach(id=>{const o=$(id)&&$(id).querySelector('option[value="gps"]');if(o)o.textContent=L('Buscando tu ubicación…')});
  navigator.geolocation.getCurrentPosition(pos=>{
    GEO=[pos.coords.latitude,pos.coords.longitude];setCity('gps');geoLabel();
    if(!$('radius').value){$('radius').value=$('hrad')?$('hrad').value||'100':'100';store.set('radius',$('radius').value)}
    if($('radius').value)$('sort').value='dist';render();renderHome();
  },err=>{GEO=null;geoLabel();setCity(geoPrev==='gps'?'':geoPrev);render();renderHome();
    if(!quiet)geoMsg(err.code===1?L('No has dado permiso para usar tu ubicación. Puedes activarlo en los ajustes del navegador o elegir tu ciudad.'):L('No hemos podido saber dónde estás. Elige tu ciudad en la lista.'))
  },{enableHighAccuracy:false,timeout:12000,maximumAge:600000})}
function geoLabel(busy){const hb=$('hLoc');if(hb){const on=!!GEO&&$('city').value==='gps';hb.classList.toggle('on',on);hb.classList.toggle('busy',!!busy);hb.lastChild.textContent=busy?L('Buscando tu ubicación…'):on?L('Usando tu ubicación'):L('Usar mi ubicación')}['city','hcity','pcity'].forEach(id=>{const o=$(id)&&$(id).querySelector('option[value="gps"]');if(o)o.textContent=GEO?L('Mi ubicación'):L('Usar mi ubicación actual')})}
function cityPick(el){const v=el.value;if(v==='gps'&&!GEO){locate(false);return true}geoPrev=v;setTimeout(()=>geoLabel(),0);return false}
document.addEventListener('click',e=>{const b=e.target.closest('[data-locate]');if(!b)return;e.preventDefault();e.stopPropagation();
  if($('city').value==='gps'&&GEO&&b.classList.contains('locchip')){setCity(geoPrev==='gps'?'':geoPrev);geoLabel();render();renderHome();return}
  if($('city').value==='gps'&&GEO){if(b.id==='hLoc')goList(null,true);return}
  geoPrev=$('city').value;locate(false)},true);
if($('city').value==='gps'){ // al volver: solo se pide sin preguntar si el permiso ya estaba concedido
  const ask=()=>locate(true);
  if(navigator.permissions&&navigator.permissions.query)navigator.permissions.query({name:'geolocation'}).then(r=>{if(r.state==='granted')ask();else setCity('')}).catch(()=>setCity(''));else setCity('')}
const km=t=>{const h=here();return h&&t.ll?Math.round(hav(h,t.ll)):null};

const norm=s=>s.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');
function filtered(ignoreQuick,ignoreDay){
  const q=norm($('q').value.trim()),st=$('fst').value,pr=$('fprice').value,d1=$('fd1').value,d2=$('fd2').value,past=$('fpast').checked,rad=+$('radius').value||0,h=here();
  return T.filter(t=>{
    for(const k in F){const v=$(F[k][0]).value;if(v&&t[k]!==v)return false}
    if(q&&!norm(t.n+' '+t.club+' '+t.city+' '+t.prov).includes(q))return false;
    if(st&&t.sk!==st)return false;
    if(past&&t.sk==='done')return false;
    if(pr==='free'&&t.price!==0)return false;
    if(pr==='known'&&t.price==null)return false;
    if((pr==='30'||pr==='60')&&(t.price==null||t.price>+pr))return false;
    if(d1&&t.e<d1)return false;if(d2&&t.s>d2)return false;
    if(!ignoreDay&&dayFilter&&!inRange(t,dayFilter,dayFilter))return false;
    if(rad&&h){const k=km(t);if(k==null||k>rad)return false}
    if(!ignoreQuick)for(const id of qOn){const f=QUICK.find(x=>x[0]===id);if(f&&!f[2](t))return false}
    return true});
}
function sorted(list){
  const m=$('sort').value;
  if(m==='dist'&&here())return list.slice().sort((a,b)=>(km(a)??1e9)-(km(b)??1e9)||a.s.localeCompare(b.s));
  if(m==='close')return list.slice().sort((a,b)=>((a.sk==='open'&&a.cl)||'9999').localeCompare((b.sk==='open'&&b.cl)||'9999')||a.s.localeCompare(b.s));
  return list.slice().sort((a,b)=>a.s.localeCompare(b.s)||a.n.localeCompare(b.n));
}
const place=t=>[t.club,t.city&&t.city!==t.club?t.city:'',t.prov!==t.city&&t.prov!=='Por confirmar'?t.prov:''].filter(Boolean).join(' - ');
const PLAYED_ICON='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>';
const cnt=n=>n+' '+(n===1?L('torneo'):L('torneos'));
const label=t=>L(t.sk==='done'||t.sk==='closed'?'Ver torneo':t.direct===false?'Web del organizador':'Inscribirme');
function row(t){
  const k=km(t);
  return '<button class="row" role="option" data-i="'+t.i+'" aria-selected="'+(sel===t.i)+'">'+I.flag(t.sk)+'<span class="t"><b>'+esc(t.n)+'</b><span>'+(nofit(t)?'<i class="nofit">'+L('No encaja')+'</i>':'')+esc(place(t))+(t.e!==t.s?' - '+fShort(t.s)+'–'+fShort(t.e):'')+'</span></span><span class="cat">'+esc(V(t.cat))+'</span><span class="km num">'+(k!=null?(k<5?'&lt; 5 km':k+' km'):'')+'</span><span class="st '+t.sk+'">'+esc(t.ss)+'</span>'+(saved.has(t.url)?I.starS:'<span></span>')+'</button>';
}
function weekTag(d){if(d===TODAY)return L('Hoy');if(d===add(TODAY,1))return L('Mañana');if(d>=WE[0]&&d<=WE[1])return L('Este finde');if(d>=NWE[0]&&d<=NWE[1])return L('Próximo finde');return''}
// La lista se pinta por tandas: 80 torneos al principio y el resto según se acerca el final (o con «Ver más»).
// Con más de mil torneos, pintarlos todos de golpe creaba 12.000 elementos y bloqueaba el móvil.
let LQ=[],LIO=null;
function listMore(n){
  const box=$('list');const old=box.querySelector('.lmore');if(old)old.remove();
  let h='',k=0;while(LQ.length&&k<n){const x=LQ.shift();h+=x[1];if(x[0])k++}
  box.insertAdjacentHTML('beforeend',h);
  box.querySelectorAll('.row:not([aria-selected])').forEach(r=>r.setAttribute('aria-selected',String(+r.dataset.i===sel)));
  const left=LQ.filter(x=>x[0]).length;
  if(left){box.insertAdjacentHTML('beforeend','<button type="button" class="btn ghost rmore lmore">'+L('Ver {n} más',{n:Math.min(120,left)})+'</button>');
    const b=box.querySelector('.lmore');b.onclick=()=>listMore(120);
    if('IntersectionObserver' in window){LIO=LIO||new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){LIO.unobserve(e.target);listMore(120)}})},{rootMargin:'600px 0px'});LIO.observe(b)}}
}
function renderList(list){
  LQ=[];if(LIO)LIO.disconnect();
  if(!list.length){$('list').innerHTML='<div class="empty"><b>'+L('Ningún torneo con estos filtros.')+'</b>'+L('Prueba a quitar alguno o a ampliar la distancia.')+'</div>';return}
  if($('sort').value!=='date'){LQ=[[0,'<div class="dhead"><b>'+L($('sort').value==='dist'?'Más cerca primero':'Cierra antes primero')+'</b><span>'+cnt(list.length)+'</span></div>']].concat(list.map(t=>[1,row(t)]))}
  else{const g={};list.forEach(t=>(g[t.s]=g[t.s]||[]).push(t));
    Object.keys(g).sort().forEach(d=>{const w=weekTag(d);LQ.push([0,'<div class="dhead"><b>'+fDay(d)+'</b><span>'+cnt(g[d].length)+'</span>'+(w?'<span class="wk">'+w+'</span>':'')+'</div>']);g[d].forEach(t=>LQ.push([1,row(t)]))})}
  // Si hay un torneo elegido más abajo, se pinta hasta él para que su fila exista.
  let n=80;if(sel!=null){let c=0;for(const x of LQ){if(x[0])c++;if(x[0]&&x[1].includes('data-i="'+sel+'"')){n=Math.max(n,c+10);break}}}
  $('list').innerHTML='';listMore(n);
}
function gcal(t){const e=add(t.e,1).replace(/-/g,'');return 'https://calendar.google.com/calendar/render?action=TEMPLATE&text='+encodeURIComponent(t.n)+'&dates='+t.s.replace(/-/g,'')+'/'+e+'&location='+encodeURIComponent(place(t))+'&details='+encodeURIComponent(L('Inscripción y detalles: ')+t.url)}
function renderDetail(){fillDetail($('detail'),T[sel],false)}
function fillDetail(d,t,modal){
  if(!t){d.innerHTML='<div class="dmap">'+greenSvg(3)+'</div><div class="dbody"><h2>'+L('Elige un torneo.')+'</h2><p class="sub">'+L('Toca cualquier fila para ver su ficha y el enlace de inscripción.')+'</p></div>';return}
  const k=km(t);const isS=saved.has(t.url);
  const facts=[['Fecha',t.e!==t.s?fShort(t.s)+' – '+fShort(t.e):fWk(t.s)],['Precio',t.price==null?L(/se paga en el club/.test(t.insNote||'')?'Se paga en el club':'En la web'):eur(t.price)],['Categoría',V(t.cat)],['Modalidad',V(t.mod)],['Formato',V(t.form)],['Género',V(t.sex)],['Recorrido',V(t.campo)],['Organiza',t.via&&!/^(Club|Golf Directo)$/.test(t.via)?t.via:V(t.org),1]];
  if(t.plazas)facts.splice(2,0,['Plazas',L('{n} máx.',{n:t.plazas})]);
  if(t.insNote)facts.push(['Inscripción',V(t.insNote),1]);
  if(t.op)facts.push(['Abre inscripción',fShort(t.op)]);if(t.cl)facts.push(['Cierra inscripción',fShort(t.cl)]);
  if(t.priceNote)facts.push(['Sobre el precio',LANG==='en'?t.priceNote.replace(/^Desde (.*?) €; hay (\d+) tarifas$/,'From €$1; $2 rates').replace('Precio de la inscripción online','Online entry price').replace('Según las condiciones publicadas','According to the published conditions').replace(/desde ([\d.,]+) € hasta ([\d.,]+) €/,'from €$1 to €$2'):t.priceNote,1]);
  const fv=fit(t);if(fv)facts.push(['Tu perfil',fv.ok?L('Encaja con lo publicado'):L('No encaja')+': '+fv.why.join(', '),1,fv.ok?'fit':'nofitf']);
  if(k!=null)facts.push(['Distancia',(k<5?L('Menos de 5 km'):'≈ '+k+' km')+' '+L('desde')+' '+cityName(),1]);
  const chg=chgFor(t.url);
  const same=T.filter(x=>x.club===t.club&&x.i!==t.i&&x.sk!=='done').slice(0,4);
  d.innerHTML='<div class="dmap">'+greenSvg(hash(t.club||t.n))+'<span class="where">'+esc(t.prov!=='Por confirmar'?t.prov:V(t.ccaa))+'</span><button class="icon-btn dclose" data-act="close" aria-label="'+L('Cerrar ficha')+'">'+I.x+'</button></div>'+
   '<div class="dbody"><span class="dst st '+t.sk+'">'+I.flag(t.sk)+esc(t.sl)+'</span><h2>'+esc(t.n)+'</h2><p class="sub">'+esc(place(t))+'</p>'+(t.club?'<button class="follow" data-act="follow" aria-pressed="'+SIGO.clubs.includes(t.club)+'">'+(SIGO.clubs.includes(t.club)?'✓ '+L('Sigues este club'):'+ '+L('Seguir este club'))+'</button>':'')+(t.aviso?'<p class="dnote"><b>'+L('Aviso')+':</b> '+esc(L(t.aviso))+'</p>':'')+(chg?'<p class="dnote">'+chg+'</p>':'')+
   '<div class="facts">'+facts.filter(f=>f[1]&&f[1]!=='Sin indicar'&&f[1]!=='Not stated').map(f=>'<div class="fact'+(f[2]?' wide':'')+(f[3]?' '+f[3]:'')+'"><span>'+L(f[0])+'</span><b title="'+esc(f[1])+'">'+esc(f[1])+'</b></div>').join('')+'</div>'+
   '<div class="acts"><a class="btn primary" href="'+esc(safeUrl(t.url))+'" target="_blank" rel="noopener noreferrer">'+label(t)+I.out+'</a><button class="btn ghost" data-act="save" aria-pressed="'+isS+'" title="'+L(isS?'Quitar de guardados':'Guardar')+'" aria-label="'+L(isS?'Quitar de guardados':'Guardar')+'">'+I.star+'</button><a class="btn ghost" href="'+gcal(t)+'" target="_blank" rel="noopener noreferrer" title="'+L('Añadir a Google Calendar')+'" aria-label="'+L('Añadir a Google Calendar')+'">'+I.cal+'</a><button class="btn ghost" data-act="share" title="'+L('Compartir torneo')+'" aria-label="'+L('Compartir torneo')+'">'+I.share+'</button></div>'+
   '<p class="note">'+L('Datos de {s}.',{s:esc(t.src)})+' '+(t.ok?esc(checkedText(t.ok))+' ':'')+L('Confirma fechas y precio en la web del organizador antes de inscribirte.')+(t.direct===false?' '+L('Este organizador no publica una ficha por torneo: el enlace lleva a su página de torneos.'):'')+'</p>'+
   (same.length?'<div class="same"><h3>'+L('Más en este campo')+'</h3>'+same.map(x=>'<button data-i="'+x.i+'"><span>'+esc(x.n)+'</span><span>'+fShort(x.s)+'</span></button>').join('')+'</div>':'')+'</div>';
  d.querySelector('[data-act=share]').onclick=()=>shareT(t);
  d.querySelector('[data-act=save]').onclick=()=>{isS?saved.delete(t.url):saved.add(t.url);store.set('saved',[...saved]);syncAvisos();render();if(modal){fillDetail(d,t,true);renderHome()}};
  const fb=d.querySelector('[data-act=follow]');if(fb)fb.onclick=()=>{toggleFollow('clubs',t.club);fillDetail(d,t,modal);renderQuick();if(location.hash==='#perfil')renderPerfil()};
  d.querySelector('[data-act=close]').onclick=modal?closeModal:closeSheet;
  d.querySelectorAll('.same button').forEach(b=>b.onclick=()=>modal?fillDetail(d,T[+b.dataset.i],true):select(+b.dataset.i,true));
}
const mobile=()=>matchMedia('(max-width:900px)').matches;
function openSheet(){if(!mobile())return;$('detail').classList.add('open');$('scrim').classList.add('open');document.body.classList.add('lock')}
function closeSheet(){$('detail').classList.remove('open');$('scrim').classList.remove('open');document.body.classList.remove('lock')}
function select(i,open){sel=i;document.querySelectorAll('.row').forEach(r=>r.setAttribute('aria-selected',String(+r.dataset.i===i)));renderDetail();$('detail').scrollTop=0;if(open)openSheet()}
function renderQuick(){
  const base=filtered(true);
  $('quick').innerHTML=(navigator.geolocation?'<button class="qchip locchip" data-locate aria-pressed="'+($('city').value==='gps'&&!!GEO)+'">'+LOCI+L('Cerca de mí')+'</button>':'')+QUICK.map(q=>{if(!qOn.has(q[0])&&((q[0]==='saved'&&!saved.size)||(q[0]==='fit'&&!hasPerf())||(q[0]==='sigo'&&!SIGO.clubs.length&&!SIGO.prov.length)))return'';const n=base.filter(q[2]).length;return '<button class="qchip" data-q="'+q[0]+'" aria-pressed="'+qOn.has(q[0])+'">'+(q[0]==='saved'?I.star:q[0]==='closing'?I.clock:'')+L(q[1])+' <span class="n num">'+n+'</span></button>'}).join('');
}
function chips(){
  const out=[];
  for(const k in F){const el=$(F[k][0]);if(el.value)out.push([el.id,L(F[k][1])+': '+V(el.value)])}
  if($('fst').value)out.push(['fst',L('Inscripción')+': '+$('fst').options[$('fst').selectedIndex].text]);
  if($('fprice').value)out.push(['fprice',L('Precio')+': '+$('fprice').options[$('fprice').selectedIndex].text]);
  if($('fd1').value)out.push(['fd1',L('Desde')+' '+fShort($('fd1').value)]);
  if($('fd2').value)out.push(['fd2',L('Hasta')+' '+fShort($('fd2').value)]);
  if(!$('fpast').checked)out.push(['fpast',L('Con finalizados')]);
  if(dayFilter)out.push(['day',fWk(dayFilter)]);
  $('chips').innerHTML=out.map(c=>'<button class="chip" data-f="'+c[0]+'">'+esc(c[1])+'</button>').join('');
  const n=out.filter(c=>c[0]!=='day').length;$('fcount').hidden=!n;$('fcount').textContent=n;
  $('moreBtn').setAttribute('aria-pressed',String(!$('more').hidden||n>0));
}
function render(){
  if(!here()&&$('sort').value==='dist')$('sort').value='date';
  $('sort').querySelector('[value=dist]').disabled=!here();
  const list=sorted(filtered());
  $('count').textContent=cnt(list.length);
  renderQuick();chips();renderList(list);
  if(sel==null||!list.some(t=>t.i===sel))sel=!mobile()&&list.length?list[0].i:null;
  document.querySelectorAll('.row').forEach(r=>r.setAttribute('aria-selected',String(+r.dataset.i===sel)));
  renderDetail();renderCal();renderHome();
}
const months=()=>[...new Set(T.flatMap(t=>[t.s.slice(0,7),t.e.slice(0,7)]))].sort();
function renderCal(){
  const ms=months();if(!ms.length)return;
  if(!calM)calM=ms.includes(TODAY.slice(0,7))?TODAY.slice(0,7):(ms.find(m=>m>TODAY.slice(0,7))||ms[ms.length-1]);
  const list=filtered(false,true);
  const[y,m]=calM.split('-').map(Number);const first=new Date(y,m-1,1);
  $('calTitle').textContent=first.toLocaleDateString(LOC,{month:'long',year:'numeric'});
  const lead=(first.getDay()+6)%7,days=new Date(y,m,0).getDate();
  let h=(LANG==='en'?['Mon','Tue','Wed','Thu','Fri','Sat','Sun']:['Lun','Mar','Mié','Jue','Vie','Sáb','Dom']).map(d=>'<div class="dow">'+d+'</div>').join('');
  for(let i=0;i<lead;i++)h+='<div class="cell out"></div>';
  for(let d=1;d<=days;d++){const ds=calM+'-'+pad(d);const ev=list.filter(t=>inRange(t,ds,ds));
    h+='<button class="cell'+(ev.length?'':' none')+(ds===TODAY?' today':'')+'" data-d="'+ds+'"'+(ev.length?'':' disabled')+' aria-label="'+d+(ev.length?': '+cnt(ev.length):'')+'"><span class="top"><span class="n">'+d+'</span>'+(ev.length?'<span class="c">'+ev.length+'</span>':'')+'</span>'+ev.slice(0,2).map(t=>'<span class="x">'+esc(t.n)+'</span>').join('')+'</button>'}
  const tail=(7-(lead+days)%7)%7;for(let i=0;i<tail;i++)h+='<div class="cell out"></div>';
  $('cal').innerHTML=h;$('prev').disabled=ms.indexOf(calM)<=0;$('next').disabled=ms.indexOf(calM)>=ms.length-1;
  const inM=d=>d&&d.slice(0,7)===calM;
  if(!inM(calDay)){const withEv=[...$('cal').querySelectorAll('.cell[data-d]:not(:disabled)')].map(c=>c.dataset.d);calDay=withEv.includes(TODAY)?TODAY:(withEv.find(d=>d>=TODAY)||withEv[0]||null)}
  renderAgenda(list);
}
let calDay=null;
function renderAgenda(list){
  list=list||filtered(false,true);
  document.querySelectorAll('.cell.sel').forEach(c=>c.classList.remove('sel'));
  if(!calDay){$('aEye').textContent='';$('aTitle').textContent=L('Sin torneos este mes con tus filtros.');$('aRows').innerHTML='';$('aList').hidden=true;return}
  const c=$('cal').querySelector('.cell[data-d="'+calDay+'"]');if(c)c.classList.add('sel');
  const ev=list.filter(t=>inRange(t,calDay,calDay)).sort((a,b)=>(a.sk==='open'?0:1)-(b.sk==='open'?0:1)||a.n.localeCompare(b.n,'es'));
  const wt=weekTag(calDay);
  $('aEye').textContent=(wt?wt+' - ':'')+cnt(ev.length);
  $('aTitle').textContent=fDay(calDay);
  $('aList').hidden=!ev.length;
  $('aRows').innerHTML=ev.length?ev.map(row).join(''):'<div class="empty">'+L('Ningún torneo este día con tus filtros.')+'</div>';
}
function route(){
  const h=location.hash.slice(1),LD=window.LEGALDOCS||{};
  const v=['inicio','lista','calendario','resultados','fuentes','perfil'].includes(h)?h:LD[h]?'legal':'inicio';
  ['inicio','lista','calendario','resultados','fuentes','perfil','legal'].forEach(x=>{$('v-'+x).hidden=x!==v});
  $('controls').hidden=v!=='lista'&&v!=='calendario';$('pagehead').hidden=v!=='lista'&&v!=='calendario';document.body.dataset.view=v;
  if(v==='resultados')openResults();
  if(v==='perfil')renderPerfil();
  {const m=$('me');if(v==='perfil')m.setAttribute('aria-current','page');else m.removeAttribute('aria-current')}
  if(v==='legal'){renderLegal(h);scrollTo({top:0})}
  if(v!=='inicio'&&v!=='calendario')closeModal();
  document.querySelectorAll('.tabs a').forEach(a=>{const on=a.getAttribute('href')==='#'+v;a.classList.toggle('on',on);if(on)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current')});
  if(v!=='lista')closeSheet();
}
const inputs=()=>document.querySelectorAll('#controls select,#controls input');
let qT=0;inputs().forEach(el=>el.addEventListener('input',()=>{if(el.type==='search'||el.type==='text'){clearTimeout(qT);qT=setTimeout(go,180)}else go();function go(){
  if(el.id==='fccaa')provs();
  if(el.id==='city'){if(cityPick(el))return;store.set('city',el.value)}
  if(el.id==='radius'){store.set('radius',el.value);if(el.value&&here())$('sort').value='dist'}
  render()}}));
$('sort').addEventListener('input',render);
$('moreBtn').onclick=()=>{const m=$('more');m.hidden=!m.hidden;$('moreBtn').setAttribute('aria-expanded',String(!m.hidden));chips()};
$('reset').onclick=()=>{inputs().forEach(i=>{if(i.id!=='city'&&i.type!=='checkbox')i.value=''});$('fpast').checked=true;qOn.clear();dayFilter=null;store.set('radius','');$('sort').value='date';provs();render()};
$('quick').onclick=e=>{const b=e.target.closest('.qchip');if(!b)return;const q=b.dataset.q;if(qOn.has(q))qOn.delete(q);else{qOn.add(q);if(q==='we')qOn.delete('nwe');if(q==='nwe')qOn.delete('we');dayFilter=null}render()};
$('chips').onclick=e=>{const b=e.target.closest('.chip');if(!b)return;const f=b.dataset.f;if(f==='day')dayFilter=null;else if(f==='fpast')$('fpast').checked=true;else $(f).value='';if(f==='fccaa')provs();render()};
$('list').onclick=e=>{const r=e.target.closest('.row');if(r)select(+r.dataset.i,true)};
$('list').onkeydown=e=>{if(e.key!=='ArrowDown'&&e.key!=='ArrowUp')return;const rows=[...document.querySelectorAll('.row')];const k=rows.findIndex(r=>+r.dataset.i===sel);const n=rows[Math.max(0,Math.min(rows.length-1,k+(e.key==='ArrowDown'?1:-1)))];if(n){e.preventDefault();n.focus();select(+n.dataset.i,false)}};
$('scrim').onclick=closeSheet;
addEventListener('keydown',e=>{if(e.key==='Escape'){closeSheet();closeModal()}});
$('cal').onclick=e=>{const c=e.target.closest('.cell[data-d]');if(!c||c.disabled)return;calDay=c.dataset.d;renderAgenda();
  if(innerWidth<901){const a=$('agenda').getBoundingClientRect();if(a.top>innerHeight*.55)scrollBy({top:a.top-90,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'})}};
$('aRows').onclick=e=>{const r=e.target.closest('.row');if(r)openModal(+r.dataset.i)};
$('aList').onclick=()=>{if(!calDay)return;dayFilter=calDay;qOn.delete('we');qOn.delete('nwe');$('sort').value='date';location.hash='lista';render();scrollTo({top:0,behavior:'smooth'})};
$('prev').onclick=()=>{const ms=months();calM=ms[ms.indexOf(calM)-1];renderCal()};
$('next').onclick=()=>{const ms=months();calM=ms[ms.indexOf(calM)+1];renderCal()};
$('theme').onclick=()=>{const r=document.documentElement,dark=r.dataset.theme?r.dataset.theme==='dark':matchMedia('(prefers-color-scheme:dark)').matches;r.dataset.theme=dark?'light':'dark';store.set('tema',r.dataset.theme)};
{const t=store.get('tema',null);if(t)document.documentElement.dataset.theme=t}
/* ===== Confianza: hora de revisión, cambios y cobertura ===== */
const REV=window.REVISION||((window.ACTUALIZADO||TODAY)+'T07:00');
const revDay=REV.slice(0,10),revTime=REV.slice(11,16);
function revWhen(){return revDay===TODAY?L('hoy a las {t}',{t:revTime}):revDay===add(TODAY,-1)?L('ayer a las {t}',{t:revTime}):L('el {d} a las {t}',{d:fShort(revDay),t:revTime})}
function revText(){return L('Comprobado {w}.',{w:revWhen()})}
function sealText(){return L('Comprobado {w} - {n} enlaces verificados',{w:revWhen(),n:T.filter(t=>t.ok).length})}
function checkedText(ok){return ok===revDay?L('Enlace comprobado {w}.',{w:revWhen()}):L('Enlace comprobado el {d}.',{d:fShort(ok)})}
const CH=(window.CAMBIOS||[]).filter(c=>c.k!=='nuevos');
function chgFor(url){const c=CH.find(x=>x.url===url&&(x.k==='fecha'||x.k==='plazo'));if(!c)return'';
  return c.k==='fecha'?'<b>'+L('Cambio de fecha')+':</b> '+esc(L('antes {a}, ahora {b}. Detectado el {d}.',{a:fShort(c.a),b:fShort(c.b),d:fShort(c.d)})):'<b>'+L('Cambio de plazo')+':</b> '+esc(L('la inscripción cerraba el {a}; ahora cierra el {b}.',{a:fShort(c.a),b:fShort(c.b)}))}
const CHK={fecha:'Cambia de fecha',plazo:'Cambia el plazo',cancelado:'Cancelado',retirado:'Retirado',abre:'Abre inscripción',nuevos:'Nuevos'};
function renderTrust(){
  const nOk=T.filter(t=>t.ok).length,cc=new Set(T.filter(t=>t.sk!=='done').map(t=>t.ccaa)).size;
  $('trust').innerHTML='<div class="big">'+esc(L('Comprobado {w}.',{w:revWhen()}))+'<small>'+esc(L('Cada mañana un proceso automático lee las fuentes, compara con el día anterior y abre cada enlace antes de publicarlo. Si un enlace no responde, el torneo no se publica.'))+'</small></div>'+
   [[nOk,'enlaces verificados'],[SRC.filter(s=>s.volcada).length,'fuentes leídas'],[cc,'comunidades con torneos']].map(x=>'<div class="m"><b class="num">'+x[0]+'</b><span>'+L(x[1])+'</span></div>').join('');
  const C=window.CAMBIOS||[];
  $('chTitle').textContent=C.length?L('Lo que ha cambiado en 14 días.'):L('Sin cambios en los últimos 14 días.');
  $('changes').innerHTML=C.length?C.slice(0,40).map(c=>{
    if(c.k==='nuevos')return '<div class="chg"><span class="k nuevos">'+L(CHK.nuevos)+'</span><b>'+esc(L('{n} torneos nuevos publicados',{n:c.c}))+'</b><span class="s">'+esc(fShort(c.d))+'</span></div>';
    const det=c.k==='fecha'?L('Antes {a}, ahora {b}',{a:fShort(c.a),b:fShort(c.b)}):c.k==='plazo'?L('Cierre: antes {a}, ahora {b}',{a:fShort(c.a),b:fShort(c.b)}):c.k==='retirado'?L('Ya no aparece en su fuente. Confirma con el organizador.'):c.k==='abre'?L('Inscripción abierta desde hoy'):L('El organizador lo ha cancelado');
    return '<a class="chg" href="'+esc(safeUrl(c.url))+'" target="_blank" rel="noopener noreferrer"><span class="k '+c.k+'">'+L(CHK[c.k])+'</span><b>'+esc(c.n)+'</b><span class="s">'+esc([fShort(c.d),c.club,det].filter(Boolean).join(' - '))+'</span></a>'}).join('')
   :'<p class="chg empty">'+L('Aquí verás cada torneo que cambie de fecha, se cancele, desaparezca de su fuente o abra inscripción. El registro empieza con la revisión de mañana y guarda los últimos 14 días.')+'</p>';
  const CO=window.COBERTURA||[];
  $('cov').innerHTML='<table><thead><tr><th>'+L('Comunidad')+'</th><th>'+L('Calendario federativo')+'</th><th style="text-align:right">'+L('Torneos')+'</th></tr></thead><tbody>'+CO.map(r=>'<tr><td><b>'+esc(V(r.ccaa))+'</b><small>'+esc(r.fuentes.length?r.fuentes.map(V).join(', '):L('Sin fuente volcada'))+'</small></td><td><span class="bdg '+r.estado+'">'+L(r.estado==='completo'?'Completo':r.estado==='parcial'?'Parcial':'Pendiente')+'</span><small>'+esc(L(r.nota))+'</small></td><td class="n num">'+r.n+'</td></tr>').join('')+'</tbody></table>';
}
renderTrust();

/* ===== Resultados e historial ===== */
let played=new Map((store.get('played',[])||[]).map(p=>[p.url,p])),rMode='res',rLimit=150,rLoaded=false;
function savePlayed(){store.set('played',[...played.values()])}
function openResults(){
  $('resTitle').textContent=L('Resultados de los últimos 45 días.');
  $('resLede').textContent=L('Banderín enlaza a la clasificación oficial de cada torneo en cuanto el organizador la publica. Marca los que has jugado y tendrás tu historial aquí.');
  if(rLoaded){renderResults();return}
  $('rlist').innerHTML='<div class="empty"><b>'+L('Cargando resultados…')+'</b></div>';
  const sc=document.createElement('script');sc.src='/pasados.js'+(PASV?'?v='+PASV:'');sc.onload=()=>{rLoaded=true;
    const P=window.PASADOS||[];fill($('rccaa'),[...new Set(P.map(t=>t.ccaa))].filter(v=>v&&v!=='Por confirmar').sort((a,b)=>V(a).localeCompare(V(b),LANG)),'Todas las comunidades');renderResults()};
  sc.onerror=()=>{$('rlist').innerHTML='<div class="empty"><b>'+L('No se han podido cargar los resultados.')+'</b>'+L('Vuelve a intentarlo en un momento.')+'</div>'};
  document.head.appendChild(sc);
}
function renderResults(){
  const P=window.PASADOS||[],q=norm($('rq').value.trim()),cc=$('rccaa').value;
  $('rMine').textContent=played.size?played.size:'';
  let list;
  if(rMode==='mine'){const byU=new Map(P.map(t=>[t.url,t]));list=[...played.values()].map(p=>Object.assign({},p,byU.get(p.url)||{})).sort((a,b)=>b.s.localeCompare(a.s))}
  else list=P.filter(t=>rMode==='all'||t.res);
  list=list.filter(t=>(!cc||t.ccaa===cc)&&(!q||norm(t.n+' '+(t.club||'')+' '+(t.prov||'')).includes(q)));
  if(!list.length){$('rlist').innerHTML='<div class="empty"><b>'+L(rMode==='mine'?'Aún no has marcado ningún torneo.':'Ningún torneo con estos filtros.')+'</b>'+L(rMode==='mine'?'Pulsa «Lo jugué» en cualquier torneo de la pestaña «Con resultados» o «Todos».':'Prueba con otra comunidad o quita la búsqueda.')+(rMode==='mine'&&!consent.pref()?' '+L('Para que se guarden al cerrar la página, acepta las cookies de preferencias.'):'')+'</div>';return}
  const g={};list.slice(0,rLimit).forEach(t=>(g[t.s]=g[t.s]||[]).push(t));
  $('rlist').innerHTML=Object.keys(g).sort().reverse().map(d=>'<div class="dhead"><b>'+fDay(d)+'</b><span>'+cnt(g[d].length)+'</span></div>'+g[d].map(t=>{const on=played.has(t.url);
    return '<div class="rrow"><span class="t"><b>'+esc(t.n)+'</b><span>'+esc([t.club,t.prov&&t.prov!=='Por confirmar'?t.prov:'',t.cat?V(t.cat):''].filter(Boolean).join(' - '))+'</span></span><button class="played" data-p="'+esc(t.url)+'" aria-pressed="'+on+'">'+PLAYED_ICON+L(on?'Jugado':'Lo jugué')+'</button><a class="btn '+(t.res?'primary':'soft')+'" href="'+esc(safeUrl(t.url))+'" target="_blank" rel="noopener noreferrer">'+L(t.res?'Resultados':'Ficha')+I.out+'</a></div>'}).join('')).join('')+
    (list.length>rLimit?'<button class="btn ghost rmore" id="rmore">'+L('Ver {n} más',{n:Math.min(150,list.length-rLimit)})+'</button>':'');
}
let rqT=0;$('rq').addEventListener('input',()=>{clearTimeout(rqT);rqT=setTimeout(()=>{rLimit=150;renderResults()},180)});
$('rccaa').addEventListener('input',()=>{rLimit=150;renderResults()});
$('rmode').addEventListener('click',e=>{const a=e.target.closest('a');if(!a)return;e.preventDefault();rMode=a.dataset.m;rLimit=150;document.querySelectorAll('#rmode a').forEach(x=>x.classList.toggle('on',x===a));renderResults()});
$('rlist').addEventListener('click',e=>{
  if(e.target.closest('#rmore')){rLimit+=150;renderResults();return}
  const b=e.target.closest('.played');if(!b)return;const u=b.dataset.p;
  if(played.has(u))played.delete(u);else{const t=(window.PASADOS||[]).find(x=>x.url===u);if(t)played.set(u,{url:t.url,n:t.n,s:t.s,club:t.club,prov:t.prov,ccaa:t.ccaa,cat:t.cat,res:t.res})}
  savePlayed();renderResults()});

/* ===== Idioma ===== */
$('lang').textContent=LANG==='en'?'ES':'EN';
$('lang').title=$('lang').ariaLabel=LANG==='en'?'Ver en español':'English version';
$('lang').onclick=()=>{const to=LANG==='en'?'es':'en';raw.set('lang',to);location.href=(to==='en'?'/en/':'/')+location.hash};

const ok=SRC.filter(s=>s.volcada).length;
$('srcTitle').textContent=L('{a} fuentes al día. {b} pendientes.',{a:ok,b:SRC.length-ok});
$('srcs').innerHTML=SRC.map(s=>{const n=s.n!=null?s.n:T.filter(t=>t.src===s.nombre&&t.sk!=='done').length;const k=s.volcada?'open':'soon';return '<article class="src glass"><span class="dst st '+k+'">'+I.flag(k)+(s.volcada?L('Volcada')+' - '+(n?cnt(n):L('sin torneos próximos')):L('Pendiente de volcar'))+'</span><h3>'+esc(V(s.nombre))+'</h3><p>'+esc(L(s.desc))+'</p><div class="foot"><span>'+esc(s.url.replace(/^https?:\/\/(www\.)?/,'').split('/')[0])+'</span><a class="btn soft" href="'+esc(safeUrl(s.url))+'" target="_blank" rel="noopener noreferrer">'+L('Abrir')+I.out+'</a></div></article>'}).join('');
$('k1').textContent=T.filter(t=>t.sk!=='done').length;$('k2').textContent=T.filter(t=>t.sk==='open').length;$('k3').textContent=uniq('ccaa').length;
$('upd').textContent=revText();

// ---------- Portada ----------
const MAPA=window.MAPA;
function mp(lat,lon){const m=MAPA.meta,R=Math.PI/180;const r=m.F/Math.pow(Math.tan(Math.PI/4+lat*R/2),m.n),a=m.n*(lon*R-m.l0);let x=r*Math.sin(a),y=m.r0-r*Math.cos(a);if(lon<-12){x+=m.ddx;y+=m.ddy}return[(x-m.X0)*m.K+10,(m.Y0-y)*m.K+10]}
const HI={
 senior:'<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="14" cy="7" r="3"/><path d="M14 11v9l-4 8M14 20l4 8M10 15h8"/><path d="M22 14v14"/></svg>',
 juvenil:'<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="16" cy="9" r="3.5"/><path d="M16 13v8l-4 7M16 21l4 7M11 16l5 1 5-3"/></svg>',
 pp:'<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 26V6l10 4-10 4"/><ellipse cx="14" cy="26" rx="8" ry="2.5"/></svg>',
 parejas:'<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="10" r="3.5"/><circle cx="21" cy="10" r="3.5"/><path d="M5 26c0-5 3-8 6-8s6 3 6 8M15 26c0-5 3-8 6-8s6 3 6 8"/></svg>',
 fem:'<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="16" cy="12" r="6"/><path d="M16 18v10M12 24h8"/></svg>',
 pro:'<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 5h12v6a6 6 0 0 1-12 0z"/><path d="M10 7H6a4 4 0 0 0 4 5M22 7h4a4 4 0 0 1-4 5M16 17v5M11 27h10M13 22h6"/></svg>',
 fed:'<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M16 4l10 4v7c0 7-5 11-10 13C11 26 6 22 6 15V8z"/><path d="M12 16l3 3 6-6" stroke-linecap="round"/></svg>',
 free:'<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M5 15V6h9l13 13-9 9z"/><circle cx="10.5" cy="11" r="1.8"/></svg>',
 adapt:'<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="15" cy="5.5" r="2.5"/><path d="M15 9v8h8l3 7"/><path d="M12 13a8 8 0 1 0 9 10"/></svg>'
};
let mapR='30',mapSel=null;
const up=()=>T.filter(t=>t.sk!=='done');
const dleft=d=>Math.round((D(d)-D(TODAY))/864e5);
function dchip(s){const x=D(s);return '<div class="dchip"><span>'+x.toLocaleDateString(LOC,{weekday:'short'}).replace('.','')+'</span><b class="num">'+x.getDate()+'</b></div>'}
function openModal(i){fillDetail($('mdetail'),T[i],true);$('modal').hidden=false;document.body.classList.add('lock');$('mdetail').scrollTop=0;const c=$('mdetail').querySelector('[data-act=close]');if(c)c.focus()}
function closeModal(){if(!$('modal')||$('modal').hidden)return;$('modal').hidden=true;if(!$('detail').classList.contains('open'))document.body.classList.remove('lock')}
function goList(setup,keepRadius){
  inputs().forEach(i=>{if(i.id!=='city'&&(keepRadius?i.id!=='radius':true)&&i.type!=='checkbox')i.value=''});$('fpast').checked=true;qOn.clear();dayFilter=null;$('sort').value='date';provs();
  setup&&setup();if(here()&&$('radius').value)$('sort').value='dist';
  location.hash='lista';render();scrollTo({top:0});
}
function hcard(t){
  const k=km(t);
  return '<button class="hcard" data-i="'+t.i+'"><div class="cmap">'+greenSvg(hash(t.club||t.n))+dchip(t.s)+'</div><div class="cb"><span class="st '+t.sk+'">'+esc(t.ss)+'</span><h3>'+esc(t.n)+'</h3><span class="cp">'+esc([t.club,t.city].filter(Boolean).join(' - '))+'</span><div class="cf"><span class="num">'+(k!=null?(k<5?'&lt; 5 km':k+' km'):esc(t.prov!=='Por confirmar'?t.prov:t.ccaa))+'</span><b class="num">'+eur(t.price)+'</b></div></div></button>';
}
function renderHome(){
  if(!$('v-inicio'))return;
  const U=up(),h=here(),rad=+$('radius').value||0;
  const clubs=new Set(U.map(t=>t.club)).size;
  const weF=t=>inRange(t,WE[0]<TODAY?TODAY:WE[0],WE[1]);
  const weAll=U.filter(weF);
  const closing=U.filter(t=>t.sk==='open'&&t.cl&&t.cl>=TODAY&&t.cl<=add(TODAY,7));
  $('hLede').textContent=L('{n} torneos de federaciones y clubes de toda España, con su enlace de inscripción y actualizados cada mañana.',{n:U.length});
  $('hAll').textContent=U.length;
  $('hStats').innerHTML=[[weAll.length,'Este finde'],[U.filter(t=>t.sk==='open').length,'Inscripción abierta'],[closing.length,'Cierran esta semana'],[clubs,'Campos']].map(x=>'<div><b>'+x[0]+'</b><span>'+L(x[1])+'</span></div>').join('');
  // Este finde
  let we=weAll.slice();
  if(h){we=we.filter(t=>km(t)!=null&&(!rad||km(t)<=rad)).sort((a,b)=>km(a)-km(b))}
  else we.sort((a,b)=>(a.sk==='open'?0:1)-(b.sk==='open'?0:1)||(a.org==='Federación'?0:1)-(b.org==='Federación'?0:1)||a.s.localeCompare(b.s));
  const city=h?cityName():null;
  $('weTitle').textContent=h?(we.length?L(rad?'{n} este finde a menos de {r} km de {c}.':'{n} este finde cerca de {c}.',{n:cnt(we.length),r:rad,c:city}):L('Nada este finde cerca de {c}. Amplía la distancia.',{c:city})):L('Este fin de semana se juegan {n} torneos.',{n:weAll.length});
  $('weCards').innerHTML=we.slice(0,12).map(hcard).join('')+(we.length>12||!h?'<button class="hcard more" data-go="we"><b class="num">'+(h?we.length:weAll.length)+'</b>'+L('Ver todos los de este finde')+'</button>':'')||'';
  // Cierra pronto
  const cs=closing.slice().sort((a,b)=>a.cl.localeCompare(b.cl)||a.s.localeCompare(b.s));
  $('closeTitle').textContent=cs.length?L('{n} inscripciones cierran en 7 días.',{n:cs.length}):L('Ninguna inscripción cierra esta semana.');
  $('closing').innerHTML=cs.slice(0,6).map(t=>{const d=dleft(t.cl);return '<button class="crow" data-i="'+t.i+'"><span class="cd'+(d===0?' today':'')+'"><span>'+(d===0?'<b>'+L('Hoy')+'</b>':'<b class="num">'+d+'</b><span>'+L(d===1?'día':'días')+'</span>')+'</span></span><span><b>'+esc(t.n)+'</b><span class="s">'+esc(fWk(t.s)+' - '+[t.club,t.city].filter(Boolean).join(' - '))+'</span></span><span class="p num">'+eur(t.price)+'</span></button>'}).join('')||'<p class="empty">'+L('Vuelve en unos días: la lista se actualiza cada mañana.')+'</p>';
  // Explora por tipo
  const TL=[['senior','Senior','Mayores de 50 años',t=>t.cat==='Senior',()=>{$('fcat').value='Senior'}],
   ['juvenil','Juvenil','Benjamín a sub-18',t=>t.cat==='Juvenil',()=>{$('fcat').value='Juvenil'}],
   ['pp','Pitch & Putt','Recorridos cortos',t=>t.campo==='Pitch & Putt',()=>{$('fcampo').value='Pitch & Putt'}],
   ['parejas','Parejas','Fourball, greensome, scramble',t=>t.form==='Parejas',()=>{$('fform').value='Parejas'}],
   ['fem','Femenino','Damas y ligas femeninas',t=>t.sex==='Femenino',()=>{$('fsex').value='Femenino'}],
   ['fed','Federativos','Campeonatos y circuitos oficiales',t=>t.org==='Federación',()=>{$('forg').value='Federación'}],
   ['pro','Profesional','Pruebas de profesionales',t=>t.cat==='Profesional',()=>{$('fcat').value='Profesional'}],
   ['free','Gratis','Sin coste de inscripción',t=>t.price===0,()=>{qOn.add('free')}],
   ['adapt','Golf adaptado','Pruebas inclusivas',t=>t.cat==='Adaptado',()=>{$('fcat').value='Adaptado'}]];
  window._tiles=TL;
  $('tiles').innerHTML=TL.map((x,i)=>{const n=U.filter(x[3]).length;return n?'<button class="tile2" data-t="'+i+'">'+HI[x[0]]+'<b>'+L(x[1])+'</b><span>'+L(x[2])+'</span><em class="num">'+n+'</em></button>':''}).join('');
  // Grandes citas
  const big=U.filter(t=>t.src==='RFEG'||(t.org==='Federación'&&/campeonato|copa|open|cto\.?\s|final|gran premio|grand prix|internacional/i.test(t.n)&&/espa[ñn]a|andaluc|madrid|catal|comunitat|\bcv\b|galicia|asturias|balear|canarias|castilla|murcia|arag|navarr|vasco|euskadi|rioja|cantabr|extremad|internacional/i.test(t.n)))
   .sort((a,b)=>(a.src==='RFEG'?0:1)-(b.src==='RFEG'?0:1)||a.s.localeCompare(b.s)).slice(0,8).sort((a,b)=>a.s.localeCompare(b.s)).slice(0,4);
  $('events').innerHTML=big.map(t=>{const d=dleft(t.s);const c=d<=0?L(t.e>=TODAY?'En juego':'Hoy'):(d===1?L('Mañana'):L('Faltan {n} días',{n:d}));return '<button class="ev" data-i="'+t.i+'"><div class="emap">'+greenSvg(hash(t.n))+'<span class="count">'+c+'</span></div><div class="eb"><h3>'+esc(t.n)+'</h3><span class="s">'+esc((t.e!==t.s?fShort(t.s)+' – '+fShort(t.e):fWk(t.s))+' - '+[t.club,t.prov!=='Por confirmar'?t.prov:''].filter(Boolean).join(' - '))+'</span><span class="tag">'+esc(V(t.cat))+'</span></div></button>'}).join('');
  // 14 días
  const days=[...Array(14)].map((_,i)=>add(TODAY,i));const cnts=days.map(d=>U.filter(t=>inRange(t,d,d)).length);const mx=Math.max(1,...cnts);
  const tot=cnts.reduce((a,b)=>a+b,0);const bi=cnts.indexOf(Math.max(...cnts));
  $('stripTitle').textContent=LANG==='en'?fDay(days[bi]).replace(/^\w/,c=>c.toUpperCase())+' is the busiest day: '+cnts[bi]+' tournaments.':'El '+fDay(days[bi]).replace(/^\w/,c=>c.toLowerCase())+' es el día con más torneos: '+cnts[bi]+'.';
  $('strip').innerHTML=days.map((d,i)=>{const x=D(d);const w=x.getDay();return '<button class="sd'+(w===0||w===6?' we':'')+(d===TODAY?' today':'')+'" data-d="'+d+'" aria-label="'+fDay(d)+': '+cnt(cnts[i])+'"><span class="n">'+cnts[i]+'</span><span class="bar" style="height:'+Math.max(6,Math.round(cnts[i]/mx*120))+'px"></span><span class="w">'+x.toLocaleDateString(LOC,{weekday:'short'}).replace('.','')+'</span><span class="d">'+x.getDate()+'</span></button>'}).join('');
  // Banda de fuentes
  const ok=SRC.filter(s=>s.volcada).length;
  $('bandTxt').textContent=L('Cada mañana se revisan los calendarios públicos de plataformas de inscripción, federaciones y otros organizadores.')+' '+revText()+' '+L('Cada enlace se comprueba antes de publicarse. Banderín solo reúne esta información para que sea fácil de encontrar: los torneos son de sus organizadores y la inscripción se hace siempre en su web.');
  const sl=sealText();['hSeal','pSeal'].forEach(id=>{$(id).innerHTML='<i></i>'+esc(sl)});
  renderMap();
}
function mapSet(){const U=up();return mapR==='all'?U:U.filter(t=>t.s<=add(TODAY,+mapR))}
function renderMap(){
  const S=mapSet(),m=MAPA.meta;const pc={};S.forEach(t=>{pc[t.prov]=(pc[t.prov]||0)+1});const mx=Math.max(1,...Object.values(pc));
  const groups={};S.forEach(t=>{if(!t.ll)return;const k=t.club+'|'+t.ll.join(',');(groups[k]=groups[k]||{club:t.club,ll:t.ll,city:t.city,prov:t.prov,items:[]}).items.push(t)});
  const G=Object.values(groups).sort((a,b)=>b.items.length-a.items.length);window._mapG=G;
  let svg='<rect class="frame" x="'+m.frame[0]+'" y="'+m.frame[1]+'" width="'+m.frame[2]+'" height="'+m.frame[3]+'" rx="14"/>';
  svg+=MAPA.prov.map(p=>{const n=pc[p.n]||0;return '<path class="pv'+(mapSel&&mapSel.p===p.n?' on':'')+'" data-p="'+esc(p.n)+'" d="'+p.d+'" fill-opacity="'+(n?(0.12+0.5*Math.sqrt(n/mx)).toFixed(2):0.05)+'"><title>'+esc(p.n)+': '+cnt(n)+'</title></path>'}).join('');
  svg+=G.slice().reverse().map(g=>{const [x,y]=mp(g.ll[0],g.ll[1]);const sc=matchMedia('(max-width:700px)').matches?2:1;const r=Math.min(16,4.5+2.2*Math.sqrt(g.items.length))*sc;const on=mapSel&&mapSel.g===g.club+'|'+g.ll.join(',');return '<circle class="dot'+(on?' on':'')+'" data-g="'+esc(g.club+'|'+g.ll.join(','))+'" cx="'+x.toFixed(1)+'" cy="'+y.toFixed(1)+'" r="'+r.toFixed(1)+'"/>'}).join('');
  const top=G.slice(0,5);svg+=top.map(g=>{const [x,y]=mp(g.ll[0],g.ll[1]);return '<circle class="pulse go" cx="'+x.toFixed(1)+'" cy="'+y.toFixed(1)+'" r="10" style="transform-origin:'+x.toFixed(1)+'px '+y.toFixed(1)+'px"/>'}).join('');
  $('map').setAttribute('viewBox','0 0 '+m.w+' '+m.h);$('map').innerHTML=svg;
  renderSide(S,pc);
}
function mlist(items){return '<div class="mlist">'+items.slice(0,12).map(t=>{const x=D(t.s);return '<button data-i="'+t.i+'"><span class="md">'+x.toLocaleDateString(LOC,{weekday:'short'}).replace('.','')+'<em class="num">'+x.getDate()+'</em>'+x.toLocaleDateString(LOC,{month:'short'}).replace('.','')+'</span><span><b>'+esc(t.n)+'</b><span class="s">'+esc([t.club,t.ss].filter(Boolean).join(' - '))+'</span></span></button>'}).join('')+'</div>'}
function renderSide(S,pc){
  const el=$('mside');const rl=L(mapR==='all'?'en total':mapR==='30'?'en los próximos 30 días':'en los próximos 3 meses');
  if(mapSel&&mapSel.p){const items=S.filter(t=>t.prov===mapSel.p).sort((a,b)=>a.s.localeCompare(b.s));
    el.innerHTML='<button class="btn ghost back" data-back>← '+L('Toda España')+'</button><h3>'+esc(mapSel.p)+'</h3><p class="sub">'+cnt(items.length)+' '+rl+'</p>'+(items.length?mlist(items):'<p class="sub">'+L('Sin torneos en este periodo.')+'</p>')+(items.length?'<button class="btn primary" data-golist="p">'+L('Ver los {n} en la lista',{n:items.length})+'</button>':'');return}
  if(mapSel&&mapSel.g){const g=(window._mapG||[]).find(x=>x.club+'|'+x.ll.join(',')===mapSel.g);if(!g){mapSel=null;return renderSide(S,pc)}
    const items=g.items.slice().sort((a,b)=>a.s.localeCompare(b.s));
    el.innerHTML='<button class="btn ghost back" data-back>← '+L('Toda España')+'</button><h3>'+esc(g.club)+'</h3><p class="sub">'+esc([g.city,g.prov].filter(x=>x&&x!=='Por confirmar').join(' - '))+' - '+cnt(items.length)+' '+rl+'</p>'+mlist(items)+'<button class="btn primary" data-golist="g">'+L('Ver en la lista')+'</button>';return}
  const R=Object.entries(pc).filter(x=>x[0]&&x[0]!=='Por confirmar').sort((a,b)=>b[1]-a[1]).slice(0,10);const mx=R.length?R[0][1]:1;
  el.innerHTML='<h3>'+cnt(S.length)+' '+rl+'.</h3><p class="sub">'+L('Toca un punto para ver los torneos de ese campo, o una provincia para ver todos los suyos.')+'</p><div class="rank">'+R.map(([p,n])=>'<button data-prov="'+esc(p)+'"><span>'+esc(p)+'</span><span class="bar"><i style="width:'+Math.round(n/mx*100)+'%"></i></span><b class="num">'+n+'</b></button>').join('')+'</div>';
}
// Eventos de portada
$('hcity').innerHTML=$('city').innerHTML.replace(L('¿Desde dónde sales?'),L('Tu ciudad'));$('hcity').value=$('city').value;if($('radius').value)$('hrad').value=$('radius').value;
$('hForm').addEventListener('submit',e=>{e.preventDefault();$('city').value=$('hcity').value;$('radius').value=$('hcity').value?$('hrad').value:'';store.set('city',$('city').value);store.set('radius',$('radius').value);goList(()=>{qOn.add('we')},true)});
$('hcity').addEventListener('input',()=>{if(cityPick($('hcity')))return;$('city').value=$('hcity').value;store.set('city',$('city').value);if($('hcity').value&&!$('radius').value){$('radius').value=$('hrad').value;store.set('radius',$('radius').value)}render()});
$('hrad').addEventListener('input',()=>{if($('hcity').value){$('radius').value=$('hrad').value;store.set('radius',$('radius').value);render()}});
$('v-inicio').addEventListener('click',e=>{
  const b=e.target.closest('[data-i]');if(b&&!b.closest('#map')){openModal(+b.dataset.i);return}
  const go=e.target.closest('[data-go]');if(go){goList(()=>{qOn.add('we')},true);return}
  const tl=e.target.closest('[data-t]');if(tl){const x=window._tiles[+tl.dataset.t];goList(x[4]);return}
  const sd=e.target.closest('.sd');if(sd){goList(()=>{dayFilter=sd.dataset.d});return}
  const pv=e.target.closest('[data-prov]');if(pv){mapSel={p:pv.dataset.prov};renderMap();return}
  if(e.target.closest('[data-back]')){mapSel=null;renderMap();return}
  const gl=e.target.closest('[data-golist]');if(gl){const s=mapSel;goList(()=>{if(s.p){const t=T.find(x=>x.prov===s.p);if(t){$('fccaa').value=t.ccaa;provs();$('fprov').value=s.p}}else{$('q').value=s.g.split('|')[0]}if(mapR!=='all')$('fd2').value=add(TODAY,mapR==='30'?30:90)});return}
  const ra=e.target.closest('#mapRange a');if(ra){e.preventDefault();mapR=ra.dataset.r;document.querySelectorAll('#mapRange a').forEach(a=>a.classList.toggle('on',a===ra));renderMap();return}
});
$('map').addEventListener('click',e=>{const d=e.target.closest('.dot');if(d){mapSel={g:d.dataset.g};renderMap();if(mobile())$('mside').scrollIntoView({behavior:'smooth',block:'start'});return}const p=e.target.closest('.pv');if(p){mapSel={p:p.dataset.p};renderMap();if(mobile())$('mside').scrollIntoView({behavior:'smooth',block:'start'})}});
$('map').addEventListener('pointermove',e=>{const d=e.target.closest('.dot'),tip=$('mtip');if(!d){tip.hidden=true;return}const g=(window._mapG||[]).find(x=>x.club+'|'+x.ll.join(',')===d.dataset.g);if(!g){tip.hidden=true;return}
  tip.innerHTML='<b>'+esc(g.club)+'</b>'+esc([g.city,cnt(g.items.length)].filter(Boolean).join(' - '));tip.hidden=false;const r=$('map').closest('.mapbox').getBoundingClientRect();let x=e.clientX-r.left+14,y=e.clientY-r.top-10;if(x+tip.offsetWidth>r.width-8)x=e.clientX-r.left-tip.offsetWidth-14;tip.style.left=x+'px';tip.style.top=y+'px'});
$('map').addEventListener('pointerleave',()=>{$('mtip').hidden=true});
$('modal').addEventListener('click',e=>{if(e.target.classList.contains('mscrim'))closeModal()});
// Arte de la portada
(function(){$('hGreen').setAttribute('d',blob(452,192,92,1.1,.07,1.45));$('hRings').innerHTML=topo(452,192,16,13,77,1.45);
 if(matchMedia('(prefers-reduced-motion:reduce)').matches){try{$('heroArt').pauseAnimations()}catch(e){}}})();




/* ===== Vista «Mi perfil» ===== */
const CCAA_ALL=['Andalucía','Aragón','Canarias','Cantabria','Castilla y León','Castilla-La Mancha','Cataluña','Comunidad de Madrid','Comunidad Foral de Navarra','Comunitat Valenciana','Extremadura','Galicia','Illes Balears','La Rioja','País Vasco','Principado de Asturias','Región de Murcia','Ceuta','Melilla'];
const CLUBS=[...new Set(T.map(t=>t.club).filter(Boolean))].sort((a,b)=>a.localeCompare(b,'es'));
const PROVS=[...new Set(T.map(t=>t.prov).filter(p=>p&&p!=='Por confirmar'))].sort((a,b)=>a.localeCompare(b,'es'));
let pClubs=[];
{const y=new Date().getFullYear();$('pnac').innerHTML='<option value="">'+L('Sin indicar')+'</option>'+Array.from({length:y-1925-4},(_,i)=>y-5-i).map(v=>'<option>'+v+'</option>').join('')}
$('pfed').innerHTML='<option value="">'+L('Sin indicar')+'</option>'+CCAA_ALL.map(c=>'<option value="'+esc(c)+'">'+esc(V(c))+'</option>').join('');
$('pclubList').innerHTML=CLUBS.map(c=>'<option value="'+esc(c)+'">').join('');
$('pprovAdd').innerHTML='<option value="">'+L('Seguir una provincia')+'</option>'+PROVS.map(p=>'<option value="'+esc(p)+'">'+esc(p)+'</option>').join('');
$('psigo').dataset.empty=L('Aún no sigues ningún club ni provincia.');
$('prows').dataset.empty=L('Cuando sigas un club o una provincia, sus próximos torneos aparecerán aquí.');
function parseH(v){v=String(v||'').trim().replace(',','.');if(!v)return null;const plus=v.startsWith('+');const n=Number(v.replace('+',''));if(!isFinite(n))return NaN;const h=plus?-n:n;return h<-10||h>54?NaN:Math.round(h*10)/10}
function drawClubs(){$('pclubs').innerHTML=pClubs.map((c,i)=>'<span class="ptag">'+esc(c)+'<button type="button" data-i="'+i+'" aria-label="'+esc(L('Quitar {c}',{c}))+'">×</button></span>').join('')}
function calLinks(kind,name){const path='/cal/'+kind+'/'+slugify(name)+'.ics',web='webcal://'+location.host+path;
  return '<a href="'+esc(web)+'">'+L('Calendario')+'</a><a href="'+esc('https://calendar.google.com/calendar/r?cid='+encodeURIComponent(web))+'" target="_blank" rel="noopener noreferrer">Google</a>'}
function renderPerfil(){
  const P=PERF||{};
  $('phcp').value=P.hcp!=null?fmtH(P.hcp):'';$('phcp').removeAttribute('aria-invalid');$('phcpErr').hidden=true;
  $('pnac').value=P.nac||'';$('pfed').value=P.fed||'';
  document.querySelectorAll('input[name=psexo]').forEach(r=>r.checked=r.value===(P.sexo||''));
  pClubs=(P.clubs||[]).slice();drawClubs();
  $('pcity').innerHTML=$('city').innerHTML.replace(L('¿Desde dónde sales?'),L('Sin indicar'));$('pcity').value=$('city').value;$('pradius').value=$('radius').value;
  const up0=T.filter(t=>t.sk!=='done');
  const items=[...SIGO.prov.map(n=>['prov',n,up0.filter(t=>t.prov===n).length]),...SIGO.clubs.map(n=>['club',n,up0.filter(t=>t.club===n).length])];
  $('psigo').innerHTML=items.map(([k,n,c])=>'<li><span><b>'+esc(n)+'</b><small>'+L(k==='prov'?'Provincia':'Club')+' - '+cnt(c)+'</small></span><span class="pcal">'+(c?calLinks(k,n):'')+'<button type="button" data-k="'+k+'" data-n="'+esc(n)+'" aria-label="'+esc(L('Dejar de seguir {c}',{c:n}))+'">×</button></span></li>').join('');
  const fl=up0.filter(follows).sort((a,b)=>a.s.localeCompare(b.s)).slice(0,8);
  {let last='';$('prows').innerHTML=fl.length?'':'<p class="phint">'+L('Aún no sigues nada.')+' <button type="button" class="linkbtn" data-pgo="sigo">'+L('Sigue un club o una provincia')+'</button></p>';$('prows').innerHTML+=fl.map(t=>{const h=t.s!==last?'<div class="dhead"><b>'+fDay(t.s)+'</b>'+(weekTag(t.s)?'<span class="wk">'+weekTag(t.s)+'</span>':'')+'</div>':'';last=t.s;return h+row(t)}).join('')}
  const nf=hasPerf()?up0.filter(nofit).length:0;
  $('pmine').innerHTML='<a href="#lista" data-go="saved"><b>'+saved.size+'</b><span>'+L('Guardados')+'</span></a><a href="#resultados" data-go="played"><b>'+played.size+'</b><span>'+L('Jugados')+'</span></a>'+
    (hasPerf()?'<a href="#lista" data-go="fit"><b>'+(up0.length-nf)+'</b><span>'+L('Encajan contigo')+'</span></a>':'')+
    ((SIGO.clubs.length+SIGO.prov.length)?'<a href="#lista" data-go="sigo"><b>'+up0.filter(follows).length+'</b><span>'+L('De lo que sigues')+'</span></a>':'');
  $('pwipe').classList.remove('confirm');$('pwipe').textContent=L('Borrar mis datos de este dispositivo');
  markMe();pLayout();
}
/* Mi perfil: puerta de entrada (cuenta primero) y secciones con menú */
let PSEC='resumen';
function pSec(k,focus){PSEC=k;document.querySelectorAll('.pnav [data-ps]').forEach(b=>{const on=b.dataset.ps===k;b.setAttribute('aria-selected',on);b.tabIndex=on?0:-1;if(on&&focus)b.focus();if(on){const n=b.parentElement;if(n&&n.scrollWidth>n.clientWidth)n.scrollTo({left:Math.max(0,b.offsetLeft-n.clientWidth/2+b.offsetWidth/2),behavior:'smooth'})}});
  document.querySelectorAll('.ppane').forEach(p=>p.hidden=p.id!=='pp-'+k)}
function pHasLocal(){return !!(PERF||SIGO.clubs.length||SIGO.prov.length||saved.size||played.size||(AV&&AV.tok))}
function pSess(){try{return Object.keys(localStorage).some(k=>/^sb-.+-auth-token$/.test(k))}catch(e){return false}}
function pLayout(){
  const u=typeof USER!=='undefined'?USER:null,on=!!(window.CUENTA&&CUENTA.url&&CUENTA.key);
  const logged=!!u||pSess();
  const gate=on&&!logged&&!pHasLocal()&&!raw.get('sincuenta');
  $('pgate').hidden=!gate;$('pmain').hidden=gate;
  $('pban').hidden=!on||logged||gate;
  $('pdatos').hidden=!!u;
  $('plede').textContent=u?L('Todo se guarda en tu cuenta ({e}) y lo tienes en cualquier dispositivo.',{e:u.email||''}):L('Lo que sigues, tus avisos y tus torneos, en un solo sitio. Sin cuenta, se guarda solo en este dispositivo.');
  if(u&&$('pavEmail')&&!$('pavEmail').value)$('pavEmail').value=u.email||'';
}
$('pgSkip').onclick=()=>{raw.set('sincuenta',1);pLayout();window.scrollTo({top:0})};
document.querySelectorAll('.pnav [data-ps]').forEach(b=>b.onclick=()=>pSec(b.dataset.ps));
document.querySelector('.pnav').addEventListener('keydown',e=>{const k=[...document.querySelectorAll('.pnav [data-ps]')].map(b=>b.dataset.ps);let i=k.indexOf(PSEC);
  if(e.key==='ArrowRight'||e.key==='ArrowDown')i=(i+1)%k.length;else if(e.key==='ArrowLeft'||e.key==='ArrowUp')i=(i-1+k.length)%k.length;else return;e.preventDefault();pSec(k[i],true)});
$('v-perfil').addEventListener('click',e=>{const b=e.target.closest('[data-pgo]');if(b){pSec(b.dataset.pgo);window.scrollTo({top:0,behavior:'smooth'})}});
pSec('resumen');
function addClub(inp,list){const v=inp.value.trim();if(!v)return false;const m=CLUBS.find(c=>norm(c)===norm(v))||v;if(!list.includes(m))list.push(m);inp.value='';return true}
$('pclubAdd').onclick=()=>{if(addClub($('pclubIn'),pClubs))drawClubs()};
$('pclubIn').onkeydown=e=>{if(e.key==='Enter'){e.preventDefault();$('pclubAdd').click()}};
$('pclubs').onclick=e=>{const b=e.target.closest('button[data-i]');if(!b)return;pClubs.splice(+b.dataset.i,1);drawClubs()};
$('phcp').oninput=()=>{const h=parseH($('phcp').value);const bad=Number.isNaN(h);$('phcp').setAttribute('aria-invalid',String(bad));$('phcpErr').hidden=!bad};
$('pform').onsubmit=e=>{
  e.preventDefault();
  if($('pclubIn').value.trim())addClub($('pclubIn'),pClubs);
  const h=parseH($('phcp').value);
  if(Number.isNaN(h)){$('phcp').setAttribute('aria-invalid','true');$('phcpErr').hidden=false;$('phcp').focus();return}
  const sx=(document.querySelector('input[name=psexo]:checked')||{}).value||null;
  PERF={v:1,hcp:h,nac:+$('pnac').value||null,sexo:sx,fed:$('pfed').value||null,clubs:pClubs.slice(),ts:Date.now()};
  raw.set('perfil',PERF);if(typeof syncAvisos==='function')syncAvisos();
  if($('pcity').value==='gps'&&!GEO){geoPrev=$('city').value;locate(false)}else{$('city').value=$('pcity').value;store.set('city',$('city').value)}$('radius').value=$('pradius').value;store.set('radius',$('radius').value);
  if($('hcity'))$('hcity').value=$('city').value;
  render();renderPerfil();
  $('pstat').textContent=L('Perfil guardado.');setTimeout(()=>{$('pstat').textContent=''},3500);
};
$('pprovAdd').onchange=()=>{const v=$('pprovAdd').value;if(v&&!SIGO.prov.includes(v)){SIGO.prov.push(v);saveSigo()}$('pprovAdd').value='';renderPerfil();renderQuick()};
$('psclubAdd').onclick=()=>{if(addClub($('psclubIn'),SIGO.clubs)){saveSigo();renderPerfil();renderQuick()}};
$('psclubIn').onkeydown=e=>{if(e.key==='Enter'){e.preventDefault();$('psclubAdd').click()}};
$('psigo').onclick=e=>{const b=e.target.closest('button[data-k]');if(!b)return;toggleFollow(b.dataset.k==='prov'?'prov':'clubs',b.dataset.n);renderPerfil();renderQuick()};
$('prows').onclick=e=>{const r=e.target.closest('.row');if(r)openModal(+r.dataset.i)};
$('pmine').onclick=e=>{const a=e.target.closest('a[data-go]');if(!a)return;const g=a.dataset.go;
  if(g==='played'){rMode='mine';document.querySelectorAll('#rmode a').forEach(x=>x.classList.toggle('on',x.dataset.m==='mine'));return}
  e.preventDefault();goList(()=>{qOn.add(g)});location.hash='lista'};
$('pwipe').onclick=()=>{const b=$('pwipe');
  if(!b.classList.contains('confirm')){b.classList.add('confirm');b.textContent=L('Pulsa otra vez para borrarlo todo');return}
  if(AV&&AV.tok&&avOn)api('/api/avisos/baja',{method:'POST',tok:AV.tok}).catch(()=>{});AV=null;
  ['perfil','sigo','saved','played','city','radius','avisos'].forEach(k=>{raw.del(k);delete MEM[k]});drawAvisos();
  PERF=null;SIGO={v:1,clubs:[],prov:[]};saved.clear();played.clear();$('city').value='';$('radius').value='';
  render();renderPerfil();$('pstat').textContent='';b.textContent=L('Datos borrados de este dispositivo.');
};
markMe();

/* ===== Textos legales ===== */
function renderLegal(k){
  const d=(LANG==='en'&&window.LEGALDOCS_EN&&window.LEGALDOCS_EN[k])||(window.LEGALDOCS||{})[k];if(!d)return;const T0=window.TITULAR||{};
  const pend='<span class="pend">'+L('Pendiente')+'</span>';
  const val=x=>T0[x]?esc(T0[x]):pend;
  const mail=T0.email?'<a href="mailto:'+esc(T0.email)+'">'+esc(T0.email)+'</a>':L('nuestro correo de contacto')+' '+pend;
  let h=d.html.replace(/\{\{registro_li\}\}/g,T0.registro?'<li><span>'+L('Datos registrales')+'</span><b>'+esc(T0.registro)+'</b></li>':'')
    .replace(/<b>\{\{email\}\}<\/b>/g,'<b>'+val('email')+'</b>')
    .replace(/\{\{email\}\}/g,mail)
    .replace(/\{\{(nombre|nif|domicilio)\}\}/g,(m,x)=>val(x))
    .replace(/\{\{marca\}\}/g,esc(T0.marca||'Esclusa'));
  h=h.replace(/<table class="tabla">/g,'<div class="tablewrap"><table class="tabla">').replace(/<\/table>/g,'</table></div>');
  const up=window.LEGAL_ACTUALIZADO?D(window.LEGAL_ACTUALIZADO).toLocaleDateString(LOC,{day:'numeric',month:'long',year:'numeric'}):'';
  $('ldoc').innerHTML='<p class="eyebrow">Legal</p><h1>'+esc(d.titulo)+'</h1><p class="lintro">'+esc(d.intro)+'</p>'+h+'<p class="lupd">'+L('Última actualización')+': '+up+'.</p>';
  document.querySelectorAll('.lnav a').forEach(a=>a.classList.toggle('on',a.getAttribute('href')==='#'+k));const on=document.querySelector('.lnav a.on');if(on&&innerWidth<900){const n=on.parentNode;n.scrollLeft=on.offsetLeft-(n.clientWidth-on.offsetWidth)/2}
  document.title=d.titulo+' - Banderín';
}
$('fyear').textContent=new Date().getFullYear();
$('fcontact').onclick=e=>{e.preventDefault();const m=(window.TITULAR||{}).email;if(m)location.href='mailto:'+m+'?subject='+encodeURIComponent(L('Corrección de un torneo en Banderín'));else location.hash='aviso-legal'};
addEventListener('hashchange',()=>{if(!(window.LEGALDOCS||{})[location.hash.slice(1)])document.title=TITLE0});
const TITLE0=document.title;

/* ===== Consentimiento ===== */
function applyConsent(pref){
  raw.set('consent',{v:1,pref:!!pref,ts:Date.now()});
  if(pref){PREF_KEYS.forEach(k=>{if(k in MEM)raw.set(k,MEM[k])})}
  else{PREF_KEYS.forEach(k=>raw.del(k))}
  $('cbanner').hidden=true;closeCookies();
}
let cLast=null;
function openCookies(){cLast=document.activeElement;$("cpref").checked=consent.pref();$('cpanel').hidden=false;$('cpanel').querySelector('.cbox button,.cbox input').focus()}
function closeCookies(){if($('cpanel').hidden)return;$('cpanel').hidden=true;if(cLast&&cLast.focus)cLast.focus()}
document.addEventListener('click',e=>{
  const t=e.target.closest('[data-cookies]');if(t){e.preventDefault();openCookies();return}
  const b=e.target.closest('[data-c]');if(!b)return;const a=b.dataset.c;
  if(a==='accept')applyConsent(true);else if(a==='reject')applyConsent(false);
  else if(a==='save')applyConsent($('cpref').checked);else if(a==='config')openCookies();else if(a==='close')closeCookies();
});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!$('cpanel').hidden){e.stopPropagation();closeCookies()}},true);
if(!consent.get())$('cbanner').hidden=false;

/* ===== Avisos por correo (fase 2). Apagados hasta que /api/estado diga lo contrario. ===== */
let AV=raw.get('avisos')||null,avOn=false,avTimer=null;
const avSigo=()=>({clubs:SIGO.clubs,prov:SIGO.prov,torneos:[...saved]});
const avPerfil=()=>PERF?{sexo:PERF.sexo,nac:PERF.nac,hcp:PERF.hcp,fed:PERF.fed,clubs:PERF.clubs}:null;
async function api(path,opt={}){
  const h={'Accept':'application/json'};if(opt.body)h['Content-Type']='application/json';if(opt.tok)h['Authorization']='Bearer '+opt.tok;
  const r=await fetch(path,{method:opt.method||'GET',headers:h,body:opt.body?JSON.stringify(opt.body):undefined,credentials:'same-origin'});
  let d=null;try{d=await r.json()}catch(e){}
  return {ok:r.ok,status:r.status,data:d};
}
function drawAvisos(){const ce=window.cuEmail&&window.cuEmail();if(ce){if($('pavEmail')&&!$('pavEmail').value)$('pavEmail').value=ce;if($('avPopEmail')&&!$('avPopEmail').value)$('avPopEmail').value=ce}
  const st=!avOn?'off':AV&&AV.tok?'on':AV&&AV.pend?'pend':'form';
  $('pavSoon').hidden=st!=='off';$('pavOff').hidden=st!=='off';$('pavForm').hidden=st!=='form';$('pavPend').hidden=st!=='pend';$('pavOn').hidden=st!=='on';
  if(st==='pend')$('pavPendMail').textContent=AV.pend;
  if(st==='on')$('pavOnMail').textContent=AV.email||'';
}
function syncAvisos(){if(!avOn||!AV||!AV.tok)return;clearTimeout(avTimer);avTimer=setTimeout(async()=>{
  const r=await api('/api/avisos/seguimientos',{method:'PUT',tok:AV.tok,body:{sigo:avSigo(),perfil:avPerfil()}}).catch(()=>null);
  if(r&&r.status===401){AV=null;raw.del('avisos');drawAvisos()}},800)}
async function initAvisos(){
  // Vuelta desde el correo de confirmación o de gestión: #perfil?avisos=<llave>
  const m=/^#perfil\?avisos=([^&]+)/.exec(location.hash);
  if(m){AV={tok:decodeURIComponent(m[1])};raw.set('avisos',AV);history.replaceState(null,'',location.pathname+'#perfil')}
  const r=await api('/api/estado').catch(()=>null);
  avOn=!!(r&&r.ok&&r.data&&r.data.avisos);
  if(avOn&&AV&&AV.tok){
    const y=await api('/api/avisos/yo',{tok:AV.tok}).catch(()=>null);
    if(y&&y.ok){AV.email=y.data.email;raw.set('avisos',AV);
      // Lo que sigue en el servidor se suma a lo de este navegador (útil en un segundo dispositivo)
      const s=y.data.sigo||{};let ch=false;
      (s.clubs||[]).forEach(c=>{if(!SIGO.clubs.includes(c)){SIGO.clubs.push(c);ch=true}});
      (s.prov||[]).forEach(c=>{if(!SIGO.prov.includes(c)){SIGO.prov.push(c);ch=true}});
      (s.torneos||[]).forEach(u=>{if(!saved.has(u)){saved.add(u);ch=true}});
      if(ch){raw.set('sigo',SIGO);store.set('saved',[...saved]);render()}
      syncAvisos();
    }else if(y&&y.status===401){AV=null;raw.del('avisos')}
  }
  drawAvisos();if(location.hash==='#perfil')renderPerfil();
  avPopSchedule();
}
// Con cuenta y el mismo correo: se activan al momento, sin correo de confirmación (Supabase ya lo verificó).
async function avCuenta(em){try{const c=window.cuSesion&&await window.cuSesion();if(!c||c.email.toLowerCase()!==em.toLowerCase())return false;
  const r=await api('/api/avisos/cuenta',{method:'POST',tok:c.tok,body:{idioma:LANG,sigo:avSigo(),perfil:avPerfil()}});
  if(!r||!r.ok||!r.data||!r.data.tok)return false;AV={tok:r.data.tok,email:r.data.email};raw.set('avisos',AV);syncAvisos();return true}catch(e){return false}}
$('pavForm').onsubmit=async e=>{
  e.preventDefault();const em=$('pavEmail').value.trim(),btn=$('pavForm').querySelector('button');
  $('pavErr').hidden=true;
  if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em)){$('pavErr').textContent=L('Revisa el correo: no parece válido.');$('pavErr').hidden=false;$('pavEmail').focus();return}
  btn.disabled=true;
  const c=await avCuenta(em);if(c){btn.disabled=false;drawAvisos();avFabSync();geoMsg(L('Avisos activados con tu cuenta.'));return}const r=await api('/api/avisos/alta',{method:'POST',body:{email:em,idioma:LANG,sigo:avSigo(),perfil:avPerfil(),web:$('pavWeb').value,ts:window.botToken?await botToken():''}}).catch(()=>null);
  btn.disabled=false;
  if(r&&r.ok){AV={pend:em};raw.set('avisos',AV);drawAvisos();avFabSync()}
  else{$('pavErr').textContent=L(r&&r.status===400?'Revisa el correo: no parece válido.':r&&r.status===429?'Demasiados intentos seguidos. Espera un rato y vuelve a probar.':'No hemos podido activarlos ahora. Inténtalo en unos minutos.');$('pavErr').hidden=false}
};
$('pavRetry').onclick=()=>{AV=null;raw.del('avisos');drawAvisos();avFabSync();$('pavEmail').focus()};
$('pavStop').onclick=async()=>{const b=$('pavStop');
  if(!b.classList.contains('confirm')){b.classList.add('confirm');b.textContent=L('Pulsa otra vez para borrar tu correo');return}
  const r=await api('/api/avisos/baja',{method:'POST',tok:AV&&AV.tok}).catch(()=>null);
  if(r&&(r.ok||r.status===401)){AV=null;raw.del('avisos');b.classList.remove('confirm');b.textContent=L('Desactivar avisos');drawAvisos();avFabSync()}
};

/* ===== Avisos: bolita en la esquina y ventana a los 5 segundos ===== */
// Se enseña una vez; si se cierra no vuelve en 30 días (banderin.avpop, preferencia de interfaz).
function avPopProvs(){const cur=(SIGO.prov[0])||(PERF&&PERF.prov)||cityProv()||'';
  $('avPopProv').innerHTML='<option value="">'+L('¿De qué provincia quieres avisos?')+'</option>'+PROVS.map(p=>'<option value="'+esc(p)+'"'+(p===cur?' selected':'')+'>'+esc(p)+'</option>').join('')}
function cityProv(){const c=$('city')&&$('city').value;if(!c)return'';if(c==='gps'){if(!GEO)return'';let b=null,bd=1e9;PROV.forEach(p=>{const d=hav(GEO,[p[2],p[3]]);if(d<bd){bd=d;b=p}});const tx=b?b[0]:'';return PROVS.find(p=>tx.indexOf(p)>=0)||''}const o=$('city').selectedOptions[0];const tx=o?o.textContent:'';return PROVS.find(p=>tx.indexOf(p)>=0)||''}
function avFabSync(){const show=avOn&&!(AV&&(AV.tok||AV.pend))&&$('avPop').hidden;$('avFab').hidden=!show}
function avPopOpen(auto){
  if(!avOn||(AV&&(AV.tok||AV.pend)))return;
  avPopProvs();$('avPopBody').hidden=false;$('avPopOk').hidden=true;$('avPopErr').hidden=true;
  $('avPop').hidden=false;avFabSync();
  if(!auto)setTimeout(()=>$('avPopEmail').focus(),50);
}
function avPopClose(remember){$('avPop').hidden=true;if(remember)raw.set('avpop',Date.now());avFabSync()}
function avPopSchedule(){
  avFabSync();
  if(!avOn||(AV&&(AV.tok||AV.pend)))return;
  const last=+raw.get('avpop')||0;if(Date.now()-last<30*864e5)return;
  let waited=0;const tick=()=>{
    const busy=!$('cbanner').hidden||document.body.classList.contains('lock')||/^#(aviso-legal|privacidad|cookies|terminos|perfil)/.test(location.hash);
    if(busy){waited=0;setTimeout(tick,1000);return}
    waited+=1;if(waited<5){setTimeout(tick,1000);return}
    if($('avPop').hidden)avPopOpen(true);
  };setTimeout(tick,1000);
}
$('avFab').onclick=()=>avPopOpen(false);
$('avPopX').onclick=()=>avPopClose(true);
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!$('avPop').hidden)avPopClose(true)});
$('avPopForm').onsubmit=async e=>{
  e.preventDefault();const em=$('avPopEmail').value.trim(),pv=$('avPopProv').value,btn=$('avPopForm').querySelector('button');
  $('avPopErr').hidden=true;
  if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em)){$('avPopErr').textContent=L('Revisa el correo: no parece válido.');$('avPopErr').hidden=false;$('avPopEmail').focus();return}
  if(!pv){$('avPopErr').textContent=L('Elige una provincia para saber de qué avisarte.');$('avPopErr').hidden=false;$('avPopProv').focus();return}
  if(!SIGO.prov.includes(pv)){SIGO.prov.push(pv);SIGO.ts=Date.now();raw.set('sigo',SIGO);markMe()}
  btn.disabled=true;
  const c=await avCuenta(em);if(c){btn.disabled=false;drawAvisos();renderQuick();avPopClose(true);geoMsg(L('Avisos activados con tu cuenta.'));return}const r=await api('/api/avisos/alta',{method:'POST',body:{email:em,idioma:LANG,sigo:avSigo(),perfil:avPerfil(),web:$('avPopWeb').value,ts:window.botToken?await botToken():''}}).catch(()=>null);
  btn.disabled=false;
  if(r&&r.ok){AV={pend:em};raw.set('avisos',AV);drawAvisos();renderQuick();$('avPopBody').hidden=true;$('avPopOk').hidden=false;raw.set('avpop',Date.now());setTimeout(()=>avPopClose(false),9000)}
  else{$('avPopErr').textContent=L(r&&r.status===400?'Revisa el correo: no parece válido.':r&&r.status===429?'Demasiados intentos seguidos. Espera un rato y vuelve a probar.':'No hemos podido activarlos ahora. Inténtalo en unos minutos.');$('avPopErr').hidden=false}
};
initAvisos();

// Arranque: al final, cuando todo está definido
addEventListener('hashchange',()=>{if(/^#t=/.test(location.hash))openShared();else route()});route();render();openShared();
