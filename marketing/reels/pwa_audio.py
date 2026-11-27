import numpy as np, wave
SR=48000;D=21.6;N=int(SR*D);o=np.zeros(N);t=np.arange(N)/SR
def add(x,at,g=1):
    i=int(at*SR);x=x[:max(0,N-i)];o[i:i+len(x)]+=g*x
def env(n,a=.005,r=.2):
    tt=np.arange(n)/SR;return np.minimum(tt/a,1)*np.exp(-tt/r)
BPM=118;b=60/BPM
kick=lambda:np.sin(2*np.pi*(50+90*np.exp(-np.arange(int(.3*SR))/SR/.03))*np.arange(int(.3*SR))/SR)*env(int(.3*SR),.002,.12)
hat=lambda:np.random.randn(int(.05*SR))*env(int(.05*SR),.001,.012)
chords=[[57,60,64,67],[53,57,60,64],[60,64,67,71],[55,59,62,67]]
f=lambda m:440*2**((m-69)/12)
k=0;x=0.0
while x<18.4:
    add(kick(),x,.55); add(hat(),x+b/2,.12)
    if k%2==1: add(np.random.randn(int(.12*SR))*env(int(.12*SR),.001,.04),x,.16)
    if k%4==0:
        c=chords[(k//4)%4];n=int(b*4*SR);tt=np.arange(n)/SR
        pad=sum(np.sin(2*np.pi*f(m)*tt)+.3*np.sin(2*np.pi*f(m)*2*tt) for m in c)*np.minimum(tt/.3,1)*np.minimum((b*4-tt)/.3,1)
        add(pad,x,.035)
        bs=np.sin(2*np.pi*f(c[0]-24)*tt)*np.minimum(tt/.01,1)*np.minimum((b*4-tt)/.1,1);add(bs,x,.12)
    k+=1;x+=b
def click():
    n=int(.06*SR);tt=np.arange(n)/SR;return (np.sin(2*np.pi*2200*tt)+.5*np.random.randn(n))*env(n,.0005,.01)
def whoosh(l=.45):
    n=int(l*SR);w=np.random.randn(n);w=np.convolve(w,np.ones(30)/30,'same');return w*np.sin(np.pi*np.arange(n)/n)**2
def pop():
    n=int(.25*SR);tt=np.arange(n)/SR;return np.sin(2*np.pi*(500+700*tt/.25)*tt)*env(n,.002,.06)
for tt_ in [2.4,4.0,5.3,7.6,11.2,14.0,16.4]: add(click(),tt_-.05,.35)
for w in [1.6,3.2,4.6,6.4,8.4,11.0,13.8,16.2]: add(whoosh(.35),w-.2,.10)
add(pop(),5.95,.45); add(whoosh(.6),7.7,.18)
# riser + impacto final
n=int(1.2*SR);tt=np.arange(n)/SR;add(np.random.randn(n)*(tt/1.2)**2*.25,17.2)
add(kick(),18.4,.9);
for i,m in enumerate([69,72,76,79]): add(np.sin(2*np.pi*f(m)*np.arange(int(2.6*SR))/SR)*env(int(2.6*SR),.01,.9),18.45+i*.12,.09)
o*=np.minimum(1,(D-t)/.4)
o=o/np.max(np.abs(o))*.9;s=(o*32767).astype(np.int16)
w=wave.open('pwa_mus.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(s.tobytes());w.close()
