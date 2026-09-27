"""WEBRA v2 soundscape — SFX ONLY. No music, no melody, no beat, no pitched motif.
Realistic interface sounds (taps, key clicks, switches, soft whooshes) synced to index.html.
Mixed low with headroom so a Georgian voiceover can sit on top. Writes audio.wav (48 kHz stereo)."""
import numpy as np, wave
from scipy.signal import butter, sosfilt, fftconvolve

SR = 48000; DUR = 30.0; N = int(SR * DUR)
out = np.zeros((2, N)); room = np.zeros((2, N))
rng = np.random.default_rng(5)

def t_(d): return np.arange(int(d * SR)) / SR
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def env(n, a, d):
    t = np.arange(n) / SR; return np.minimum(1, t / max(a, 1e-5)) * np.exp(-t / d)
def db(x): return 10 ** (x / 20)
def add(sig, at, gain_db=0.0, pan=0.0, wet=0.15):
    i = int(round(at * SR)); j = min(N, i + len(sig))
    if j <= i: return
    s = sig[: j - i] * db(gain_db); lg, rg = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    out[0, i:j] += s * lg; out[1, i:j] += s * rg
    room[0, i:j] += s * lg * wet; room[1, i:j] += s * rg * wet
def norm(x): return x / (np.max(np.abs(x)) + 1e-9)

# ---------------- sound sources (all unpitched / percussive) ----------------
def click(bright=1.0, body=1.0):            # crisp UI click: transient + tiny plastic body
    n = int(SR * .045); x = rng.standard_normal(n)
    tr = hp(x, 2500 * bright) * env(n, .0002, .0012)
    bd = bp(x, 900, 2600) * env(n, .0005, .006) * .6 * body
    return norm(tr + bd)
def tap():                                    # soft finger tap on glass
    n = int(SR * .08); x = rng.standard_normal(n)
    return norm(lp(x, 1800) * env(n, .0008, .012) + hp(x, 4000) * env(n, .0002, .002) * .3)
def pop():                                    # soft notification pop (fast downward "bloop", percussive)
    t = t_(.07); f = 900 * np.exp(-t * 55) + 160
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), .001, .014)
    return norm(s + tap() [:len(t)] * .35)
def key(heavy=False):                         # keyboard key: press click + bottom-out thock + release
    n = int(SR * .09); x = rng.standard_normal(n)
    press = hp(x, 3000) * env(n, .0002, .0015)
    thock = bp(x, 250 + rng.uniform(-40, 60), 1400) * env(n, .0006, .009 if heavy else .006)
    s = press * .7 + thock
    r = int(SR * rng.uniform(.045, .07)); s[r:] += hp(x[: n - r], 3500) * env(n - r, .0002, .001) * .35
    return norm(s)
def whoosh(d=.5, lo=300, hi=3500):            # short, clean air movement (band sweep)
    n = int(SR * d); x = rng.standard_normal(n); u = np.linspace(0, 1, n)
    seg = 24; y = np.zeros(n); L = n // seg
    for k in range(seg):
        c = lo + (hi - lo) * np.sin(np.pi * (k + .5) / seg)
        y[k * L:(k + 1) * L] = bp(x[k * L:(k + 1) * L + 0] if k < seg - 1 else x[k * L:(k + 1) * L], c * .6, c * 1.4)
    return norm(lp(y, 6000)) * np.sin(np.pi * u) ** 2
def swipe():                                  # finger swipe on glass
    n = int(SR * .22); x = rng.standard_normal(n); u = np.linspace(0, 1, n)
    return norm(bp(x, 2000, 7000)) * np.sin(np.pi * u) ** 3 * .6
def switch():                                 # mechanical toggle: two-stage click with low body
    a = click(.7, 1.6); b = click(1.1, .8)
    s = np.zeros(int(SR * .1)); s[:len(a)] += a; o = int(.028 * SR); s[o:o + len(b)] += b * .8
    n = len(s); s += lp(rng.standard_normal(n), 400) * env(n, .001, .01) * .5
    return norm(s)
def confirm():                                # completion: soft double click + short airy release
    s = np.zeros(int(SR * .45)); a = click(1.2); o = int(.07 * SR)
    s[:len(a)] += a * .8; s[o:o + len(a)] += a
    n = len(s); u = np.linspace(0, 1, n); s += bp(rng.standard_normal(n), 3000, 9000) * np.exp(-u * 9) * (u > .15) * .18
    return norm(s)
def impact():                                 # restrained, deep logo impact (noise body + sub thump, no tone)
    t = t_(1.2); f = 55 * np.exp(-t * 6) + 30
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(t), .003, .18)
    bodyn = lp(rng.standard_normal(len(t)), 700) * env(len(t), .001, .06)
    return norm(sub * .9 + bodyn * .5)
def sonic_logo():                             # non-musical signature: air-in, "shutter" double click, soft settle
    s = np.zeros(int(SR * 1.3))
    w = whoosh(.45, 800, 6000) * np.linspace(0, 1, int(SR * .45)) ** 1.5; s[:len(w)] += w * .5
    for k, o in enumerate((.43, .49)):
        c = click(1.3 if k else .9, 1.2); i = int(o * SR); s[i:i + len(c)] += c
    th = impact()[: int(SR * .7)] * .45; i = int(.49 * SR); s[i:i + len(th)] += th
    return norm(s)

# ---------------- cue sheet (seconds, synced to picture) ----------------
Q = []
def cue(at, sig, g, pan=0.0, wet=.12): Q.append((at, sig, g, pan, wet))
# 0–3.8 opening
cue(0.32, pop(), -16)                                   # Instagram page appears
cue(0.45, tap(), -20, -.1)                              # question appears
cue(0.84, swipe(), -33, .2)
cue(1.88, whoosh(.45, 250, 2200), -31, 0, .2)           # final opening statement
cue(3.62, whoosh(.6, 300, 3000), -29, .1, .25)          # phone -> website
# 5–9 website
for i in range(15): cue(4.40 + i * .037 + rng.uniform(-.004, .004), key(), -23 + rng.uniform(-2, 1), .15)
cue(4.98, click(1.0, 1.2), -16)                         # website loads
cue(6.98, whoosh(.5, 400, 2600), -36, -.1, .2)          # desktop -> mobile (very soft)
cue(9.05, whoosh(.6, 300, 3200), -29, 0, .25)           # website -> search scene
# 10–14.6 search
for i in range(26): cue(10.30 + i * .046 + rng.uniform(-.005, .005), key(i % 7 == 3), -23 + rng.uniform(-2, 1), -.1)
cue(11.50, click(.9, 1.5), -17)                         # search confirm
cue(11.66, pop(), -18, .05)                             # business listing appears
for k in range(3): cue(12.20 + k * .08, tap(), -25, -.25 + k * .25)   # listing buttons
cue(14.82, whoosh(.7, 250, 2800), -28, 0, .25)          # pan down to automation
# 15.6–20.6 automation
cue(17.45, switch(), -17)                               # manual -> automatic
for k in range(6): cue(18.30 + k * .25, click(1.1, .9), -22, -.2 + k * .08)   # each task confirmed
cue(19.72, confirm(), -18, 0, .2)                       # sequence complete
cue(20.72, whoosh(.55, 300, 2600), -30, 0, .25)         # chips -> stripes
cue(22.70, whoosh(.9, 200, 1800), -34, 0, .3)           # pattern folds (very soft)
# 24–30 end card
cue(23.95, impact(), -22, 0, .2)                        # WEBRA logo
cue(24.60, click(), -22)                                # slogan
cue(25.62, click(), -23, -.1); cue(25.77, click(), -27, .1)   # contact details
cue(28.40, sonic_logo(), -21, 0, .2)                    # non-musical sign-off; silence to the end
for at, sig, g, pan, wet in Q: add(sig, at, g, pan, wet)

# ---------------- small-room reverb + master (headroom for voiceover) ----------------
it = t_(.45); ir = rng.standard_normal((2, len(it))) * np.exp(-it * 14); ir = np.stack([lp(ir[c], 6000) for c in (0, 1)])
mix = out + np.stack([fftconvolve(room[c], ir[c])[:N] for c in (0, 1)]) * .25
mix = np.stack([hp(mix[c], 30) for c in (0, 1)])
mix *= db(-3) / max(np.max(np.abs(mix)), 1e-9)          # peaks at -3 dBFS, no limiting, no loudness push
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix.T * 32767).astype('<i2').tobytes())
print('audio.wav written (SFX only)')
