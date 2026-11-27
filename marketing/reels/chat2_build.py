import subprocess, os, sys, wave
import numpy as np
D = '/home/claude/reels'; rid = 'chat2'; OUT = 'banderin-viral-6-todo-grupo-tiene-un-paco.mp4'
DUR = 22.4
MSG = [(1.7,'o'),(2.8,'o'),(3.8,'o'),(5.1,'o'),(6.4,'me'),(7.4,'me'),(12.7,'o'),(13.7,'o'),(15.1,'o'),(16.4,'sys'),(17.7,'o')]
WEB0, WEB1, TAP, END0 = 8.3, 12.3, 9.5, 19.2

if 'audio' not in sys.argv:
    cuts = [0, 3.0, 6.0, 8.3, 9.4, 11.0, 12.3, 15.0, 17.5, 19.2, DUR]
    os.makedirs(f'{D}/parts_{rid}', exist_ok=True)
    jobs = [f'{a:.4f} {b:.4f} {D}/parts_{rid}/p{k:02d}.mp4' for k, (a, b) in enumerate(zip(cuts, cuts[1:]))]
    open(f'{D}/parts_{rid}/jobs.txt', 'w').write('\n'.join(jobs) + '\n')
    subprocess.run(f"cat {D}/parts_{rid}/jobs.txt | PAGE=chat2 xargs -P 5 -L 1 sh -c 'python3 {D}/cap.py {rid} \"$0\" \"$1\" \"$2\"'", shell=True)
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
duck = np.ones(N) * .9
mix += music * duck
add(boom(1.2), 0, .8)
for t0, who in MSG:
    if who == 'o':
        for j in range(4): add(tick(), t0 - .5 + j * .11, .12)
        add(pop_in(), t0, .45)
    elif who == 'sys': add(boom(.6), t0, .7); add(tone(330, .5, 6, 180), t0, .5)
    else: add(sent(), t0, .45)
add(whoosh(), WEB0 - .2, .7); add(boom(), WEB0 + .05, .5)
add(tone(1800, .05, 80) * .7, TAP, .8)
add(whoosh(), WEB1 - .15, .6)
n = int(SR * .7); add(rng.standard_normal(n) * (np.arange(n) / n) ** 2 * .5, END0 - .7, .4)
add(boom(1.2), END0, .7); add(tone(1200, .15, 25), END0 + .95, .5)
mix *= .9 / np.abs(mix).max()
with wave.open(f'{D}/{rid}_fx.wav', 'w') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
VO = f'{D}/vp/5e729884-2633-435d-bbfe-b99f735d110d.mp3'; AT = END0 + .5
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', VO, '-af', f'aresample=48000,adelay={int(AT*1000)}|{int(AT*1000)},apad,atrim=0:{DUR},loudnorm=I=-15:TP=-1.5', '-ar', '48000', f'{D}/chat2_vo_track.wav'], check=True)
r = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{D}/{rid}_v.mp4', '-i', f'{D}/{rid}_fx.wav', '-i', f'{D}/chat2_vo_track.wav', '-filter_complex',
                    '[1:a]loudnorm=I=-17:TP=-2,aresample=48000[bg];[2:a]aresample=48000,apad[vv];[bg][vv]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]',
                    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', f'{D}/{OUT}'])
print('listo' if r.returncode == 0 else 'error')
