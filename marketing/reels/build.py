"""Monta un reel: python3 build.py <id>
Lee reels/<id>.py (TOKENS, SCENES(ph) y KEYS), alinea las palabras con la voz <id>_vo.mp3,
escribe <id>.js para engine.html, renderiza por tramos en paralelo, añade música + efectos y la voz."""
import sys, subprocess, re, json, os, importlib.util, math
import numpy as np, wave
D = '/home/claude/reels'
rid = sys.argv[1]
spec = importlib.util.spec_from_file_location('cfg', f'{D}/{rid}.py'); C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
def sh(*a, **k): return subprocess.run(a, capture_output=True, text=True, **k)
NOVO = getattr(C, 'NOVO', False)
if NOVO:
    DUR = C.DUR; scenes = C.SCENES(None, DUR); words = []; groups = []
    cfg = {'id': rid, 'dur': DUR, 'words': [], 'capgroups': [], 'keys': [], 'scenes': scenes}
    open(f'{D}/{rid}.js', 'w').write('window.REEL=' + json.dumps(cfg, ensure_ascii=False) + ';')
    print('duración', DUR, [(s['type'], round(s['t0'],2), round(s['t1'],2)) for s in scenes])
    if len(sys.argv) > 2 and sys.argv[2] == 'cfg': sys.exit()
else:
    vo = f'{D}/{rid}_vo.mp3'
    if getattr(C, 'TEMPO', 1.0) != 1.0:
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', vo, '-af', f'atempo={C.TEMPO}', '-ar', '48000', f'{D}/{rid}_vo_t.wav'], check=True); vo = f'{D}/{rid}_vo_t.wav'
    LEAD = getattr(C, 'LEAD', 0.35)  # la voz empieza tras este margen

    def sh(*a, **k): return subprocess.run(a, capture_output=True, text=True, **k)

    # ---------- 1. tramos de voz (silencedetect) ----------
    dur_vo = float(sh('ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', vo).stdout)
    log = sh('ffmpeg', '-i', vo, '-af', 'silencedetect=noise=-38dB:d=0.16', '-f', 'null', '-').stderr
    ss = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]; se = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
    speech = []; cur = 0.0
    for a, b in zip(ss, se + [dur_vo] * (len(ss) - len(se))):
        if a - cur > 0.05: speech.append([cur, a])
        cur = b
    if dur_vo - cur > 0.05: speech.append([cur, dur_vo])
    speech = [[max(0, a - 0.02), b] for a, b in speech]
    print('tramos de voz', [(round(a, 2), round(b, 2)) for a, b in speech])

    # ---------- 2. palabras: cada frase (PHRASES) a un tramo; si no cuadra, reparto por letras ----------
    # TOKENS: lista de (texto_mostrado, peso_letras, frase_idx)
    toks = C.TOKENS
    nph = max(t[2] for t in toks) + 1
    # tiempo de habla continuo (sin silencios) -> tiempo real
    cum = [0]
    for a_, b_ in speech: cum.append(cum[-1] + b_ - a_)
    S = cum[-1]
    def real(x, prefer_next=False):
        for k, (a_, b_) in enumerate(speech):
            if x < cum[k + 1] - 1e-6 or (x <= cum[k + 1] + 1e-6 and not prefer_next) or k == len(speech) - 1:
                return a_ + (x - cum[k])
        return speech[-1][1]
    W = [t[1] for t in toks]; TW = sum(W)
    pw = [sum(t[1] for t in toks if t[2] == p) for p in range(nph)]
    bx = [0.0]
    for p in range(nph): bx.append(bx[-1] + S * pw[p] / TW)
    gaps = cum[1:-1]
    used = set()
    for p in range(1, nph):
        cand = [g for g in gaps if g not in used and g > bx[p - 1] + 0.2]
        if cand:
            g = min(cand, key=lambda g: abs(g - bx[p]))
            if abs(g - bx[p]) < 0.7: bx[p] = g; used.add(g)
    bx[-1] = S
    if len(speech) == nph: bx = list(cum)  # una frase por tramo de voz: reparto exacto
    words = []; segs = []
    for p in range(nph):
        tp = [t for t in toks if t[2] == p]; x0, x1 = bx[p], bx[p + 1]; tot = sum(t[1] for t in tp); acc = 0
        segs.append([real(x0, True), real(x1)])
        for t in tp:
            s0 = x0 + (x1 - x0) * acc / tot; acc += t[1]; e0 = x0 + (x1 - x0) * acc / tot
            words.append({'w': t[0], 's': round(real(s0, True) + LEAD, 3), 'e': round(real(e0) + LEAD, 3), 'p': p})
    print('frases', [(round(a_, 2), round(b_, 2)) for a_, b_ in segs])
    ph = [[round(segs[p][0] + LEAD, 3), round(segs[p][1] + LEAD, 3)] for p in range(nph)]
    # grupos de subtítulo: máx 3 palabras o corte por frase / signo
    groups = []; i = 0
    while i < len(words):
        j = i + 1
        while j < len(words) and j - i < C.__dict__.get('MAXW', 3) and words[j]['p'] == words[i]['p'] and not re.search(r'[.,?!:]$', words[j - 1]['w']): j += 1
        groups.append([words[i]['s'] - 0.05, words[j - 1]['e'] + 0.05, i, j]); i = j
    for k in range(len(groups) - 1): groups[k][1] = min(groups[k][1], groups[k + 1][0])
    DUR = round(ph[-1][1] + C.__dict__.get('TAIL', 1.6), 2)
    scenes = C.SCENES(ph, DUR)
    cfg = {'id': rid, 'dur': DUR, 'words': words, 'capgroups': groups, 'keys': C.KEYS, 'scenes': scenes}
    if getattr(C, 'REVEAL', None) is not None: cfg['reveal'] = C.REVEAL
    open(f'{D}/{rid}.js', 'w').write('window.REEL=' + json.dumps(cfg, ensure_ascii=False) + ';')
    print('duración', DUR, 'escenas', [(s['type'], s['t0'], s['t1']) for s in scenes])
    if len(sys.argv) > 2 and sys.argv[2] == 'cfg': sys.exit()


# ---------- 3. render por tramos en paralelo ----------
if not (len(sys.argv) > 2 and sys.argv[2] == 'audio'):
    cuts = sorted(set([0] + [s['t0'] for s in scenes if s['t0'] > 0.5] + [DUR]))
    parts = []
    for a, b in zip(cuts, cuts[1:]):
        while b - a > 4.5: parts.append((a, a + 4)); a += 4
        parts.append((a, b))
    os.makedirs(f'{D}/parts_{rid}', exist_ok=True)
    jobs = [f'{a:.4f} {b:.4f} {D}/parts_{rid}/p{k:02d}.mp4' for k, (a, b) in enumerate(parts)]
    open(f'{D}/parts_{rid}/jobs.txt', 'w').write('\n'.join(jobs) + '\n')
    r = subprocess.run(f"cat {D}/parts_{rid}/jobs.txt | xargs -P 5 -L 1 sh -c 'python3 {D}/cap.py {rid} \"$0\" \"$1\" \"$2\"'", shell=True)
    open(f'{D}/parts_{rid}/list.txt', 'w').write(''.join(f"file 'p{k:02d}.mp4'\n" for k in range(len(parts))))
    missing = [k for k in range(len(parts)) if not os.path.exists(f'{D}/parts_{rid}/p{k:02d}.mp4')]
    if missing: print('FALTAN', missing); sys.exit(1)
    sh('ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', f'{D}/parts_{rid}/list.txt', '-c', 'copy', f'{D}/{rid}_v.mp4')

# ---------- 4. audio: música + whoosh/pop en cortes + voz ----------
SR = 48000; N = int(SR * DUR); rng = np.random.default_rng(7)
mix = np.zeros(N)
def add(sig, t, g=1.0):
    i = int(t * SR); j = min(N, i + len(sig))
    if i < N: mix[i:j] += g * sig[:j - i]
def whoosh(d=0.42):
    n = int(SR * d); x = rng.standard_normal(n); t = np.linspace(0, 1, n)
    # ruido filtrado con barrido (filtro de un polo variable)
    y = np.zeros(n); a0 = 0.0
    for k in range(n):
        c = 0.02 + 0.5 * t[k] ** 1.5; a0 += c * (x[k] - a0); y[k] = a0
    env = np.sin(np.pi * t) ** 1.6
    return y * env / (np.abs(y).max() + 1e-9)
def pop(f=880, d=0.09):
    n = int(SR * d); t = np.arange(n) / SR
    return np.sin(2 * np.pi * f * t * (1 + 0.6 * np.exp(-t * 60))) * np.exp(-t * 42)
def tick(): return pop(2400, 0.03) * 0.6
def boom(d=0.9):
    n = int(SR * d); t = np.arange(n) / SR
    return np.sin(2 * np.pi * (55 + 40 * np.exp(-t * 9)) * t) * np.exp(-t * 4.5)
def riser(d=0.6):
    n = int(SR * d); t = np.arange(n) / SR; x = rng.standard_normal(n)
    return x * (t / d) ** 2 * 0.5
W0 = whoosh()
# música: pulso suave 120 bpm, acordes de pad + bombo
bpm = getattr(C, 'BPM', 118); beat = 60 / bpm
chords = [[220, 277.2, 329.6], [196, 246.9, 293.7], [174.6, 220, 261.6], [196, 246.9, 329.6]]
tt = np.arange(N) / SR
pad = np.zeros(N)
for k in range(int(DUR / (beat * 4)) + 1):
    a = int(k * beat * 4 * SR); b = min(N, int((k + 1) * beat * 4 * SR)); seg_t = tt[a:b] - tt[a]
    env = np.minimum(1, seg_t * 6) * np.exp(-seg_t * 0.35)
    for f in chords[k % 4]: pad[a:b] += np.sin(2 * np.pi * f * seg_t) * env * 0.33 + np.sin(2 * np.pi * f * 2.003 * seg_t) * env * 0.08
kick = boom(0.28)
hat = rng.standard_normal(int(SR * 0.03)) * np.exp(-np.arange(int(SR * 0.03)) / SR * 160)
for k in range(int(DUR / beat) + 1):
    add(kick, k * beat, 0.55)
    add(hat, k * beat + beat / 2, 0.10)
mix += pad * 0.20
if NOVO:  # sin voz: ritmo con más pegada (palmas en 2 y 4, hi-hats a semicorcheas, bajo)
    clapn = int(SR * 0.16); ct = np.arange(clapn) / SR
    clap = rng.standard_normal(clapn) * (np.exp(-ct * 38) + 0.6 * np.exp(-np.maximum(0, ct - 0.012) * 45) * (ct > 0.012))
    clap = np.convolve(clap, np.ones(6) / 6, 'same')
    roots = [110, 98, 87.3, 98]
    bass = np.zeros(N)
    nb = int(DUR / beat) + 1
    for k in range(nb):
        if k % 4 in (1, 3): add(clap, k * beat, 0.32)
        for q in range(4):
            if q: add(hat * 0.8, k * beat + q * beat / 4, 0.05 if q != 2 else 0.09)
        f = roots[(k // 4) % 4]; a = int((k * beat + beat / 2) * SR); n = int(beat * 0.45 * SR); bt = np.arange(n) / SR
        if a + n < N: bass[a:a + n] += np.sin(2 * np.pi * f * bt) * np.exp(-bt * 6) * (1 - np.exp(-bt * 200))
    mix += bass * 0.45
    for k in range(nb): add(kick, k * beat, 0.25)  # refuerzo
if getattr(C, 'MOOD', '') == 'doc':
    # Documental: dron grave + ostinato de cuerdas en tensión hasta el giro; silencio; luego la música de siempre
    REV = C.REVEAL; mix[:] = 0
    def lp(x, c):
        y = np.zeros_like(x); a0 = 0.0
        for k in range(0, len(x)): a0 += c * (x[k] - a0); y[k] = a0
        return y
    nrev = int(REV * SR)
    tq = tt[:nrev]
    drone = np.zeros(nrev)
    for f, g in [(73.42, 1), (110.0, .6), (146.83, .35), (174.61, .25)]:
        for h in range(1, 7):
            drone += g / h * np.sin(2 * np.pi * f * h * tq * (1 + .0012 * (h % 2)) + h)
    drone *= (0.35 + 0.65 * (tq / REV) ** 1.3) * np.minimum(1, tq / 1.2)
    drone = lp(drone, 0.08)
    mix[:nrev] += drone * 0.10
    # ostinato (semicorcheas a 100 bpm) en re menor, entra con el chat
    bt = 60 / 100 / 4; notes = [146.83, 146.83, 174.61, 146.83, 220.0, 146.83, 174.61, 130.81]
    t_on = scenes[1]['t0']; k = 0
    while t_on + k * bt < REV - 0.5:
        t0_ = t_on + k * bt; f = notes[k % 8] * (2 if (t0_ > scenes[3]['t0']) else 1)
        n = int(bt * 0.9 * SR); x = np.arange(n) / SR
        v = sum(np.sin(2 * np.pi * f * h * x) / h for h in range(1, 5)) * np.exp(-x * 9) * (1 - np.exp(-x * 400))
        add(v, t0_, 0.05 + 0.07 * (t0_ / REV)); k += 1
    # latido grave cada pulso desde la búsqueda
    hb = boom(0.35)
    k = 0; tb_ = scenes[2]['t0']
    while tb_ + k * 0.6 < REV - 0.6:
        add(hb, tb_ + k * 0.6, 0.55); add(hb, tb_ + k * 0.6 + 0.16, 0.3); k += 1
    # silencio dramático antes del giro y subida
    g0 = int((scenes[5]['t0'] - 0.1) * SR); mix[g0:nrev] *= np.linspace(1, 0.15, nrev - g0)
    add(riser(0.9), REV - 0.9, 0.45)
    # después del giro: música de marca (pad mayor + bombo + hats)
    post = np.zeros(N - nrev); tp_ = tt[nrev:] - REV; beat2 = 60 / 118
    chords2 = [[261.6, 329.6, 392.0], [220.0, 261.6, 329.6], [174.6, 220.0, 261.6], [196.0, 246.9, 293.7]]
    for c in range(int((DUR - REV) / (beat2 * 4)) + 1):
        a = int(c * beat2 * 4 * SR); b = min(len(post), int((c + 1) * beat2 * 4 * SR)); st = tp_[a:b] - tp_[a] if b > a else tp_[a:b]
        env = np.minimum(1, st * 6) * np.exp(-st * 0.35)
        for f in chords2[c % 4]: post[a:b] += np.sin(2 * np.pi * f * st) * env * 0.33 + np.sin(2 * np.pi * f * 2.003 * st) * env * 0.08
    mix[nrev:] += post * 0.22
    for k in range(int((DUR - REV) / beat2) + 1):
        add(kick, REV + k * beat2, 0.55); add(hat, REV + k * beat2 + beat2 / 2, 0.12)
    add(boom(1.4), REV, 0.9)
    # efectos propios de cada escena
    for s in scenes:
        if s['type'] == 'open':
            for j in range(len(s['time'])): add(pop(3200, .02) * .7, s['tAt'] + j / 12, 0.5)
        if s['type'] == 'chat':
            add(pop(1500, .1), s['q1'], .5); add(pop(990, .14), s['q2'], .5); add(boom(.6), s['nd'], .8)
        if s['type'] == 'tabs':
            last = 1
            for fr in range(int((s['nAt'] - s['t0']) * 30)):
                tt_ = s['t0'] + fr / 30; n = max(1, min(s['n'], int(1 + (s['n'] - 1) * min(1, max(0, (tt_ - s['t0'] - .2) / (s['nAt'] - s['t0'] - .2))) ** 1.4)))
                if n > last: add(pop(1800 + 40 * n, .04), tt_, .45); last = n
            for pt in s['pdfAt']: add(W0, pt - .1, .35)
            add(pop(660, .3), s['foundAt'], .5)
        if s['type'] == 'closed': add(boom(1.0), s['stampAt'] + .05, 1.0); add(boom(.8), s['ayerAt'], .8)
        if s['type'] == 'stat':
            for k in range(16): add(tick(), s['t0'] + .15 + 1.45 * (1 - (1 - k / 16) ** (1 / 3)), 0.5)
            add(boom(.7), s['n2At'], .8)
        if s['type'] == 'phone' and s.get('note'): add(pop(1320), s['noteAt'] + .05, .5); add(pop(1760, .12), s['noteAt'] + .13, .35)
        if s['type'] == 'end': add(pop(1200, .15), s['t0'] + 0.9, 0.5)
        if s['t0'] > 0.2 and s['type'] not in ('line',): add(W0, s['t0'] - 0.21, 0.4)
    add(boom(1.6), 0.0, 0.9)
elif getattr(C, 'MOOD', '') == 'wrap':
    # Resumen: electro-pop alegre a 122 bpm, todo al compás
    mix[:] = 0; bpm = 122; b = 60 / bpm; nb = int(DUR / b) + 2
    prog = [[261.63, 329.63, 392.0], [220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [196.0, 246.94, 293.66]]
    roots = [65.41, 55.0, 43.65, 49.0]
    def tone(f, d, dec=6, harm=4):
        n = int(d * SR); x = np.arange(n) / SR
        return sum(np.sin(2 * np.pi * f * h * x) / h ** 1.3 for h in range(1, harm + 1)) * np.exp(-x * dec) * (1 - np.exp(-x * 600))
    rng = np.random.default_rng(3)
    clap = rng.standard_normal(int(.18 * SR)) * np.exp(-np.arange(int(.18 * SR)) / SR * 30)
    for k in range(nb):
        t0_ = k * b; bar = (k // 4) % 4
        if t0_ > DUR: break
        intro = t0_ < scenes[1]['t0'] - .05
        add(kick, t0_, .35 if intro else .75)
        if not intro:
            if k % 2 == 1: add(clap, t0_, .22)
            add(hat, t0_ + b / 2, .16)
            add(tone(roots[bar], b * .9, 5, 6), t0_, .22); add(tone(roots[bar], b * .45, 9, 6), t0_ + b / 2, .14)
        for j in range(2):
            f = prog[bar][(k * 2 + j) % 3] * 2
            add(tone(f, b * .5, 9, 3), t0_ + j * b / 2, .07 if intro else .09)
        if k % 4 == 0:
            for f in prog[bar]:
                add(tone(f, b * 4, .6, 3), t0_, .05)
    for s in scenes:
        if s['t0'] > 0.2: add(W0, s['t0'] - 0.2, 0.55); add(boom(.5), s['t0'], .45)
        if s['type'] == 'num':
            for k in range(18): add(tick(), s['t0'] + .15 + 1.35 * (1 - (1 - k / 18) ** (1 / 3)), .4)
            add(pop(1320), s['n2At'], .45)
        if s['type'] == 'date':
            add(pop(990, .15), s['calAt'], .5)
            for k in range(14): add(pop(1500 + 60 * k, .03), s['nAt'] + 1.1 * (1 - (1 - k / 14) ** 2), .25)
            add(pop(1760, .12), s['tagAt'], .45)
        if s['type'] == 'versus': add(riser(1.0), s['growAt'], .3); add(boom(.8), s['badgeAt'], .7)
        if s['type'] == 'share':
            for k in range(12): add(tick(), s['t0'] + .3 + 1.1 * k / 12, .35)
        if s['type'] == 'club': add(pop(880, .2), s['nameAt'], .45); add(pop(1320), s['cAt'], .45)
        if s['type'] == 'dots':
            add(boom(.6), s['wordAt'], .6)
            for i in range(s['on']): add(pop(1200 + 90 * i, .06), s['fillAt'] + i * .07, .35)
        if s['type'] == 'price': add(boom(.9), s['pAt'], .8); add(pop(2200, .08), s['pAt'] + .05, .4)
        if s['type'] == 'ask': add(pop(990, .15), s['a1'], .5); add(pop(1320, .15), s['a2'], .45)
        if s['type'] == 'end': add(pop(1200, .15), s['t0'] + .8, .5)
    add(boom(1.2), 0.0, 0.6)
else:
    for s in scenes:
        if s['t0'] > 0.2: add(W0, s['t0'] - 0.21, 0.55)
        if s.get('flash'): add(boom(), s['t0'], 0.7)
    add(boom(1.2), 0.0, 0.8)
    for s in scenes:
        if s['type'] in ('cards', 'profile') and 'rows' in s:
            for j in range(len(s['rows'])): add(pop(990 + 60 * j), s['t0'] + (1.2 if s['type'] == 'profile' else .25) + j * s.get('gap', .28) + .05, 0.35)
        if s['type'] == 'notifs':
            for j in range(len(s['items'])): add(pop(1320), s['t0'] + .15 + j * .38 + .05, 0.45); add(pop(1760, .12), s['t0'] + .15 + j * .38 + .13, 0.3)
        if s['type'] == 'counter':
            for k in range(14): add(tick(), s['t0'] + .1 + (s.get('dur', 1.4)) * (1 - (1 - k / 14) ** (1 / 3)), 0.5)
        if s['type'] == 'cal':
            n_ = len(s['counts']); st_ = s.get('step') or ((s['t1'] - s['t0'] - 1.3) / n_)
            for j in range(n_): add(tick(), s['t0'] + .35 + j * st_ + .05, 0.28)
        if s['type'] == 'shuffle':
            iv_ = s.get('iv', .17); k_ = 0
            while s['t0'] + .15 + k_ * iv_ < s['t1'] - .05 and k_ < len(s['rows']): add(tick(), s['t0'] + .15 + k_ * iv_, 0.5); k_ += 1
        if s.get('stamp'): add(boom(.5), s['t0'] + s.get('stampAt', .9), 0.8)
        for h in s.get('hits', []): add(boom(.7), h, .85)
        for q in s.get('pops', []): add(pop(1320, .1), q, .45)
        if s['type'] == 'bars':
            for j in range(len(s['items'])): add(pop(660 + 80 * j, .07), s['t0'] + .3 + j * .18, 0.3)
        if s['type'] == 'end': add(riser(), s['t0'] - 0.6, 0.35); add(pop(1200, .15), s['t0'] + 0.9, 0.5)
mix *= 0.9 / (np.abs(mix).max() + 1e-9)
with wave.open(f'{D}/{rid}_fx.wav', 'w') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
if NOVO:
    r = sh('ffmpeg', '-y', '-i', f'{D}/{rid}_v.mp4', '-i', f'{D}/{rid}_fx.wav', '-filter_complex', '[1:a]loudnorm=I=-14:TP=-1.2[a]', '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', f'{D}/{C.OUT}')
    print(r.stderr[-400:] if r.returncode else 'listo ' + C.OUT); sys.exit()
d_ms = int(LEAD * 1000)
r = sh('ffmpeg', '-y', '-i', f'{D}/{rid}_v.mp4', '-i', f'{D}/{rid}_fx.wav', '-i', vo, '-filter_complex',
       f'[1:a]volume=0.32[m];[2:a]adelay={d_ms}|{d_ms},loudnorm=I=-15:TP=-1.5,volume=1.0[v];[m][v]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]',
       '-map', '0:v', '-map', '[a]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', f'{D}/{C.OUT}')
print(r.stderr[-400:] if r.returncode else 'listo ' + C.OUT)
