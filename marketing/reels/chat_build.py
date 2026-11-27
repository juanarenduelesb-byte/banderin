import subprocess, os, sys, wave
import numpy as np
D = '/home/claude/reels'; rid = 'chat'; OUT = 'banderin-reel-grupo-de-golf.mp4'
DUR = 21.6
MSG = [(0.30, 'o'), (1.40, 'o'), (2.30, 'o'), (3.30, 'o'), (4.50, 'o'), (5.80, 'o'), (7.20, 'me'), (8.30, 'me'),
       (13.95, 'o'), (14.85, 'me'), (16.00, 'o'), (17.00, 'o')]
WEB0, WEB1, TAP, END0 = 9.25, 13.6, 10.55, 18.3

if 'audio' not in sys.argv:
    cuts = [0, 3.0, 6.0, 9.2, 10.4, 12.0, 13.6, 16.0, 18.3, DUR]
    os.makedirs(f'{D}/parts_{rid}', exist_ok=True)
    jobs = [f'{a:.4f} {b:.4f} {D}/parts_{rid}/p{k:02d}.mp4' for k, (a, b) in enumerate(zip(cuts, cuts[1:]))]
    open(f'{D}/parts_{rid}/jobs.txt', 'w').write('\n'.join(jobs) + '\n')
    subprocess.run(f"cat {D}/parts_{rid}/jobs.txt | PAGE=chat xargs -P 5 -L 1 sh -c 'python3 {D}/cap.py {rid} \"$0\" \"$1\" \"$2\"'", shell=True)
    n = len(jobs)
    missing = [k for k in range(n) if not os.path.exists(f'{D}/parts_{rid}/p{k:02d}.mp4')]
    if missing: print('FALTAN', missing); sys.exit(1)
    open(f'{D}/parts_{rid}/list.txt', 'w').write(''.join(f"file 'p{k:02d}.mp4'\n" for k in range(n)))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{D}/parts_{rid}/list.txt', '-c', 'copy', f'{D}/{rid}_v.mp4'], check=True)

SR = 48000; N = int(SR * DUR); rng = np.random.default_rng(3); mix = np.zeros(N)
def add(sig, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(sig))
    if 0 <= i < N: mix[i:j] += g * sig[:j - i]
def tone(f, d, dec, f2=None):
    n = int(SR * d); t = np.arange(n) / SR; ff = f if f2 is None else f + (f2 - f) * t / d
    return np.sin(2 * np.pi * np.cumsum(ff) / SR if f2 else 2 * np.pi * f * t) * np.exp(-t * dec) * (1 - np.exp(-t * 900))
def pop_in():
    a = tone(880, .12, 30) * .8; b = tone(1320, .08, 45) * .4; a[:len(b)] += b; return a  # mensaje recibido
def sent(): return tone(600, .16, 20, 1400) * .6                           # mensaje enviado
def tick(): return rng.standard_normal(int(SR * .012)) * np.exp(-np.arange(int(SR * .012)) / SR * 400)
def whoosh(d=.45):
    n = int(SR * d); x = rng.standard_normal(n); t = np.linspace(0, 1, n); y = np.zeros(n); a0 = 0.
    for k in range(n): c = .02 + .5 * t[k] ** 1.5; a0 += c * (x[k] - a0); y[k] = a0
    return y * np.sin(np.pi * t) ** 1.6 / (np.abs(y).max() + 1e-9)
def boom(d=.9):
    n = int(SR * d); t = np.arange(n) / SR
    return np.sin(2 * np.pi * (55 + 40 * np.exp(-t * 9)) * t) * np.exp(-t * 4.5)
# ritmo 124 bpm: bombo, palmas, hi-hats, bajo y acordes suaves
bpm = 124; beat = 60 / bpm; tt = np.arange(N) / SR
kick = boom(.28); hat = rng.standard_normal(int(SR * .03)) * np.exp(-np.arange(int(SR * .03)) / SR * 160)
cn = int(SR * .16); ct = np.arange(cn) / SR; clap = np.convolve(rng.standard_normal(cn) * np.exp(-ct * 34), np.ones(6) / 6, 'same')
chords = [[220, 277.2, 329.6], [196, 246.9, 293.7], [174.6, 220, 261.6], [196, 246.9, 329.6]]; roots = [110, 98, 87.3, 98]
pad = np.zeros(N); bass = np.zeros(N)
for k in range(int(DUR / (beat * 4)) + 1):
    a = int(k * beat * 4 * SR); b = min(N, int((k + 1) * beat * 4 * SR)); st = tt[a:b] - tt[a]
    env = np.minimum(1, st * 6) * np.exp(-st * .35)
    for f in chords[k % 4]: pad[a:b] += np.sin(2 * np.pi * f * st) * env * .3
for k in range(int(DUR / beat) + 1):
    t0 = k * beat
    if t0 < END0 + 2.5:
        add(kick, t0, .5)
        if k % 4 in (1, 3): add(clap, t0, .28)
        for q in (1, 3): add(hat, t0 + q * beat / 4, .05)
        add(hat, t0 + beat / 2, .09)
        f = roots[(k // 4) % 4]; a = int((t0 + beat / 2) * SR); n = int(beat * .45 * SR); bt = np.arange(n) / SR
        if a + n < N: bass[a:a + n] += np.sin(2 * np.pi * f * bt) * np.exp(-bt * 6) * (1 - np.exp(-bt * 200))
music = pad * .18 + bass * .4
# la música baja un poco mientras se leen los mensajes y sube en la web y el cierre
duck = np.ones(N) * .55  # con voz en off, la música va por debajo todo el rato
mix += music * duck
add(boom(1.2), 0, .8)
for t0, who in MSG:
    if who == 'o':
        for j in range(4): add(tick(), t0 - .5 + j * .11, .12)
        add(pop_in(), t0, .45)
    else: add(sent(), t0, .45)
add(whoosh(), WEB0 - .2, .7); add(boom(), WEB0 + .05, .5)
add(tone(1800, .05, 80) * .7, TAP, .8)
add(whoosh(), WEB1 - .15, .6)
n = int(SR * .7); add(rng.standard_normal(n) * (np.arange(n) / n) ** 2 * .5, END0 - .7, .4)
add(boom(1.2), END0, .7); add(tone(1200, .15, 25), END0 + .95, .5)
mix *= .9 / np.abs(mix).max()
with wave.open(f'{D}/{rid}_fx.wav', 'w') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
# voz en off (Gemini TTS vía Picsart): cuatro tramos colocados sobre la acción, a 1,08x
VO = f'{D}/chat_vo.wav'; TEMPO = 1.08
SEGS = [(0.28, 10.09, 0.15), (10.44, 16.28, 9.35), (16.53, 20.31, 14.85), (20.60, 21.81, 19.30)]
fc = []; ins = []; args = []
for k, (a, b, at) in enumerate(SEGS):
    args += ['-ss', str(a), '-to', str(b), '-i', VO]
    fc.append(f'[{k}:a]atempo={TEMPO},aresample=48000,adelay={int(at*1000)}|{int(at*1000)}[v{k}]'); ins.append(f'[v{k}]')
fc.append(''.join(ins) + f'amix=inputs={len(SEGS)}:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-15:TP=-1.5,aresample=48000[vo]')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + args + ['-filter_complex', ';'.join(fc), '-map', '[vo]', '-ar', '48000', f'{D}/chat_vo_track.wav'], check=True)
r = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{D}/{rid}_v.mp4', '-i', f'{D}/{rid}_fx.wav', '-i', f'{D}/chat_vo_track.wav', '-filter_complex',
                    '[1:a]loudnorm=I=-24:TP=-3,aresample=48000[bg];[2:a]aresample=48000,apad[vv];[bg][vv]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]',
                    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', f'{D}/banderin-reel-grupo-de-golf-voz.mp4'])
print('listo' if r.returncode == 0 else 'error')
