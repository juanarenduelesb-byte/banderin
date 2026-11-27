const $=id=>document.getElementById(id),cl=(x,a=0,b=1)=>Math.max(a,Math.min(b,x)),seg=(t,a,b)=>cl((t-a)/(b-a));
const eo=x=>1-Math.pow(1-x,3),eio=x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2,back=x=>{const c=1.7;return 1+(c+1)*Math.pow(x-1,3)+c*Math.pow(x-1,2)};
// visibilidad de una escena/elemento entre a y b con entrada y salida
function vis(t,a,b,fi=.25,fo=.25){return Math.min(eo(seg(t,a,a+fi)),1-eo(seg(t,b-fo,b)))}
// texto que entra con rebote
function pop(el,t,a,b,dy=40){const v=vis(t,a,b,.12,.15),p=back(seg(t,a,a+.38));el.style.opacity=v;el.style.transform=`translateY(${(1-p)*dy}px) scale(${.88+.12*p})`}
// toque
function tapAt(el,t,tt,x,y){const q=seg(t,tt-.3,tt+.55);if(t>tt-.3&&t<tt+.55){el.style.left=x+'px';el.style.top=y+'px';el.style.opacity=q<.35?1:1-(q-.35)/.65;el.style.transform=`scale(${q<.35?1-.25*(q/.35):.75+1.1*(q-.35)})`;return true}return false}
function endCard(t,E,DUR){const e=$('end');e.style.opacity=eo(seg(t,E,E+.35));
  e.querySelector('img').style.transform=`scale(${.5+.5*back(seg(t,E+.1,E+.6))})`;
  const h=eo(seg(t,E+.4,E+.9));e.querySelector('h2').style.opacity=h;e.querySelector('h2').style.transform=`translateY(${(1-h)*40}px)`;
  const u=back(seg(t,E+.95,E+1.4)),U=e.querySelector('.u');U.style.opacity=cl(seg(t,E+.95,E+1.1));U.style.transform=`scale(${.8+.2*u})`;
  e.querySelector('p').style.opacity=eo(seg(t,E+1.4,E+1.9));document.body.style.opacity=1-seg(t,DUR-.3,DUR)}
function flash(t,list){$('flash').style.opacity=Math.max(0,...list.map(a=>t>=a&&t<a+.15?.5*(1-seg(t,a,a+.15)):0))}
