import numpy as np, librosa, wave
from scipy.signal import fftconvolve, butter, sosfilt
SR = 48000; DUR = 33.0; N = int(SR * DUR); rng = np.random.default_rng(11)
mus = np.zeros(N); vo = np.zeros(N)
def add(buf, x, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(x))
    if i < N: buf[i:j] += g * x[:j - i]
def lpf(x, fc, o=2): return sosfilt(butter(o, fc, 'low', fs=SR, output='sos'), x)
def hpf(x, fc, o=2): return sosfilt(butter(o, fc, 'high', fs=SR, output='sos'), x)
f = lambda m: 440 * 2 ** ((m - 69) / 12)
def saw(fr, d):
    t = np.arange(int(SR * d)) / SR; return 2 * ((fr * t) % 1) - 1
def braam(m, d=3.0, g=1.0):  # metal grave de tráiler
    t = np.arange(int(SR * d)) / SR
    s = sum(saw(f(m) * (1 + det), d) for det in (-.006, 0, .006, .5005)) / 4
    s = lpf(s, 900) * np.minimum(1, t / .04) * np.exp(-t * .9)
    sub = np.sin(2 * np.pi * f(m - 12) * t) * np.exp(-t * .8)
    return g * (s * .8 + sub * .7)
def hit(d=2.5):
    t = np.arange(int(SR * d)) / SR
    k = np.sin(2 * np.pi * (40 + 90 * np.exp(-t * 14)) * t) * np.exp(-t * 2.5)
    nz = lpf(rng.standard_normal(len(t)), 3000) * np.exp(-t * 9) * .5
    return k + nz
def tick(g=1):
    n = int(.03 * SR); return hpf(rng.standard_normal(n), 3000) * np.exp(-np.arange(n) / SR * 260) * g
def riser(d):
    n = int(SR * d); t = np.arange(n) / SR
    s = hpf(rng.standard_normal(n), 800) * (t / d) ** 3 * .6 + np.sin(2 * np.pi * (200 + 900 * (t / d) ** 2) * t) * (t / d) ** 2 * .25
    return s
def pulse(m, d):
    t = np.arange(int(SR * d)) / SR; return lpf(saw(f(m), d), 500) * np.exp(-t * 7)
def heartbeat():
    return np.concatenate([hit(.25) * .9, np.zeros(int(.12 * SR)), hit(.25) * .6])

# 0–1,2: drone
n = int(14.9 * SR); t = np.arange(n) / SR
drone = lpf(sum(saw(f(m), 14.9) for m in (33, 40.02)), 220) * np.minimum(1, t / 3) * .35
add(mus, drone, 0.2)
# Reloj de tráiler 1,3–14,9
for k in range(int((14.9 - 1.3) / .5)): add(mus, tick(.5 if k % 2 else .8), 1.3 + k * .5)
add(mus, braam(33, 3.5, .9), 1.25); add(mus, braam(31, 3.5, .8), 5.6)
# Pulso de bajo desde 5,6
for k in range(int((14.9 - 5.6) / .25)): add(mus, pulse(33 if (k // 8) % 2 == 0 else 31, .22), 5.6 + k * .25, .35 + .25 * (k / 37))
add(mus, braam(29, 2.4, .7), 8.6)  # expediente
for k in range(28): add(mus, tick(.35), 8.95 + k * .055)  # máquina de escribir
add(mus, hit(1.2), 10.3, .5)  # sello
# Cuenta atrás con latidos
for k in range(5): add(mus, heartbeat(), 11.35 + k * .625, .8)
add(mus, riser(1.6), 13.5, .9)
# Tres golpes
for a in (15.13, 16.45, 18.45): add(mus, hit(1.6), a, 1.0); add(mus, braam(30, 1.4, .7), a)
# Silencio y barrido
n = int(2.5 * SR); add(mus, hpf(rng.standard_normal(n), 2000) * np.sin(np.linspace(0, np.pi, n)) ** 3 * .15, 20.8)
add(mus, riser(1.3), 22.4, 1.0)
# BRAAM del logo y percusión de acción
add(mus, hit(3), 23.72, 1.3); add(mus, braam(33, 4.0, 1.2), 23.72); add(mus, braam(45, 3.0, .5), 23.72)
bpm = 128; b = 60 / bpm; tt = 24.2
while tt < 28.5:
    for j, g in enumerate((1, 0, .6, 0, .9, .4, .6, 0)):
        if g: add(mus, hit(.4) * .5, tt + j * b / 2, g * .7)
    add(mus, pulse(33, b * 2), tt, .5); add(mus, pulse(40, b * 2), tt + b * 2, .5)
    tt += b * 4
add(mus, riser(1.2), 26.5, .6)
add(mus, tick(1.5) * 3, 27.72, 1.0); add(mus, hit(2.2), 27.72, .8)  # golpe a la bola
add(mus, hit(3.5), 28.6, 1.3); add(mus, braam(33, 5, 1.0), 28.6); add(mus, braam(40, 5, .5), 28.6)
# Reverberación
ir_n = int(2.8 * SR); ir = rng.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR * 2.2); ir[0] = 8
wet = fftconvolve(mus, ir)[:N]; wet /= np.abs(wet).max() + 1e-9
dry = mus / (np.abs(mus).max() + 1e-9); bed = .6 * dry + .4 * wet
# Voz
y, _ = librosa.load('tr_vo.wav', sr=SR)
CUTS = [(0.0, 3.9, 1.2), (4.3, 7.1, 5.6), (7.3, 9.5, 8.9), (9.8, 12.6, 11.5), (12.9, 18.2, 14.95),
        (18.35, 20.45, 21.0), (20.5, 21.8, 23.6), (21.9, 24.25, 26.0)]
for a, b_, at in CUTS:
    s = y[int(a * SR):int(b_ * SR)].copy(); r = int(.02 * SR); s[:r] *= np.linspace(0, 1, r); s[-r:] *= np.linspace(1, 0, r)
    add(vo, s, at)
vo = vo / (np.abs(vo).max() + 1e-9)
# Algo de cuerpo a la voz (un poco de grave y sala corta)
ir2 = rng.standard_normal(int(.5 * SR)) * np.exp(-np.arange(int(.5 * SR)) / SR * 12); ir2[0] = 25
vo = fftconvolve(vo, ir2)[:N]; vo /= np.abs(vo).max() + 1e-9
env = np.convolve(np.abs(vo), np.ones(int(.08 * SR)) / int(.08 * SR), 'same'); env = np.minimum(1, env * 8)
env = np.convolve(env, np.ones(int(.2 * SR)) / int(.2 * SR), 'same')
mix = bed * (1 - .5 * env) * .55 + vo * .85
fade = np.ones(N); fade[-int(1.5 * SR):] = np.linspace(1, 0, int(1.5 * SR)); mix *= fade
mix = np.tanh(mix * 1.6) / np.tanh(1.6); mix *= .95 / np.abs(mix).max()
with wave.open('tr_mix.wav', 'w') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.stack([mix, mix], 1) * 32767).astype(np.int16).tobytes())
print('ok')
