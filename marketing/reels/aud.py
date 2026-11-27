import subprocess, sys, wave
import numpy as np
D = '/home/claude/reels'
rid, vo, out = sys.argv[1], sys.argv[2], sys.argv[3]
CFG = {
 'r2': dict(DUR=22.6, E=20.0, ev=[('boom', 0, .8), ('wh', 2.85, .7), *[('pop', a, .45) for a in (3.06, 4.61, 6.11, 7.15, 8.45)],
       *[('tick', 8.95 + i * .042, .5) for i in range(18)], ('boom', 9.72, .9), ('err', 9.75, .35), ('wh', 12.75, .7), ('boom', 13.0, .55),
       ('tap', 15.3, .8), ('wh', 17.0, .45), ('pop', 17.2, .3)]),
 'r3': dict(DUR=22.6, E=19.95, ev=[('boom', 0, .8), *[('pop', a, .45) for a in (.15, 1.0, 2.45)], ('wh', 5.6, .7),
       *[('tick', 5.8 + i * .035, .35) for i in range(17)], *[('err', a, .4) for a in (7.91, 9.06, 10.96, 12.32)],
       ('chime', 14.0, .5), ('wh', 14.95, .7), ('boom', 15.15, .7), ('wh', 15.75, .5), ('tick', 16.3, .6), ('tick', 16.55, .6),
       ('tap', 17.6, .8), *[('pop', 18.1 + i * .2, .3) for i in range(4)]]),
 'r4': dict(DUR=19.4, E=15.55, ev=[('boom', 0, .8), ('tap', 1.84, .8), ('wh', 2.0, .6), ('wh', 2.9, .6), ('tap', 4.15, .8),
       ('boom', 4.5, 1.0), ('err', 4.52, .45), ('wh', 5.65, .6), ('wh', 7.3, .6), ('pop', 7.65, .4), ('pop', 7.85, .4),
       ('tap', 8.72, .8), ('chime', 8.78, .3), ('tap', 9.17, .8), ('chime', 9.23, .3), ('wh', 9.8, .6),
       ('notif', 10.95, .6), ('notif', 12.41, .6), ('pop', 13.56, .5), ('pop', 14.35, .5)]),
}[rid]
DUR, E = CFG['DUR'], CFG['E']
SR = 48000; N = int(SR * DUR); rng = np.random.default_rng(5); mix = np.zeros(N)
def add(sig, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(sig))
    if 0 <= i < N: mix[i:j] += g * sig[:j - i]
def tone(f, d, dec, f2=None):
    n = int(SR * d); t = np.arange(n) / SR
    ph = 2 * np.pi * np.cumsum(f + (f2 - f) * t / d) / SR if f2 else 2 * np.pi * f * t
    return np.sin(ph) * np.exp(-t * dec) * (1 - np.exp(-t * 900))
def whoosh(d=.45):
    n = int(SR * d); x = rng.standard_normal(n); t = np.linspace(0, 1, n); y = np.zeros(n); a0 = 0.
    for k in range(n): c = .02 + .5 * t[k] ** 1.5; a0 += c * (x[k] - a0); y[k] = a0
    return y * np.sin(np.pi * t) ** 1.6 / (np.abs(y).max() + 1e-9)
def boom(d=.9):
    t = np.arange(int(SR * d)) / SR; return np.sin(2 * np.pi * (55 + 40 * np.exp(-t * 9)) * t) * np.exp(-t * 4.5)
def tick():
    n = int(SR * .02); return rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 300) * .8 + tone(2400, .02, 200) * .4
def pop():
    a = tone(880, .12, 30) * .8; b = tone(1320, .08, 45) * .4; a[:len(b)] += b; return a
def err():
    a = tone(220, .22, 12) * .7; b = tone(233, .22, 12) * .7; return a + b
def chime():
    a = tone(1046, .5, 7) * .5; b = tone(1568, .5, 7) * .35; return a + b
def notif():
    a = tone(1318, .25, 12) * .6; b = np.zeros(int(SR * .38)); b[int(SR * .12):] = tone(1760, .26, 11)[:len(b) - int(SR * .12)] * .5
    a = np.pad(a, (0, len(b) - len(a))); return a + b
FX = dict(boom=lambda: boom(1.1), wh=whoosh, tick=tick, pop=pop, err=err, chime=chime, notif=notif, tap=lambda: tone(1800, .05, 80) * .7)
# música: igual que el reel del grupo (124 bpm, bombo, palmas, hats, bajo y acordes)
bpm = 124; beat = 60 / bpm; tt = np.arange(N) / SR
kick = boom(.28); hat = rng.standard_normal(int(SR * .03)) * np.exp(-np.arange(int(SR * .03)) / SR * 160)
cn = int(SR * .16); ct = np.arange(cn) / SR; clap = np.convolve(rng.standard_normal(cn) * np.exp(-ct * 34), np.ones(6) / 6, 'same')
chords = [[220, 277.2, 329.6], [196, 246.9, 293.7], [174.6, 220, 261.6], [196, 246.9, 329.6]]; roots = [110, 98, 87.3, 98]
pad = np.zeros(N); bass = np.zeros(N); drums = np.zeros(N)
for k in range(int(DUR / (beat * 4)) + 1):
    a = int(k * beat * 4 * SR); b = min(N, int((k + 1) * beat * 4 * SR)); st = tt[a:b] - tt[a]
    env = np.minimum(1, st * 6) * np.exp(-st * .35)
    for f in chords[k % 4]: pad[a:b] += np.sin(2 * np.pi * f * st) * env * .3
for k in range(int(DUR / beat) + 1):
    t0 = k * beat
    if t0 < E + 2.0:
        add(kick, t0, .5)
        if k % 4 in (1, 3): add(clap, t0, .28)
        for q in (1, 3): add(hat, t0 + q * beat / 4, .05)
        add(hat, t0 + beat / 2, .09)
        f = roots[(k // 4) % 4]; a = int((t0 + beat / 2) * SR); n = int(beat * .45 * SR); bt = np.arange(n) / SR
        if a + n < N: bass[a:a + n] += np.sin(2 * np.pi * f * bt) * np.exp(-bt * 6) * (1 - np.exp(-bt * 200))
mix += (pad * .18 + bass * .4) * .55
for name, t0, g in CFG['ev']: add(FX[name](), t0, g)
n = int(SR * .7); add(rng.standard_normal(n) * (np.arange(n) / n) ** 2 * .5, E - .7, .4)
add(boom(1.2), E, .7); add(tone(1200, .15, 25), E + .95, .5)
mix *= np.minimum(1, (DUR - tt) / .4)
mix *= .9 / np.abs(mix).max()
with wave.open(f'{D}/{rid}_fx.wav', 'w') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
# voz: misma cadena que el reel del grupo (atempo 1,08, loudnorm -15, música a -24)
r = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{D}/{rid}_v.mp4', '-i', f'{D}/{rid}_fx.wav', '-i', vo, '-filter_complex',
    f'[2:a]atempo=1.08,aresample=48000,adelay=150|150,apad,atrim=0:{DUR},loudnorm=I=-15:TP=-1.5,aresample=48000[vv];'
    '[1:a]loudnorm=I=-24:TP=-3,aresample=48000[bg];[bg][vv]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]',
    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', f'{D}/{out}'])
print('listo' if r.returncode == 0 else 'error', out)
