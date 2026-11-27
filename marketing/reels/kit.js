// Kit compartido de los reels de Banderín: utilidades, subtítulos grandes y tarjeta final
const $=id=>document.getElementById(id),cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)),seg=(t,a,b)=>cl((t-a)/(b-a));
const eo=x=>1-Math.pow(1-x,3),eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2,back=x=>{const c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
const V=x=>0.3+x/1.08; // tiempo de la voz (bruta) -> tiempo del vídeo
document.head.insertAdjacentHTML('beforeend',`<style>
@font-face{font-family:"PS";font-weight:400;src:url(/fonts/public-sans-latin-400-normal.woff2)}
@font-face{font-family:"PS";font-weight:500;src:url(/fonts/public-sans-latin-500-normal.woff2)}
@font-face{font-family:"PS";font-weight:600;src:url(/fonts/public-sans-latin-600-normal.woff2)}
@font-face{font-family:"PS";font-weight:700;src:url(/fonts/public-sans-latin-700-normal.woff2)}
@font-face{font-family:"CAS";src:url(/fonts/libre-caslon-display-latin-400-normal.woff2)}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1920px;overflow:hidden;background:radial-gradient(110% 80% at 50% 30%,#1F5139,#123323 55%,#071710);font-family:"PS",sans-serif;color:#F4F1E8}
.cap{position:absolute;left:60px;right:60px;text-align:center;font-family:"CAS";font-size:92px;line-height:1.04;z-index:50;text-shadow:0 8px 40px rgba(0,0,0,.45)}
.cap .g{color:#E9C77E}.cap .r{color:#FF8A7A}
.pill{display:inline-block;font-family:"PS";font-weight:700;font-size:40px;letter-spacing:.08em;border-radius:999px;padding:10px 30px}
#end{position:absolute;inset:0;opacity:0;z-index:100;background:radial-gradient(110% 80% at 50% 40%,#1F5139,#123323 55%,#071710);text-align:center}
#end img{width:230px;height:230px;border-radius:54px;margin-top:470px;box-shadow:0 30px 80px rgba(0,0,0,.45)}
#end h2{font-family:"CAS";font-weight:400;font-size:112px;line-height:1.02;margin:56px 70px 0}#end h2 span{color:#E9C77E}
#end .u{display:inline-block;margin-top:66px;font-weight:700;font-size:82px;letter-spacing:-.02em;background:#F4F1E8;color:#163D2B;border-radius:999px;padding:30px 70px}
#end p{margin-top:40px;font-size:38px;color:#B9C9BE;font-weight:500}
#tap{position:absolute;width:140px;height:140px;margin:-70px 0 0 -70px;border-radius:50%;border:7px solid rgba(255,255,255,.95);background:rgba(255,255,255,.25);opacity:0;z-index:90}
</style>`);
function kitEnd(h,p){document.body.insertAdjacentHTML('beforeend',`<div id="end"><img src="/icons/icon-512.png" alt=""><h2>${h}</h2><div class="u">banderin.es</div><p>${p}</p></div><div id="tap"></div>`)}
function endRender(t,END,DUR){const e=$('end');e.style.opacity=eo(seg(t,END,END+.35));
  e.querySelector('img').style.transform=`scale(${.5+.5*back(seg(t,END+.1,END+.6))})`;
  e.querySelector('h2').style.opacity=eo(seg(t,END+.4,END+.9));e.querySelector('h2').style.transform=`translateY(${(1-eo(seg(t,END+.4,END+.9)))*40}px)`;
  const u=e.querySelector('.u');u.style.opacity=cl(seg(t,END+.9,END+1.1));u.style.transform=`scale(${.8+.2*back(seg(t,END+.9,END+1.4))})`;
  e.querySelector('p').style.opacity=eo(seg(t,END+1.4,END+1.9));document.body.style.opacity=1-seg(t,DUR-.3,DUR)}
// subtítulos: lista [inicio, fin, html]; entra con rebote, sale con fundido
function capRender(el,t,L){const c=L.find(c=>t>=c[0]&&t<c[1]);
  if(!c){el.style.opacity=0;return}
  if(el.dataset.k!=c[0]){el.dataset.k=c[0];el.innerHTML=c[2]}
  const p=back(seg(t,c[0],c[0]+.35));el.style.opacity=Math.min(cl(seg(t,c[0],c[0]+.12)),1-seg(t,c[1]-.12,c[1]));
  el.style.transform=`translateY(${(1-p)*40}px) scale(${.9+.1*p})`}
function tapAt(t,list){const tp=$('tap');for(const [tt,x,y] of list){if(t>tt-.3&&t<tt+.5){const q=seg(t,tt-.3,tt+.5);tp.style.left=x+'px';tp.style.top=y+'px';tp.style.opacity=q<.4?1:1-(q-.4)/.6;tp.style.transform=`scale(${q<.4?1-.3*(q/.4):.7+1*(q-.4)})`;return}}tp.style.opacity=0}
