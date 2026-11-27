"""python3 mk.py <id>  -> monta un reel con el motor de siempre + voz de Picsart (VOICE=[(url,inicio_s)])"""
import sys, os, json, subprocess, importlib.util, wave, urllib.request, socket, time
import numpy as np
D = '/home/claude/reels'; rid = sys.argv[1]
spec = importlib.util.spec_from_file_location('cfg', f'{D}/{rid}.py'); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
DUR = C.DUR; scenes = C.SCENES(None, DUR)
open(f'{D}/{rid}.js', 'w').write('window.REEL=' + json.dumps({'id': rid, 'dur': DUR, 'words': [], 'capgroups': [], 'keys': [], 'scenes': scenes}, ensure_ascii=False) + ';')
s = socket.socket()
if s.connect_ex(('127.0.0.1', 8772)) != 0:
    subprocess.Popen(['python3', f'{D}/srv.py'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1.5)
s.close()
if 'audio' not in sys.argv:
    cuts = [0]
    while cuts[-1] + 3.0 < DUR - 0.5: cuts.append(round(cuts[-1] + 3.0, 2))
    cuts.append(DUR)
    os.makedirs(f'{D}/parts_{rid}', exist_ok=True)
    jobs = [f'{a:.4f} {b:.4f} {D}/parts_{rid}/p{k:02d}.mp4' for k, (a, b) in enumerate(zip(cuts, cuts[1:]))]
    for k in range(len(jobs)):
        p = f'{D}/parts_{rid}/p{k:02d}.mp4'
        if os.path.exists(p): os.remove(p)
    open(f'{D}/parts_{rid}/jobs.txt', 'w').write('\n'.join(jobs) + '\n')
    subprocess.run(f"cat {D}/parts_{rid}/jobs.txt | xargs -P 5 -L 1 sh -c 'python3 {D}/cap.py {rid} \"$0\" \"$1\" \"$2\"'", shell=True)
    miss = [k for k in range(len(jobs)) if not os.path.exists(f'{D}/parts_{rid}/p{k:02d}.mp4')]
    if miss: print('FALTAN', miss); sys.exit(1)
    open(f'{D}/parts_{rid}/list.txt', 'w').write(''.join(f"file 'p{k:02d}.mp4'\n" for k in range(len(jobs))))
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', f'{D}/parts_{rid}/list.txt', '-c', 'copy', f'{D}/{rid}_v.mp4'], check=True)
SR = 48000; N = int(SR * DUR); rng = np.random.default_rng(7); mix = np.zeros(N)
def add(sig, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(sig))
    if 0 <= i < N: mix[i:j] += g * sig[:j - i]
def boom(d=.9):
    t = np.arange(int(SR * d)) / SR; return np.sin(2 * np.pi * (55 + 40 * np.exp(-t * 9)) * t) * np.exp(-t * 4.5)
def whoosh(d=.45):
    n = int(SR * d); x = rng.standard_normal(n); t = np.linspace(0, 1, n); y = np.zeros(n); a0 = 0.
    for k in range(n): c = .02 + .5 * t[k] ** 1.5; a0 += c * (x[k] - a0); y[k] = a0
    return y * np.sin(np.pi * t) ** 1.6 / (np.abs(y).max() + 1e-9)
bpm = 124; beat = 60 / bpm; tt = np.arange(N) / SR
kick = boom(.28); hat = rng.standard_normal(int(SR * .03)) * np.exp(-np.arange(int(SR * .03)) / SR * 160)
chords = [[220, 277.2, 329.6], [196, 246.9, 293.7], [174.6, 220, 261.6], [196, 246.9, 329.6]]; roots = [110, 98, 87.3, 98]
pad = np.zeros(N); bass = np.zeros(N)
for k in range(int(DUR / (beat * 4)) + 1):
    a = int(k * beat * 4 * SR); b = min(N, int((k + 1) * beat * 4 * SR))
    if a >= N: break
    st = tt[a:b] - tt[a]; env = np.minimum(1, st * 6) * np.exp(-st * .35)
    for f in chords[k % 4]: pad[a:b] += np.sin(2 * np.pi * f * st) * env * .3
for k in range(int(DUR / beat) + 1):
    t0 = k * beat; add(kick, t0, .5); add(hat, t0 + beat / 2, .09)
    f = roots[(k // 4) % 4]; a = int((t0 + beat / 2) * SR); n = int(beat * .45 * SR); bt = np.arange(n) / SR
    if a + n < N: bass[a:a + n] += np.sin(2 * np.pi * f * bt) * np.exp(-bt * 6) * (1 - np.exp(-bt * 200))
mix += (pad * .18 + bass * .4) * .5
add(boom(1.2), 0, .8)
for sc in scenes[1:]: add(whoosh(), max(0, sc['t0'] - .2), .5)
mix *= .9 / np.abs(mix).max()
with wave.open(f'{D}/{rid}_fx.wav', 'w') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
args = []; fc = []; ins = []
for k, (u, at) in enumerate(C.VOICE):
    p = f'{D}/vp/{u}.mp3'
    args += ['-i', p]; fc.append(f'[{k}:a]aresample=48000,adelay={int(at*1000)}|{int(at*1000)}[v{k}]'); ins.append(f'[v{k}]')
fc.append(''.join(ins) + f'amix=inputs={len(C.VOICE)}:normalize=0,apad,atrim=0:{DUR},loudnorm=I=-15:TP=-1.5,aresample=48000[vo]')
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + args + ['-filter_complex', ';'.join(fc), '-map', '[vo]', '-ar', '48000', f'{D}/{rid}_vo_track.wav'], check=True)
r = subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', f'{D}/{rid}_v.mp4', '-i', f'{D}/{rid}_fx.wav', '-i', f'{D}/{rid}_vo_track.wav', '-filter_complex',
    '[1:a]loudnorm=I=-24:TP=-3,aresample=48000[bg];[2:a]aresample=48000,apad[vv];[bg][vv]amix=inputs=2:normalize=0:duration=first,alimiter=limit=0.95[a]',
    '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', f'{D}/{C.OUT}'])
print('listo' if r.returncode == 0 else 'error', C.OUT)
