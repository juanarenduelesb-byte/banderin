/* Banderín — green en 3D de la portada (Three.js r128, servido desde /vendor).
   Green elevado con franjas de corte, búnkeres hundidos, hoyo con profundidad, bandera de tela,
   luz de atardecer con sombras y un putt que rompe y entra. Si no hay WebGL o Three.js no carga,
   se queda el SVG de siempre (#heroArt), que sigue en la página como respaldo. */
(function(){
  const cv=document.getElementById('green3d');if(!cv)return;
  let ok=false;try{const t=document.createElement('canvas');ok=!!(window.WebGLRenderingContext&&(t.getContext('webgl')||t.getContext('experimental-webgl')))}catch(e){}
  if(!ok)return;
  const go=()=>{if(window.THREE)return init();const s=document.createElement('script');s.src='/vendor/three.min.js?v=r128';s.async=true;s.onload=init;document.head.append(s)};
  const idle=window.requestIdleCallback||(f=>setTimeout(f,300));
  go();
function init(){
  if(!window.THREE)return;
  const RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const T=THREE;
  const mobile=matchMedia('(max-width:900px)').matches;

  /* ---------- mundo ---------- */
  const SIZE=12, GC={x:.3,z:-.4}, CUP={x:.55,z:-.75}, CUP_R=.095, BALL_R=.064;
  const wob=(a,s)=>1+.09*Math.sin(2*a+s)+.055*Math.sin(3*a+s*2.1)+.03*Math.cos(5*a+s*.7);
  const rel=(x,z,cx,cz,rx,rz,s,rot=0)=>{let dx=x-cx,dz=z-cz;if(rot){const c=Math.cos(rot),n=Math.sin(rot);[dx,dz]=[dx*c-dz*n,dx*n+dz*c]}const a=Math.atan2(dz/rz,dx/rx);return Math.hypot(dx/rx,dz/rz)/wob(a,s)};
  const ss=(a,b,x)=>{const t=Math.min(1,Math.max(0,(x-a)/(b-a)));return t*t*(3-2*t)};
  const relG=(x,z)=>rel(x,z,GC.x,GC.z,1.6,1.12,.6);
  const relA=(x,z)=>rel(x,z,-.9,1.1,2.6,1.9,1.9,.35);
  const B1=(x,z)=>rel(x,z,2.05,.4,.52,.3,.4,-.5);
  const B2=(x,z)=>rel(x,z,-1.35,-1.5,.46,.24,1.3,.3);
  const B3=(x,z)=>rel(x,z,1.75,-1.75,.3,.2,2.2,.8);
  function H(x,z){
    let h=.06*Math.sin(x*.8+.3)*Math.cos(z*.6)+.04*Math.sin(z*1.3+x*.4);
    const g=relG(x,z);
    h+=.07*(1-ss(.92,1.2,g));                                      // meseta del green
    h+=(1-ss(.85,1.05,g))*(.045*(-(x-GC.x)*.35+(z-GC.z)*.28)+.035*Math.exp(-((x+.25)**2+(z+.05)**2)*2.2)); // caídas del green
    [B1,B2,B3].forEach(b=>{const r=b(x,z);h-=.24*(1-ss(.45,1,r));h+=.045*Math.exp(-((r-1.08)**2)*55)}); // búnker hundido + labio
    return h}

  /* ---------- textura pintada (albedo) ---------- */
  const N=mobile?1536:2048;
  const tex=document.createElement('canvas');tex.width=tex.height=N;const tx=tex.getContext('2d');
  const img=tx.createImageData(N,N),D=img.data;
  const hash=(x,y)=>{const s=Math.sin(x*127.1+y*311.7)*43758.5453;return s-Math.floor(s)};
  const mix=(a,b,t)=>[a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t,a[2]+(b[2]-a[2])*t];
  const ROUGH=[22,58,35],APP=[34,84,50],FRINGE=[38,98,52],GREEN=[52,132,64],SAND=[214,192,146],SAND_D=[176,150,104];
  for(let py=0;py<N;py++){const z=py/N*SIZE-SIZE/2;
    for(let px=0;px<N;px++){const x=px/N*SIZE-SIZE/2;
      const n=hash(px,py),n2=hash(px*.13|0,py*.13|0);
      let c=ROUGH.slice();c=mix(c,[18,52,31],n2*.5);
      const a=relA(x,z);if(a<1){const st=Math.floor((x*.55+z*.83)/.42)&1;let f=mix(APP,[40,94,56],st);c=mix(c,f,ss(1.05,.8,a))}
      const g=relG(x,z);
      if(g<1.13){c=mix(c,FRINGE,ss(1.13,1.04,g))}
      if(g<1){const st=Math.floor((x*.62-z*.78)/.26)&1;let gc=mix(GREEN,[74,154,84],st*.8);
        gc=mix(gc,[70,132,80],ss(.75,1,g)*.5);c=mix(c,gc,ss(1,.985,g));
        // curvas de nivel doradas (esencia Banderín)
        const hh=H(x,z)*55;const fr=Math.abs(hh-Math.round(hh));if(fr<.045&&g<.97)c=mix(c,[210,190,130],.22*(1-fr/.045))}
      [B1,B2,B3].forEach(b=>{const r=b(x,z);if(r<1.12){if(r>1&&r<1.12)c=mix(c,[30,70,40],.35*(1-(r-1)/.12));
        if(r<1){let s=mix(SAND,[238,222,184],n2);s=mix(s,SAND_D,ss(.72,1,r)*.9);const rake=Math.sin((x*.7+z*.71)*95+Math.sin(z*7)*1.5);s=mix(s,[200,178,130],(rake>.85)*.25);c=mix(s,c,ss(.98,1,r))}}});
      const k=(n-.5)*14;const i=(py*N+px)*4;D[i]=c[0]+k;D[i+1]=c[1]+k;D[i+2]=c[2]+k*.6;D[i+3]=255}}
  tx.putImageData(img,0,0);

  /* ---------- render ---------- */
  const renderer=new T.WebGLRenderer({canvas:cv,antialias:true,powerPreference:'high-performance'});
  const bgCol=()=>{const c=getComputedStyle(cv.closest('.hero')).backgroundColor.match(/\d+/g)||[14,42,30];return new T.Color(`rgb(${c[0]},${c[1]},${c[2]})`)};
  renderer.setPixelRatio(Math.min(devicePixelRatio||1,mobile?1.5:2));
  renderer.outputEncoding=T.sRGBEncoding;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=.88;
  renderer.shadowMap.enabled=true;renderer.shadowMap.type=T.PCFSoftShadowMap;renderer.setClearColor(bgCol(),1);
  const scene=new T.Scene();scene.fog=new T.Fog(bgCol(),7.5,13);
  const syncBg=()=>{const c=bgCol();renderer.setClearColor(c,1);scene.fog.color.copy(c)};
  new MutationObserver(syncBg).observe(document.documentElement,{attributes:true,attributeFilter:['data-theme','class']});matchMedia('(prefers-color-scheme:dark)').addEventListener('change',syncBg);
  const cam=new T.PerspectiveCamera(30,1,.05,40);

  // luz de atardecer
  scene.add(new T.HemisphereLight(0xfff1d6,0x0b2318,.42));
  const sun=new T.DirectionalLight(0xffdcae,1.9);sun.position.set(4.2,6.4,-2.6);sun.castShadow=true;
  sun.shadow.mapSize.set(mobile?2048:4096,mobile?2048:4096);Object.assign(sun.shadow.camera,{left:-7,right:7,top:7,bottom:-7,near:.5,far:22});sun.shadow.bias=-.0004;sun.shadow.normalBias=.02;sun.shadow.radius=3;
  sun.target.position.set(.3,0,-.4);scene.add(sun,sun.target);
  const fill=new T.DirectionalLight(0x9fc9ff,.22);fill.position.set(-4,2,4);scene.add(fill);
  const pool=new T.SpotLight(0xfff0cc,.85,0,.45,1,1.2);pool.position.set(.6,7,-.2);pool.target.position.set(.35,0,-.5);scene.add(pool,pool.target);

  // terreno
  const seg=mobile?220:320;
  const geo=new T.PlaneGeometry(SIZE,SIZE,seg,seg);geo.rotateX(-Math.PI/2);
  const pos=geo.attributes.position;for(let i=0;i<pos.count;i++){pos.setY(i,H(pos.getX(i),pos.getZ(i)))}geo.computeVertexNormals();
  const map=new T.CanvasTexture(tex);map.encoding=T.sRGBEncoding;map.anisotropy=renderer.capabilities.getMaxAnisotropy();
  const mat=new T.MeshStandardMaterial({map,roughness:.92,metalness:0});
  mat.onBeforeCompile=sh=>{sh.uniforms.uCup={value:new T.Vector3(CUP.x,CUP.z,CUP_R)};
    sh.vertexShader=sh.vertexShader.replace('#include <common>','#include <common>\nvarying vec3 vW;').replace('#include <worldpos_vertex>','#include <worldpos_vertex>\nvW=(modelMatrix*vec4(transformed,1.)).xyz;');
    sh.fragmentShader=sh.fragmentShader.replace('#include <common>','#include <common>\nvarying vec3 vW;uniform vec3 uCup;float hs(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}')
      .replace('void main() {','void main() {\nif(distance(vW.xz,uCup.xy)<uCup.z)discard;')
      .replace('#include <map_fragment>','#include <map_fragment>\nfloat gr=hs(floor(vW.xz*260.));diffuseColor.rgb*=.93+.14*gr;float rim=smoothstep(uCup.z+.022,uCup.z,distance(vW.xz,uCup.xy));diffuseColor.rgb=mix(diffuseColor.rgb,vec3(.93,.93,.88),rim*.85);')};
  const ground=new T.Mesh(geo,mat);ground.receiveShadow=true;scene.add(ground);

  // hoyo con profundidad
  const cupY=H(CUP.x,CUP.z);
  const cupIn=new T.Mesh(new T.CylinderGeometry(CUP_R,CUP_R,.22,48,1,true),new T.MeshStandardMaterial({color:0x0c140f,side:T.BackSide,roughness:1}));
  cupIn.position.set(CUP.x,cupY-.11,CUP.z);scene.add(cupIn);
  const liner=new T.Mesh(new T.CylinderGeometry(CUP_R-.002,CUP_R-.002,.04,48,1,true),new T.MeshStandardMaterial({color:0xf4f4ee,side:T.BackSide,roughness:.6}));
  liner.position.set(CUP.x,cupY-.03,CUP.z);scene.add(liner);
  const cupBot=new T.Mesh(new T.CircleGeometry(CUP_R,40),new T.MeshBasicMaterial({color:0x020604}));cupBot.rotation.x=-Math.PI/2;cupBot.position.set(CUP.x,cupY-.21,CUP.z);scene.add(cupBot);

  // mástil
  const POLE_H=1.55;
  const pole=new T.Mesh(new T.CylinderGeometry(.011,.011,POLE_H,16),new T.MeshStandardMaterial({color:0xf2efe6,roughness:.35,metalness:.2}));
  pole.position.set(CUP.x,cupY-.2+POLE_H/2,CUP.z);pole.castShadow=true;scene.add(pole);
  const knob=new T.Mesh(new T.SphereGeometry(.02,16,12),new T.MeshStandardMaterial({color:0xC9A86A,roughness:.3,metalness:.6}));knob.position.set(CUP.x,cupY-.2+POLE_H,CUP.z);knob.castShadow=true;scene.add(knob);

  // bandera de tela
  const fc=document.createElement('canvas');fc.width=512;fc.height=320;const fx=fc.getContext('2d');
  const fg=fx.createLinearGradient(0,0,512,320);fg.addColorStop(0,'#D8B978');fg.addColorStop(1,'#B8955A');fx.fillStyle=fg;fx.fillRect(0,0,512,320);
  for(let i=0;i<2200;i++){fx.fillStyle=`rgba(${Math.random()<.5?'255,250,235':'90,60,20'},${Math.random()*.07})`;fx.fillRect(Math.random()*512,Math.random()*320,2,1)}
  fx.strokeStyle='rgba(14,42,30,.25)';fx.lineWidth=6;fx.strokeRect(14,14,484,292);
  fx.fillStyle='#0E2A1E';fx.font='160px "Libre Caslon Display", Georgia, serif';fx.textAlign='center';fx.textBaseline='middle';fx.fillText('18',256,172);
  const ftex=new T.CanvasTexture(fc);ftex.encoding=T.sRGBEncoding;
  document.fonts&&document.fonts.load('160px "Libre Caslon Display"').then(()=>{fx.fillStyle=fg;fx.fillRect(40,40,432,240);fx.fillStyle='#0E2A1E';fx.fillText('18',256,172);ftex.needsUpdate=true}).catch(()=>{});
  const FW=.62,FH=.39,fgeo=new T.PlaneGeometry(FW,FH,28,14);fgeo.translate(FW/2,-FH/2,0);
  const fbase=fgeo.attributes.position.array.slice();
  const flag=new T.Mesh(fgeo,new T.MeshStandardMaterial({map:ftex,side:T.DoubleSide,roughness:.85}));
  flag.position.set(CUP.x+.01,cupY-.2+POLE_H-.03,CUP.z);flag.castShadow=false;scene.add(flag);

  // bola con hoyuelos
  const bc=document.createElement('canvas');bc.width=512;bc.height=256;const bx=bc.getContext('2d');bx.fillStyle='#fff';bx.fillRect(0,0,512,256);
  for(let j=0;j<18;j++)for(let i=0;i<36;i++){const x=(i+(j%2)*.5)/36*512,y=(j+.5)/18*256;const g=bx.createRadialGradient(x,y,0,x,y,7);g.addColorStop(0,'#9a9a9a');g.addColorStop(1,'#ffffff');bx.fillStyle=g;bx.beginPath();bx.arc(x,y,7,0,7);bx.fill()}
  const btex=new T.CanvasTexture(bc);
  const ball=new T.Mesh(new T.SphereGeometry(BALL_R,48,32),new T.MeshStandardMaterial({color:0xfbfbf6,roughness:.32,bumpMap:btex,bumpScale:.0025}));
  ball.castShadow=true;scene.add(ball);

  // puntos de la línea de putt (lectura + estela)
  const path=t=>{const p=[{x:-.15,z:.5},{x:-.5,z:-.15},{x:.05,z:-.62},{x:CUP.x,z:CUP.z}];const u=1-t;
    return{x:u*u*u*p[0].x+3*u*u*t*p[1].x+3*u*t*t*p[2].x+t*t*t*p[3].x,z:u*u*u*p[0].z+3*u*u*t*p[1].z+3*u*t*t*p[2].z+t*t*t*p[3].z}};
  const ND=34,dotGeo=new T.CircleGeometry(.016,12);dotGeo.rotateX(-Math.PI/2);
  const dotMat=new T.MeshBasicMaterial({color:0xF4F1E8,transparent:true,opacity:0,depthWrite:false});
  const dots=new T.InstancedMesh(dotGeo,dotMat,ND);const m4=new T.Matrix4();
  for(let i=0;i<ND;i++){const p=path(i/(ND-1));m4.makeTranslation(p.x,H(p.x,p.z)+.004,p.z);dots.setMatrixAt(i,m4)}scene.add(dots);
  const aimMat=dotMat.clone();aimMat.color.set(0xC9A86A);const aim=new T.InstancedMesh(dotGeo,aimMat,ND);
  for(let i=0;i<ND;i++){const p=path(i/(ND-1));m4.makeTranslation(p.x,H(p.x,p.z)+.005,p.z);aim.setMatrixAt(i,m4)}scene.add(aim);

  // onda dorada al embocar
  const ring=new T.Mesh(new T.RingGeometry(CUP_R*1.05,CUP_R*1.25,64),new T.MeshBasicMaterial({color:0xE3CFA2,transparent:true,opacity:0,depthWrite:false}));
  ring.rotation.x=-Math.PI/2;ring.position.set(CUP.x,cupY+.006,CUP.z);scene.add(ring);

  // motas de luz flotando en el sol
  const PN=mobile?40:90,pg=new T.BufferGeometry(),pp=new Float32Array(PN*3),ph=[];
  for(let i=0;i<PN;i++){pp[i*3]=(Math.random()-.4)*5;pp[i*3+1]=.2+Math.random()*1.6;pp[i*3+2]=(Math.random()-.6)*4;ph.push(Math.random()*6.28)}
  pg.setAttribute('position',new T.BufferAttribute(pp,3));
  const sc=document.createElement('canvas');sc.width=sc.height=64;const sx=sc.getContext('2d');const sgr=sx.createRadialGradient(32,32,0,32,32,32);sgr.addColorStop(0,'rgba(255,236,190,1)');sgr.addColorStop(1,'rgba(255,236,190,0)');sx.fillStyle=sgr;sx.fillRect(0,0,64,64);
  const motes=new T.Points(pg,new T.PointsMaterial({size:.035,map:new T.CanvasTexture(sc),transparent:true,opacity:.55,depthWrite:false,blending:T.AdditiveBlending}));scene.add(motes);

  /* ---------- cámara y tamaño ---------- */
  let W=0,Hh=0,wide=true,full=false;
  function resize(){W=cv.clientWidth;Hh=cv.clientHeight;if(!W||!Hh)return;wide=W/Hh>1.35;full=W>900;renderer.setSize(W,Hh,false);cam.aspect=W/Hh;
    if(full)cam.setViewOffset(W*1.42,Hh,0,0,W,Hh);else cam.clearViewOffset();cam.fov=full?27:wide?24:33;cam.updateProjectionMatrix()}
  cv.closest('.hart').classList.add('g3d');resize();addEventListener('resize',()=>{clearTimeout(resize.t);resize.t=setTimeout(resize,100)});if(window.ResizeObserver)new ResizeObserver(()=>resize()).observe(cv);
  let mx=0,my=0,tmx=0,tmy=0;
  cv.closest('.hero').addEventListener('pointermove',e=>{const r=cv.getBoundingClientRect();tmx=(e.clientX-r.left)/r.width-.5;tmy=(e.clientY-r.top)/r.height-.5});
  cv.closest('.hero').addEventListener('pointerleave',()=>{tmx=tmy=0});
  const look=new T.Vector3(.35,0,-.45);

  /* ---------- animación del putt ---------- */
  const AIM=1.1,ROLL=3.8,DROP=.55,HOLD=2.2,FADE=.7,CYCLE=AIM+ROLL+DROP+HOLD+FADE;
  const LEN=(()=>{let l=0,p=path(0);for(let i=1;i<=200;i++){const q=path(i/200);l+=Math.hypot(q.x-p.x,q.z-p.z);p=q}return l})();
  const ax=new T.Vector3(),q=new T.Quaternion();let last=path(0),t0=performance.now(),visible=true;
  new IntersectionObserver(e=>{visible=e[0].isIntersecting},{threshold:0}).observe(cv);
  let drawn=0;function frame(now){if(!(RM&&drawn>2))requestAnimationFrame(frame);drawn++;if(!visible&&!RM)return;
    const time=(now-t0)/1000;const c=RM?AIM+ROLL+DROP+.4:time%CYCLE;
    mx+=(tmx-mx)*.05;my+=(tmy-my)*.05;
    const orbit=RM?0:Math.sin(time*.07)*.22;
    const R=full?7.6:wide?7.4:8.2;cam.position.set(look.x+Math.sin(orbit+mx*.25)*R*.36,(full?3.35:wide?2.7:3.8)-my*.35,look.z+Math.cos(orbit+mx*.25)*R*.88);cam.lookAt(look);

    // fases
    let prog=0,y=0,alpha=1;
    if(c<AIM){prog=0;alpha=Math.min(1,c/.45)}else if(c<AIM+ROLL){const k=(c-AIM)/ROLL;prog=1-Math.pow(1-k,2.35)}else prog=1;
    const p=path(prog);let bxp=p.x,bzp=p.z,by=H(p.x,p.z)+BALL_R;
    if(c>=AIM+ROLL){const k=Math.min((c-AIM-ROLL)/DROP,1);by=cupY+BALL_R-k*k*.16;bxp+=Math.sin(k*16)*.006*(1-k);ball.visible=k<1}else ball.visible=true;
    if(c>=CYCLE-FADE){ball.visible=false}
    // rodar: girar sobre el eje perpendicular al avance
    const dx=bxp-last.x,dz=bzp-last.z,d=Math.hypot(dx,dz);if(d>1e-5&&d<.2){ax.set(dz,0,-dx).normalize();q.setFromAxisAngle(ax,d/BALL_R);ball.quaternion.premultiply(q)}
    last={x:bxp,z:bzp};ball.position.set(bxp,by,bzp);ball.material.opacity=alpha;ball.material.transparent=alpha<1;
    // línea de lectura (antes del golpe) y estela (durante)
    aimMat.opacity=c<AIM?.8*Math.sin(c/AIM*Math.PI):0;
    const trail=Math.floor(prog*ND);dots.count=trail;dotMat.opacity=c>CYCLE-FADE-1?Math.max(0,(CYCLE-FADE-c+1)*.5):.5;
    // onda
    const dt=c-(AIM+ROLL+DROP*.7);if(dt>0&&dt<1.6){const k=dt/1.6;ring.scale.setScalar(1+k*6);ring.material.opacity=(1-k)*.9}else ring.material.opacity=0;
    // bandera: ondas que viajan del mástil hacia la punta
    const fa=fgeo.attributes.position,wind=1+.25*Math.sin(time*.6)+mx*.6;
    for(let i=0;i<fa.count;i++){const X=fbase[i*3],Y=fbase[i*3+1],u=X/FW;
      fa.setZ(i,Math.sin(u*6-time*5.2)*.05*u*wind+Math.sin(u*11-time*8.3+Y*4)*.012*u);fa.setY(i,Y-u*u*.03*(1.2-wind*.3));fa.setX(i,X*(1-.04*Math.sin(time*3+u*3)))}
    fa.needsUpdate=true;fgeo.computeVertexNormals();
    flag.rotation.y=-.55+Math.sin(time*.4)*.12+mx*.2;
    // motas
    const pa=pg.attributes.position;for(let i=0;i<PN;i++){pa.array[i*3+1]+=Math.sin(time*.5+ph[i])*.0009;pa.array[i*3]+=.0007}
    for(let i=0;i<PN;i++)if(pa.array[i*3]>3)pa.array[i*3]=-2.5;pa.needsUpdate=true;
    renderer.render(scene,cam);
  }
  requestAnimationFrame(frame);
  cv.closest('.hart').classList.add('g3d');
}
})();
