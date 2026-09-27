"""WEBRA 30s spot - procedural score + sound design (120 BPM, A minor).
Writes audio.wav (48 kHz stereo). Cue times match index.html."""
import numpy as np, wave

SR = 48000; DUR = 30.0; BPM = 120; BEAT = 60 / BPM
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(7)

def t_(d): return np.arange(int(d * SR)) / SR
def add(sig, at, gain=1.0, pan=0.0):
    i = int(at * SR); j = min(N, i + len(sig))
    if j <= i: return
    s = sig[: j - i] * gain
    L[i:j] += s * np.sqrt((1 - pan) / 2) * 1.414; R[i:j] += s * np.sqrt((1 + pan) / 2) * 1.414
def lp(x, fc):  # one-pole lowpass
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); s = 0.0
    for i, v in enumerate(x): s = (1 - a) * v + a * s; y[i] = s
    return y
def hp(x, fc): return x - lp(x, fc)
def env(n, a, d):  # attack/exp-decay envelope in seconds
    t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)

# ---------- instruments ----------
def kick(g=1.0):
    t = t_(0.45); f = 44 + 90 * np.exp(-t * 38)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7) * g
def hat(open_=False):
    n = rng.standard_normal(int(SR * (0.18 if open_ else 0.05)))
    return hp(n, 7000) * env(len(n), 0.001, 0.05 if open_ else 0.012)
def clap():
    n = rng.standard_normal(int(SR * 0.25)); e = env(len(n), 0.001, 0.06)
    for k in (0.008, 0.017): e[int(k * SR):] += 0.6 * env(len(n) - int(k * SR), 0.001, 0.02)
    return lp(hp(n, 900), 5000) * e * 0.5
def impact(size=1.0):  # deep, restrained hit for typography
    t = t_(1.6 * size); f = 32 + 70 * np.exp(-t * 18)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2 / size)
    n = lp(rng.standard_normal(len(t)), 900) * env(len(t), 0.001, 0.12 * size)
    return body * 0.9 + n * 0.5
def whoosh(d=0.6, rev=False):
    n = rng.standard_normal(int(SR * d)); x = np.linspace(0, 1, len(n))
    shape = np.sin(np.pi * x) ** 2 if not rev else x ** 3
    out = np.zeros_like(n); seg = len(n) // 16
    for k in range(16):  # sweeping band
        fc = 400 + 5000 * (k / 15 if not rev else (k / 15) ** 2)
        s = n[k * seg:(k + 1) * seg]; out[k * seg:(k + 1) * seg] = lp(hp(s, fc * .5), fc)
    return out * shape * 0.8
def tick(f=2400, d=0.05):
    t = t_(d); return np.sin(2 * np.pi * f * t) * env(len(t), 0.0005, 0.012)
def key(f=1800):  # soft typing click
    t = t_(0.03); return (np.sin(2 * np.pi * f * t) * .5 + lp(rng.standard_normal(len(t)), 5000) * .5) * env(len(t), 0.0003, 0.006)
def glitch(d=0.35):
    t = t_(d); sq = np.sign(np.sin(2 * np.pi * 180 * t * (1 + 3 * (np.floor(t * 40) % 3))))
    return sq * (np.floor(t * 24) % 2) * 0.25 * env(len(t), 0.001, 0.2)
def shatter():
    out = np.zeros(int(SR * 1.2))
    for k in range(26):
        at = int(abs(rng.normal(0, 0.12)) * SR); f = rng.uniform(2500, 7000)
        s = tick(f, 0.12) * rng.uniform(.3, 1); out[at:at + len(s)] += s[: len(out) - at]
    n = hp(rng.standard_normal(len(out)), 3000) * env(len(out), 0.001, 0.15)
    return out * .5 + n * .4
def bell(f, d=2.4):  # FM bell for the sonic logo
    t = t_(d); m = np.sin(2 * np.pi * f * 3.5 * t) * 2.2 * np.exp(-t * 3)
    return np.sin(2 * np.pi * f * t + m) * env(len(t), 0.002, 0.9)
def pad(freqs, d):
    t = t_(d); s = np.zeros(len(t))
    for f in freqs:
        for det in (-0.12, 0.0, 0.11):
            ph = 2 * np.pi * f * (1 + det / 100) * t; s += 2 * (ph / (2 * np.pi) % 1) - 1
    s = lp(s / (3 * len(freqs)), 1100)
    a = np.minimum(1, t / 0.6) * np.minimum(1, (d - t) / 0.6); return s * a
def bass(f, d):
    t = t_(d); s = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)
    return s * np.minimum(1, t / 0.01) * np.exp(-t * 1.2)

# ---------- score ----------
# progression per bar (2 s): Am - F - C - G (roots) ; hook is sparse, 22-24 breakdown
roots = [55.0, 43.65, 65.41, 49.0]
chords = [[220, 261.6, 329.6], [174.6, 220, 261.6], [196, 261.6, 329.6], [196, 246.9, 293.7]]
bar = 4 * BEAT
for b in range(15):
    t0 = b * bar
    if t0 >= 22 and t0 < 24: continue          # breakdown before the logo hit
    ch = chords[b % 4]; add(pad(ch, bar + .3), t0, 0.16 if t0 < 4 else 0.20)
    if t0 >= 4 and t0 < 27:
        for q in range(8):                    # eighth-note bass with kick ducking
            add(bass(roots[b % 4] * (2 if q % 4 == 3 else 1), BEAT / 2), t0 + q * BEAT / 2, 0.30)
for i in range(60):
    t = i * BEAT
    if 4 <= t < 22 or 24 <= t < 27:
        add(kick(), t, 0.85)
        add(hat(), t + BEAT / 2, 0.18, 0.3)
        add(hat(), t + BEAT / 4, 0.07, -0.3); add(hat(), t + 3 * BEAT / 4, 0.07, -0.3)
        if i % 2: add(clap(), t, 0.35)
    elif t < 4 and i % 4 == 0 and t >= 2:
        add(kick(), t, 0.6)
# riser into the logo + CTA outro pulse
add(whoosh(2.0, rev=True), 22.0, 0.5)
for i in range(6): add(kick(0.7), 27 + i * BEAT, 0.5)

# ---------- sound design cues ----------
add(whoosh(1.2, rev=True), 0.0, 0.25)                          # phone approach
add(tick(3000, .1), 1.0, .3); add(shatter(), 1.25, 0.9)        # crack + shatter
for at, g in [(1.5, .8), (1.75, .9), (2.0, 1.0)]: add(impact(.8), at, g)  # JUST AN / INSTAGRAM / PAGE?
add(glitch(), 3.0, 0.9); add(whoosh(.55), 3.3, 0.8)            # distort + exit
add(whoosh(1.0, rev=True), 3.4, 0.35)                          # shapes rush in
for at in [5.0, 5.2, 5.3, 5.4, 5.5, 5.9, 6.0, 6.125, 6.25]: add(tick(2000 + 900 * ((at * 7) % 1)), at, .35, .4 * np.sin(at * 9))
add(whoosh(.9), 6.95, 0.35)                                     # desktop -> mobile morph
add(impact(1.0), 7.98, 1.0); add(impact(.6), 8.2, .6)          # BUILD IT.
add(whoosh(1.1), 8.0, 0.3); add(whoosh(.5), 9.4, 0.6)          # camera move / collapse
for i in range(3): add(tick(1500 + i * 400, .08), 10.0 + i * .07, .25, (i - 1) * .6)  # search bars form
for c in range(25): add(key(1600 + (c % 5) * 90), 10.8 + c * 0.046, 0.45, 0.2)       # typing
add(tick(1200, .12), 12.0, .5)                                  # enter
for i in range(3): add(tick(2600, .06), 12.1 + i * .08, .25)
add(whoosh(.6), 12.45, 0.4); add(bell(880, 1.2), 13.0, 0.18)   # business found
add(impact(1.0), 13.48, 1.0); add(impact(.6), 13.72, .6)       # GET FOUND.
add(whoosh(1.0, rev=True), 15.0, 0.6); add(impact(.7), 16.0, .5)  # circular wipe
for i in range(8): add(glitch(.08), 16.1 + i * .21, .25)        # scattered tasks
add(whoosh(.5), 17.8, 0.5); add(impact(.6), 18.0, .6)           # snap into system
for k in range(8): add(tick(1760 * 2 ** (k / 12 * 2), .09), 18.5 + k * .25, .35, (k % 2 - .5))  # task resolves
add(impact(1.0), 19.46, 1.0); add(impact(.6), 19.72, .6)       # AUTOMATE IT.
add(whoosh(.7), 21.2, 0.6)                                     # converge to stripes
# sonic logo: low hit + three-note bell motif (E5 - B5 - A5) with echo
add(impact(1.6), 24.0, 1.3)
for k, (f, at) in enumerate([(659.3, 24.0), (987.8, 24.25), (880.0, 24.5)]):
    for e in range(4): add(bell(f), at + e * 0.375, 0.32 * 0.45 ** e, (-.5, .5)[(k + e) % 2])
for at in (25.0, 25.5, 26.0): add(tick(2200, .06), at, .25)    # tagline words
add(whoosh(.6), 26.55, 0.5)
add(impact(.8), 27.0, .7); add(impact(.9), 28.0, .8); add(tick(1800, .1), 28.5, .4)
add(bell(659.3, 2.5), 28.5, .15)

# ---------- master ----------
mix = np.stack([L, R]); mix = np.tanh(mix * 1.1)
fade = np.ones(N); k = int(1.2 * SR); fade[-k:] = np.linspace(1, 0, k) ** 2
mix *= fade; mix /= np.max(np.abs(mix)) / 0.89
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix.T * 32767).astype('<i2').tobytes())
print('audio.wav written')
