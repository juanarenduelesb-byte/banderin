import numpy as np, librosa, wave
from scipy.signal import fftconvolve
SR = 48000; DUR = 31.0; N = int(SR * DUR); rng = np.random.default_rng(7)
mus = np.zeros(N); fx = np.zeros(N); vo = np.zeros(N)
def add(buf, x, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(x))
    if i < N: buf[i:j] += g * x[:j - i]
f = lambda m: 440 * 2 ** ((m - 69) / 12)
def piano(m, d=3.5, v=1.0):
    n = int(SR * d); t = np.arange(n) / SR; fr = f(m); s = np.zeros(n)
    for k in range(1, 8):
        fk = fr * k * (1 + .0004 * k * k)
        if fk > 12000: break
        s += np.sin(2 * np.pi * fk * t) * (1 / k ** 1.4) * np.exp(-t * (0.9 + .55 * k))
    s *= (1 - np.exp(-t * 300)); return v * s / 2
def pad(ms, d, g=1.0, bright=0.0):
    n = int(SR * d); t = np.arange(n) / SR; s = np.zeros(n)
    for m in ms:
        for det in (-.07, 0, .07):
            ph = 2 * np.pi * f(m) * (1 + det / 100) * t
            s += np.sin(ph) + bright * .3 * np.sin(2 * ph) + .12 * np.sin(3 * ph)
    env = np.minimum(1, t / 1.2) * np.minimum(1, (d - t) / 1.0)
    return g * s * env / (len(ms) * 3)
def boom(d=2.0, f0=48):
    t = np.arange(int(SR * d)) / SR; return np.sin(2 * np.pi * (f0 + 60 * np.exp(-t * 7)) * t) * np.exp(-t * 2.2)
def noise_burst(d, dec):
    n = int(SR * d); return rng.standard_normal(n) * np.exp(-np.arange(n) / SR * dec)
def S(*xs):
    n = max(len(x) for x in xs); o = np.zeros(n)
    for x in xs: o[:len(x)] += x
    return o
def lp(x, a):
    y = np.zeros_like(x); s = 0.
    for i in range(len(x)): s += a * (x[i] - s); y[i] = s
    return y

# — Parte 1 (0–15,5): piano en La menor, 70 bpm, arpegios suaves —
b1 = 60 / 70
prog1 = [[57, 60, 64], [53, 57, 60], [48, 55, 60, 64], [55, 59, 62]]  # Am F C G
t0 = .2; k = 0
while t0 < 15.0:
    ch = prog1[k % 4]
    add(mus, piano(ch[0] - 12, 4, .9), t0, .55)
    for j, m in enumerate([ch[0], ch[1], ch[2], ch[1] + 12, ch[2], ch[1]]):
        tt = t0 + j * b1 / 1.5
        if tt < 15.2: add(mus, piano(m + 12, 2.5, .55), tt, .32)
    add(mus, pad([c + 12 for c in ch], b1 * 4 + .8, .35), t0, .7)
    t0 += b1 * 4; k += 1
fade1 = np.ones(N); i0, i1 = int(14.6 * SR), int(15.6 * SR); fade1[i0:i1] = np.linspace(1, 0, i1 - i0); fade1[i1:] = 0
mus *= fade1
# Silencio y subida (16,4–18,3)
n = int(1.9 * SR); t = np.arange(n) / SR
riser = (np.sin(2 * np.pi * (110 + 220 * (t / 1.9) ** 2) * t) * .25 + lp(rng.standard_normal(n), .08) * 1.2) * (t / 1.9) ** 2.5
add(mus, riser, 16.35, .35)
# — Parte 2 (18,3–31): Do mayor, luminoso —
b2 = 60 / 96
prog2 = [[48, 55, 64, 67], [43, 55, 62, 67], [45, 57, 64, 69], [41, 57, 60, 65]]  # C G Am F
add(mus, boom(2.6, 40), 18.3, 1.0)
add(mus, pad([60, 64, 67, 72], 3.0, 1.0, 1), 18.3, .9)
t0 = 18.3; k = 0
while t0 < 29.5:
    ch = prog2[k % 4]
    add(mus, piano(ch[0], 3.5, 1), t0, .6)
    add(mus, pad([c + 12 for c in ch[1:]], b2 * 4 + 1.0, .9, 1), t0, .55)
    for j in range(8):
        tt = t0 + j * b2 / 2; m = ch[1 + (j % 3)] + 12 + (12 if j in (3, 7) else 0)
        if tt < 29.8: add(mus, piano(m, 2, .6), tt, .26)
    if t0 >= 19.5:
        for j in range(4):
            tt = t0 + j * b2
            if tt < 23.9: add(mus, boom(.35, 52), tt, .35 if j % 2 == 0 else .2)
            if j % 2 == 1 and tt < 23.9: add(mus, lp(noise_burst(.18, 30), .4), tt, .12)
    t0 += b2 * 4; k += 1
# Acorde final
add(mus, boom(3, 38), 24.0, .9); add(mus, pad([48, 55, 60, 64, 67, 72], 7.0, 1.2, 1), 24.0, 1.0)
for j, m in enumerate([72, 76, 79, 84]): add(mus, piano(m, 4, .8), 24.05 + j * .09, .3)
# — Sonidos —
for a in (4.55, 5.75): add(fx, lp(noise_burst(.35, 9), .25) * np.sin(np.linspace(0, np.pi, int(.35 * SR))), a, .5)  # hoja
for a in (7.55, 8.1, 8.75): add(fx, S(piano(88, .25, 1), piano(95, .2, .6)), a, .35)  # mensajes
for i in range(14): add(fx, lp(noise_burst(.12, 25), .3), 9.75 + i * .11, .18)  # ventanas
add(fx, S(noise_burst(.03, 300) * .6, piano(91, .08, .6)), 13.6, .5)  # toque
add(fx, boom(1.2, 45), 14.35, .9); add(fx, lp(noise_burst(.25, 18), .5), 14.35, .5)  # sello
add(fx, S(piano(96, 1.0, 1), piano(103, .8, .5)), 20.95, .5)  # la bola en el hoyo
n = int(.5 * SR); add(fx, lp(rng.standard_normal(n), .05) * np.sin(np.linspace(0, np.pi, n)) ** 2, 21.3, .5)  # paso a la web
# Reverberación de sala grande
ir_n = int(2.4 * SR); ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR * 2.6); ir[0] = 6
wet = fftconvolve(mus + fx * .6, ir)[:N]; wet /= np.abs(wet).max() + 1e-9
dry = mus + fx; dry /= np.abs(dry).max() + 1e-9
bed = .55 * dry + .45 * wet
# — Voz: frases separadas en sus tiempos —
y, sr = librosa.load('tv_vo.wav', sr=SR)
CUTS = [(0.0, 1.69, 1.0), (1.72, 5.35, 3.0), (5.35, 7.2, 7.6), (7.2, 9.2, 9.9), (9.29, 12.48, 12.4),
        (12.48, 14.25, 16.7), (14.26, 18.44, 19.3), (18.44, 19.47, 24.0), (19.47, 22.05, 25.35)]
for a, b, at in CUTS:
    seg = y[int(a * SR):int(b * SR)].copy(); r = int(.02 * SR); seg[:r] *= np.linspace(0, 1, r); seg[-r:] *= np.linspace(1, 0, r)
    add(vo, seg, at)
vo /= np.abs(vo).max() + 1e-9
# Ducking de la música bajo la voz
env = np.convolve(np.abs(vo), np.ones(int(.08 * SR)) / int(.08 * SR), 'same'); env = np.minimum(1, env * 8)
env = np.convolve(env, np.ones(int(.25 * SR)) / int(.25 * SR), 'same')
mix = bed * (1 - .45 * env) * .5 + vo * .9
fade = np.ones(N); fade[:int(.6 * SR)] = np.linspace(0, 1, int(.6 * SR)); fade[-int(1.2 * SR):] = np.linspace(1, 0, int(1.2 * SR))
mix *= fade; mix *= .95 / np.abs(mix).max()
st = np.stack([mix, mix], 1)
with wave.open('tv_mix.wav', 'w') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype(np.int16).tobytes())
print('ok')
